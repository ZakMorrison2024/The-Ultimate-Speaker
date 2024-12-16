# The-Ultimate-Speaker

# Party Speaker Setup and Usage Instructions

## Overview
This project is a local network-based party speaker application allowing users to:
1. Add songs to a queue from YouTube or Spotify URLs (no API keys required).
2. Play audio directly in the browser.
3. Vote songs up or down in the queue.
4. Automatically download and save songs for offline playback.

The system uses Flask for the backend and a browser-based UI to control playback.

---

## Features
- Embedded video/audio player.
- Voting functionality to prioritize songs in the queue.
- Local caching of downloaded songs to reduce redundant downloads.
- Works over WiFi, enabling multiple users to connect via their browsers.

---
## Personal
 
- This is a project I've been planning for some time, a "Party" speaker anyone can connect too and share music without restriction.
- My build will be a Raspberry Pi dedicated to this purpose, with housing made from my 3D Printer.


## Requirements

### Software Dependencies
1. Python 3.8+
2. Required Python packages:
   - Flask==2.2.5
   - yt-dlp==2024.3.11

Install these packages using pip:
```sh
pip install Flask yt-dlp
```

### Hardware Requirements
1. A Raspberry Pi with:
   - Internet access for downloading music.
   - Speakers connected for audio playback.
2. Devices (phones, laptops, etc.) connected to the same WiFi network to control the speaker.

---

## Setup Instructions


### 1. Install Python Dependencies
Ensure you have Python installed. Install the required packages:
```
pip install Flask yt-dlp
```

### 2. Run the Application
Start the Flask server by running the script:
```
python speaker.py
```

### 3. Access the Application
On the device running the script, note the IP address (e.g., `192.168.0.10`). On any device connected to the same WiFi network, open a browser and navigate to: (I Recommend putting a QR code over build to localhost:5000)
```
http://localhost:5000
```

Example:
```
http://localhost:5000
```

---

## How to Use

### Adding Songs
1. Enter a YouTube or Spotify URL in the text input field.
2. Click the "Add" button.
3. The song will be added to the queue and downloaded if not already cached.

### Voting
- Use the "Upvote" or "Downvote" buttons next to a song to prioritize or deprioritize it.

### Playback
- The first song in the queue will auto-play when added.
- Skipping a song will automatically play the next in the queue.

---

## Advanced Features
### Offline Playback
All downloaded songs are saved locally in the `downloads` folder. The app will check if a song is already downloaded before attempting to fetch it online.

### WiFi Connectivity
Ensure all users are connected to the same WiFi network as the host machine to control the speaker via their browsers.

---

## Troubleshooting
### Common Issues
1. **Server not accessible:** Check if the Flask server is running and ensure the IP address is correct.
2. **Playback issues:** Ensure the browser supports audio playback for the downloaded format (MP3).

For further assistance, open an issue on the project's GitHub page.
