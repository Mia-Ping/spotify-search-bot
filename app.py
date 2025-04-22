import os
from flask import Flask, session, request, redirect, render_template, url_for, jsonify
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json
import requests
from werkzeug.utils import secure_filename
from audio_processor import AudioProcessor, AudDRecognizer

# Ensure directories exist at runtime
os.makedirs('/data/flask_session', exist_ok=True)
os.makedirs('/data/uploads', exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(64))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/data/flask_session/'
app.config['UPLOAD_FOLDER'] = '/data/uploads'
Session(app)

# Spotify API credentials - use environment variables in production
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID', '112198efe8bc4ae49492ad78031679a8')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET', '9deeb3255e3d4d7187903c8b5ae2dd90')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI', 'http://localhost:5000/callback')
SCOPE = 'user-library-read user-library-modify playlist-read-private playlist-modify-private user-read-private'

# AudD API key - use environment variable in production
AUDD_API_KEY = os.environ.get('AUDD_API_KEY', 'test')

# Cache handler for Spotify tokens
cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)

# Initialize audio processor and recognizer
audio_processor = AudioProcessor(app.config['UPLOAD_FOLDER'])
audd_recognizer = AudDRecognizer(AUDD_API_KEY)

@app.route('/')
def index():
    # Check if user is authenticated
    if not is_authenticated():
        return render_template('login.html')
    
    # Get Spotify client
    sp = get_spotify_client()
    
    # Get user info
    user_info = sp.current_user()
    
    # Get user's playlists
    playlists = sp.current_user_playlists()
    
    return render_template('index.html', 
                          user_info=user_info, 
                          playlists=playlists)

@app.route('/login')
def login():
    # Create Spotify OAuth manager
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Process the callback from Spotify
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/')

@app.route('/logout')
def logout():
    # Clear session and log out
    session.clear()
    return redirect('/')

@app.route('/search')
def search():
    # Check if user is authenticated
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get query parameter
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Get Spotify client
    sp = get_spotify_client()
    
    # Search for tracks
    results = sp.search(q=query, type='track', limit=20)
    tracks = results['tracks']['items']
    
    # Get user's playlists
    playlists = sp.current_user_playlists()
    playlist_ids = [playlist['id'] for playlist in playlists['items']]
    
    # Get tracks from user's playlists
    user_tracks = []
    for playlist_id in playlist_ids:
        playlist_tracks = sp.playlist_tracks(playlist_id)
        user_tracks.extend([item['track'] for item in playlist_tracks['items']])
    
    # Filter tracks that are in user's playlists
    user_track_ids = [track['id'] for track in user_tracks]
    filtered_tracks = [track for track in tracks if track['id'] in user_track_ids]
    
    # If no tracks found in user's playlists, return all search results
    if not filtered_tracks:
        # Get recommendations based on search results if available
        if tracks:
            seed_tracks = [track['id'] for track in tracks[:5]]
            recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10)
            tracks.extend(recommendations['tracks'])
        return jsonify(tracks)
    
    return jsonify(filtered_tracks)

@app.route('/identify', methods=['POST'])
def identify():
    # Check if user is authenticated
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if file is in request
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    # Process audio
    processed_filepath = audio_processor.process_audio(file)
    
    # Identify song
    result = audd_recognizer.identify_song(processed_filepath)
    
    # Clean up files
    audio_processor.cleanup_files(processed_filepath)
    
    # Process AudD response
    if result.get('status') == 'success' and result.get('result'):
        # Get Spotify client
        sp = get_spotify_client()
        
        # Get track info from Spotify
        spotify_id = result['result'].get('spotify', {}).get('id')
        if spotify_id:
            track = sp.track(spotify_id)
            
            # Get recommendations based on identified track
            recommendations = sp.recommendations(seed_tracks=[spotify_id], limit=10)
            tracks = [track] + recommendations['tracks']
            
            return jsonify(tracks)
        else:
            # If no Spotify ID, search by title and artist
            title = result['result'].get('title', '')
            artist = result['result'].get('artist', '')
            if title and artist:
                query = f"track:{title} artist:{artist}"
                results = sp.search(q=query, type='track', limit=10)
                return jsonify(results['tracks']['items'])
    
    return jsonify({'error': 'Could not identify song'}), 404

@app.route('/match-humming', methods=['POST'])
def match_humming():
    # Check if user is authenticated
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if file is in request
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    # Process audio
    processed_filepath = audio_processor.process_audio(file)
    
    # Match humming
    result = audd_recognizer.match_humming(processed_filepath)
    
    # Clean up files
    audio_processor.cleanup_files(processed_filepath)
    
    # Get Spotify client
    sp = get_spotify_client()
    
    # Process AudD response for humming
    if result.get('status') == 'success' and result.get('result'):
        # If direct match found
        spotify_id = result['result'].get('spotify', {}).get('id')
        if spotify_id:
            track = sp.track(spotify_id)
            return jsonify([track])
    
    # If no direct match, check for similar matches
    if result.get('status') == 'success' and result.get('matches'):
        tracks = []
        for match in result['matches']:
            spotify_id = match.get('spotify', {}).get('id')
            if spotify_id:
                track = sp.track(spotify_id)
                tracks.append(track)
        
        if tracks:
            return jsonify(tracks)
    
    # If no matches found, try to search user's playlists
    # This is a fallback and may not be accurate for humming
    playlists = sp.current_user_playlists()
    playlist_ids = [playlist['id'] for playlist in playlists['items']]
    
    # Get a sample of tracks from user's playlists
    sample_tracks = []
    for playlist_id in playlist_ids[:5]:  # Limit to first 5 playlists for performance
        playlist_tracks = sp.playlist_tracks(playlist_id, limit=10)
        sample_tracks.extend([item['track'] for item in playlist_tracks['items']])
    
    # Return a sample of user's tracks as potential matches
    # This is not ideal but provides some results when humming recognition fails
    if sample_tracks:
        return jsonify(sample_tracks[:20])
    
    return jsonify({'error': 'Could not match humming to any songs'}), 404

@app.route('/playlist/<playlist_id>')
def playlist(playlist_id):
    # Check if user is authenticated
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get Spotify client
    sp = get_spotify_client()
    
    # Get playlist tracks
    results = sp.playlist_tracks(playlist_id)
    tracks = [item['track'] for item in results['items']]
    
    return jsonify(tracks)

@app.route('/add-to-liked', methods=['POST'])
def add_to_liked():
    # Check if user is authenticated
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated', 'success': False}), 401
    
    # Get track ID from request
    data = request.json
    track_id = data.get('track_id')
    
    if not track_id:
        return jsonify({'error': 'No track ID provided', 'success': False}), 400
    
    # Get Spotify client
    sp = get_spotify_client()
    
    # Add track to user's Liked Songs
    try:
        sp.current_user_saved_tracks_add([track_id])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

def is_authenticated():
    # Check if user is authenticated
    return 'token_info' in session

def get_spotify_client():
    # Get Spotify client with proper authentication
    token_info = get_token()
    if not token_info:
        return None
    return spotipy.Spotify(auth=token_info['access_token'])

def get_token():
    # Get and refresh token if needed
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    
    # Check if token is expired and refresh if needed
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    
    return token_info

def create_spotify_oauth():
    # Create Spotify OAuth manager
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_handler=cache_handler
    )

if __name__ == '__main__':
    # Get port from environment variable for production deployment
    port = int(os.environ.get('PORT', 5000))
    # In production, don't use debug mode
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=debug)
