import os
import wave
import numpy as np
from flask import Flask, request, jsonify
import requests

class AudioProcessor:
    """
    Class for processing audio files and preparing them for recognition
    """
    
    def __init__(self, upload_folder='./uploads'):
        """Initialize with upload folder path"""
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def save_audio(self, file, filename=None):
        """Save uploaded audio file"""
        if filename is None:
            filename = file.filename if file.filename else 'audio.wav'
        
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        return filepath
    
    def convert_to_wav(self, filepath):
        """Convert audio to WAV format if needed"""
        # This is a simplified version - in a real app, you'd use a library like pydub
        # to convert various formats to WAV
        filename, ext = os.path.splitext(filepath)
        
        if ext.lower() != '.wav':
            # For now, we'll just return the original file
            # In a real implementation, you would convert the file here
            return filepath
        
        return filepath
    
    def normalize_audio(self, filepath):
        """Normalize audio volume and quality for better recognition"""
        try:
            # Open the WAV file
            with wave.open(filepath, 'rb') as wf:
                # Get basic info
                channels = wf.getnchannels()
                width = wf.getsampwidth()
                rate = wf.getframerate()
                frames = wf.getnframes()
                
                # Read all frames
                raw_data = wf.readframes(frames)
                
                # Convert to numpy array
                if width == 1:  # 8-bit audio
                    dtype = np.uint8
                else:  # 16-bit or higher audio
                    dtype = np.int16
                
                data = np.frombuffer(raw_data, dtype=dtype)
                
                if channels == 2:
                    # Convert stereo to mono by averaging channels
                    data = data.reshape(-1, 2).mean(axis=1).astype(dtype)
                
                # Normalize volume
                if data.size > 0:
                    max_val = np.max(np.abs(data))
                    if max_val > 0:
                        data = data * (32767 / max_val)
                    data = data.astype(np.int16)
                
                # Write normalized data to a new file
                normalized_filepath = os.path.join(
                    os.path.dirname(filepath),
                    'normalized_' + os.path.basename(filepath)
                )
                
                with wave.open(normalized_filepath, 'wb') as wf_out:
                    wf_out.setnchannels(1)  # Mono
                    wf_out.setsampwidth(2)  # 16-bit
                    wf_out.setframerate(rate)
                    wf_out.writeframes(data.tobytes())
                
                return normalized_filepath
                
        except Exception as e:
            print(f"Error normalizing audio: {e}")
            # Return original file if normalization fails
            return filepath
    
    def process_audio(self, file):
        """Process audio file for recognition"""
        # Save the uploaded file
        filepath = self.save_audio(file)
        
        # Convert to WAV if needed
        wav_filepath = self.convert_to_wav(filepath)
        
        # Normalize audio
        normalized_filepath = self.normalize_audio(wav_filepath)
        
        return normalized_filepath
    
    def cleanup_files(self, *filepaths):
        """Clean up temporary files"""
        for filepath in filepaths:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Error removing file {filepath}: {e}")


class AudDRecognizer:
    """
    Class for recognizing songs using the AudD API
    """
    
    def __init__(self, api_key):
        """Initialize with AudD API key"""
        self.api_key = api_key
        self.api_url = 'https://api.audd.io/'
    
    def identify_song(self, filepath, return_spotify=True):
        """Identify a song from an audio file"""
        try:
            with open(filepath, 'rb') as f:
                data = {
                    'api_token': self.api_key,
                    'return': 'spotify' if return_spotify else 'apple_music,deezer'
                }
                files = {
                    'file': f
                }
                response = requests.post(self.api_url, data=data, files=files)
                return response.json()
        except Exception as e:
            print(f"Error identifying song: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def match_humming(self, filepath, return_spotify=True):
        """Match humming to a song"""
        try:
            with open(filepath, 'rb') as f:
                data = {
                    'api_token': self.api_key,
                    'return': 'spotify' if return_spotify else 'apple_music,deezer',
                    'return_matches': 'true'  # This tells AudD to try to match humming
                }
                files = {
                    'file': f
                }
                response = requests.post(self.api_url, data=data, files=files)
                return response.json()
        except Exception as e:
            print(f"Error matching humming: {e}")
            return {'status': 'error', 'error': str(e)}
