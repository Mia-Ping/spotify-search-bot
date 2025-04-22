// Main Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Text search form submission
    const textSearchForm = document.getElementById('text-search-form');
    if (textSearchForm) {
        textSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.getElementById('search-query').value;
            if (query.trim() !== '') {
                searchByText(query);
            }
        });
    }
    
    // Audio recording functionality
    const recordBtn = document.getElementById('record-btn');
    const recordTimer = document.getElementById('record-timer');
    let mediaRecorder;
    let audioChunks = [];
    let startTime;
    let timerInterval;
    
    if (recordBtn) {
        recordBtn.addEventListener('click', function() {
            if (recordBtn.textContent === 'Start Recording') {
                startRecording();
            } else {
                stopRecording();
            }
        });
    }
    
    // Humming recording functionality
    const humRecordBtn = document.getElementById('hum-record-btn');
    const humTimer = document.getElementById('hum-timer');
    let humMediaRecorder;
    let humAudioChunks = [];
    let humStartTime;
    let humTimerInterval;
    
    if (humRecordBtn) {
        humRecordBtn.addEventListener('click', function() {
            if (humRecordBtn.textContent === 'Start Humming') {
                startHumming();
            } else {
                stopHumming();
            }
        });
    }
    
    // Audio file upload
    const audioUploadForm = document.getElementById('audio-upload-form');
    if (audioUploadForm) {
        audioUploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const audioFile = document.getElementById('audio-file').files[0];
            if (audioFile) {
                uploadAudioFile(audioFile);
            }
        });
    }
    
    // Playlist selection
    const playlistItems = document.querySelectorAll('.playlist-item');
    playlistItems.forEach(item => {
        item.addEventListener('click', function() {
            const playlistId = this.getAttribute('data-id');
            loadPlaylistTracks(playlistId);
        });
    });
    
    // Functions
    
    function searchByText(query) {
        // Show loading state
        document.getElementById('search-results').innerHTML = '<div class="loading">Searching...</div>';
        
        // Make API request to backend
        fetch('/search?query=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('search-results').innerHTML = 
                    '<div class="error">An error occurred while searching. Please try again.</div>';
            });
    }
    
    function startRecording() {
        // Request microphone access
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                audioChunks = [];
                mediaRecorder = new MediaRecorder(stream);
                
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.addEventListener('stop', () => {
                    clearInterval(timerInterval);
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    identifySong(audioBlob);
                });
                
                // Start recording
                mediaRecorder.start();
                recordBtn.textContent = 'Stop Recording';
                recordBtn.classList.add('recording');
                
                // Start timer
                startTime = Date.now();
                updateTimer(recordTimer);
                timerInterval = setInterval(() => updateTimer(recordTimer), 1000);
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                alert('Could not access microphone. Please check permissions and try again.');
            });
    }
    
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            recordBtn.textContent = 'Start Recording';
            recordBtn.classList.remove('recording');
            
            // Stop all audio tracks
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
    
    function startHumming() {
        // Request microphone access
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                humAudioChunks = [];
                humMediaRecorder = new MediaRecorder(stream);
                
                humMediaRecorder.addEventListener('dataavailable', event => {
                    humAudioChunks.push(event.data);
                });
                
                humMediaRecorder.addEventListener('stop', () => {
                    clearInterval(humTimerInterval);
                    const audioBlob = new Blob(humAudioChunks, { type: 'audio/wav' });
                    identifyByHumming(audioBlob);
                });
                
                // Start recording
                humMediaRecorder.start();
                humRecordBtn.textContent = 'Stop Humming';
                humRecordBtn.classList.add('recording');
                
                // Start timer
                humStartTime = Date.now();
                updateTimer(humTimer);
                humTimerInterval = setInterval(() => updateTimer(humTimer), 1000);
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                alert('Could not access microphone. Please check permissions and try again.');
            });
    }
    
    function stopHumming() {
        if (humMediaRecorder && humMediaRecorder.state !== 'inactive') {
            humMediaRecorder.stop();
            humRecordBtn.textContent = 'Start Humming';
            humRecordBtn.classList.remove('recording');
            
            // Stop all audio tracks
            humMediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
    
    function updateTimer(timerElement) {
        const currentTime = Date.now();
        const elapsedTime = currentTime - (timerElement === recordTimer ? startTime : humStartTime);
        const seconds = Math.floor(elapsedTime / 1000);
        const minutes = Math.floor(seconds / 60);
        const displaySeconds = (seconds % 60).toString().padStart(2, '0');
        const displayMinutes = minutes.toString().padStart(2, '0');
        timerElement.textContent = `${displayMinutes}:${displaySeconds}`;
    }
    
    function uploadAudioFile(file) {
        // Create FormData object
        const formData = new FormData();
        formData.append('audio', file);
        
        // Show loading state
        document.getElementById('search-results').innerHTML = '<div class="loading">Identifying song...</div>';
        
        // Make API request to backend
        fetch('/identify', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('search-results').innerHTML = 
                    '<div class="error">An error occurred while identifying the song. Please try again.</div>';
            });
    }
    
    function identifySong(audioBlob) {
        // Create FormData object
        const formData = new FormData();
        formData.append('audio', audioBlob);
        
        // Show loading state
        document.getElementById('search-results').innerHTML = '<div class="loading">Identifying song...</div>';
        
        // Make API request to backend
        fetch('/identify', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('search-results').innerHTML = 
                    '<div class="error">An error occurred while identifying the song. Please try again.</div>';
            });
    }
    
    function identifyByHumming(audioBlob) {
        // Create FormData object
        const formData = new FormData();
        formData.append('audio', audioBlob);
        
        // Show loading state
        document.getElementById('search-results').innerHTML = '<div class="loading">Matching your humming...</div>';
        
        // Make API request to backend
        fetch('/match-humming', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('search-results').innerHTML = 
                    '<div class="error">An error occurred while matching your humming. Please try again.</div>';
            });
    }
    
    function loadPlaylistTracks(playlistId) {
        // Show loading state
        document.getElementById('search-results').innerHTML = '<div class="loading">Loading playlist tracks...</div>';
        
        // Make API request to backend
        fetch('/playlist/' + playlistId)
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('search-results').innerHTML = 
                    '<div class="error">An error occurred while loading playlist tracks. Please try again.</div>';
            });
    }
    
    function displayResults(data) {
        const resultsContainer = document.getElementById('search-results');
        
        if (!data || data.length === 0) {
            resultsContainer.innerHTML = '<div class="empty-state">No results found</div>';
            return;
        }
        
        let html = '';
        
        data.forEach(track => {
            html += `
                <div class="track-item" data-id="${track.id}">
                    <img src="${track.album.images[0].url}" alt="${track.name}" class="track-img">
                    <div class="track-info">
                        <div class="track-name">${track.name}</div>
                        <div class="track-artist">${track.artists.map(artist => artist.name).join(', ')}</div>
                        <div class="track-actions">
                            <button class="play-btn" onclick="window.open('${track.external_urls.spotify}', '_blank')">▶</button>
                            <button class="add-btn" onclick="addToLiked('${track.id}')">+</button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        resultsContainer.innerHTML = html;
    }
});

// Function to add track to Liked Songs
function addToLiked(trackId) {
    fetch('/add-to-liked', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ track_id: trackId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Added to your Liked Songs!');
            } else {
                alert('Failed to add to Liked Songs: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding to Liked Songs');
        });
}
