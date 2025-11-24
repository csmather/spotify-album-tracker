import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from album_database import sync_spotify_library, load_albums

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="user-library-read user-read-currently-playing user-read-playback-state"
))

# Sync your library
print("Syncing Spotify library...")
albums = sync_spotify_library(sp)

# Show some stats
unlistened = [a for a in albums.values() if not a['listened']]
print(f"\nTotal albums: {len(albums)}")
print(f"Unlistened: {len(unlistened)}")