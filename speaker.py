from flask import Flask, request, jsonify, render_template, send_from_directory
import threading
import yt_dlp
import os
from collections import deque

# Flask app
app = Flask(__name__)

# Shared in-memory data
queue = deque()  # The song queue
downloaded_songs = {}  # Cache for downloaded songs (key: URL, value: metadata)
votes = {}  # Voting dictionary (key: URL, value: votes)

# Lock for thread safety
queue_lock = threading.Lock()

# Function to download a song and fetch metadata
def download_song(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info).replace(info['ext'], 'mp3')
        metadata = {
            'title': info.get('title', 'Unknown Title'),
            'artist': info.get('uploader', 'Unknown Artist'),
            'duration': info.get('duration', 0),
            'url': url,
            'file_path': file_path
        }
        return metadata

# Route: Serve audio files
@app.route('/downloads/<path:filename>')
def serve_audio(filename):
    return send_from_directory('downloads', filename)

# Route: Homepage
@app.route('/')
def index():
    return render_template('index.html')  # Create an HTML file for the UI

# Route: Add song to queue
@app.route('/add', methods=['POST'])
def add_song():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Download and get metadata
    with queue_lock:
        if url not in downloaded_songs:
            metadata = download_song(url)
            downloaded_songs[url] = metadata
        else:
            metadata = downloaded_songs[url]

        queue.append(metadata)
        votes[url] = 0

    return jsonify({'message': 'Song added', 'metadata': metadata})

# Route: Get current queue
@app.route('/queue', methods=['GET'])
def get_queue():
    with queue_lock:
        queue_data = []
        for song in queue:
            if os.path.exists(song['file_path']):
                song_url = f"/downloads/{os.path.basename(song['file_path'])}"
            else:
                song_url = song['url']
            queue_data.append({**song, 'play_url': song_url})
        return jsonify(queue_data)

# Route: Vote for a song
@app.route('/vote', methods=['POST'])
def vote_song():
    data = request.json
    url = data.get('url')
    vote_type = data.get('vote')  # "up" or "down"

    if not url or vote_type not in ['up', 'down']:
        return jsonify({'error': 'Invalid vote'}), 400

    with queue_lock:
        if url in votes:
            votes[url] += 1 if vote_type == 'up' else -1
            return jsonify({'message': 'Vote recorded', 'votes': votes[url]})
        else:
            return jsonify({'error': 'Song not found'}), 404

# Run Flask app
if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
