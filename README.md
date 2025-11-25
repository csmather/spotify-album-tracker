# Spotify Album Tracker

A personal web app to track and rate albums from your Spotify library. Automatically detects when you finish listening to albums and prompts you to rate them.

## Features

- Syncs your entire Spotify saved album library
- Real-time playback tracking - automatically detects when you finish albums
- Rate albums 1-5 stars
- Filter by listened/unlistened status
- Sort by album name, artist, release date, or date added
- Manual album marking with rating support
- All data stored locally

## Setup

### Prerequisites

- Python 3.8+
- A Spotify account
- A Spotify Developer account

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/spotify-album-tracker.git
cd spotify-album-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Spotify API credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note your **Client ID** and **Client Secret**
4. In your app settings, add `http://127.0.0.1:8888/callback` as a Redirect URI

### 4. Configure environment variables

Create a `.env` file in the project root:
```
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

### 5. Initial library sync

Run the sync script to fetch your Spotify library:
```bash
python album_database.py
```

Or just start the web app and click "Sync Spotify Library".

## Usage

### Web Dashboard

Start the Flask web server:
```bash
python app.py
```

Open your browser to `http://localhost:5000`

From the dashboard you can:
- View all your saved albums
- Filter by listened/unlistened status
- Sort by various criteria
- Manually mark albums as listened
- Rate listened albums
- Sync new albums from Spotify

### Playback Tracker

To automatically track your listening and get prompted to rate albums when you finish them:
```bash
python playback_tracker.py
```

Keep this running while you listen to music on Spotify. When you complete an album, it will:
1. Detect that you've finished (or heard 75% of tracks)
2. Prompt you to rate it (1-5 stars)
3. Save the rating to your database
4. Update the web dashboard automatically

Press `Ctrl+C` to stop the tracker.

## Project Structure
```
spotify-album-tracker/
├── app.py                 # Flask web server
├── playback_tracker.py    # Real-time listening tracker
├── album_database.py      # Database management functions
├── albums_data.json       # Your album data (created on first sync)
├── .env                   # Your API credentials (not tracked in git)
├── templates/
│   └── index.html        # Web dashboard HTML
├── static/
│   ├── style.css         # Styling
│   └── app.js            # Frontend JavaScript
└── requirements.txt       # Python dependencies
```

## Technologies Used

- **Backend**: Python, Flask, Spotipy
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **APIs**: Spotify Web API
- **Data Storage**: JSON (local file)

## Features I'd Like to Add

- [ ] Listening statistics and charts
- [ ] Random album picker for backlog
- [ ] Export data to CSV
- [ ] Album notes/comments
- [ ] Tag/category system
- [ ] Listening history timeline

## License

MIT License - feel free to use this for your own Spotify library tracking!

## Contributing

This is a personal project, but suggestions and improvements are welcome! Open an issue or submit a pull request.