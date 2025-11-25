import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time
from album_database import load_albums, save_albums
from datetime import datetime

load_dotenv()

class PlaybackTracker:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            scope="user-library-read user-read-currently-playing user-read-playback-state"
        ))
        
        self.current_album_id = None
        self.tracks_played = set()  # Track URIs we've heard
        self.albums_db = load_albums()
        self.completed_albums = set()  # Track albums we've already prompted for this session
    
    def get_current_playback(self):
        """Get what's currently playing"""
        try:
            playback = self.sp.current_playback()
            if playback and playback['is_playing']:
                return playback
            return None
        except Exception as e:
            print(f"Error getting playback: {e}")
            return None
    
    def check_if_album_complete(self, album_id):
        """Check if we've played enough of the album to mark it listened"""
        if album_id not in self.albums_db:
            return False
        
        album_data = self.albums_db[album_id]
        total_tracks = album_data['total_tracks']
        tracks_heard = len(self.tracks_played)
        
        # Consider album complete if we've heard 75% of tracks
        percentage = tracks_heard / total_tracks
        return percentage >= 0.75
    
    def mark_album_listened(self, album_id):
        """Mark an album as listened and prompt for rating"""
        # Reload albums in case they were updated elsewhere
        self.albums_db = load_albums()
        album_data = self.albums_db[album_id]
        
        print(f"\n{'='*60}")
        print(f"🎵 Album Complete: {album_data['name']}")
        print(f"   Artist: {album_data['artist']}")
        print(f"{'='*60}")
        
        # Prompt for rating
        while True:
            rating_input = input("Rate this album (1-5 stars, or 0 to skip): ").strip()
            try:
                rating = int(rating_input)
                if 0 <= rating <= 5:
                    break
                print("Please enter a number between 0 and 5")
            except ValueError:
                print("Please enter a valid number")
        
        # Update database
        self.albums_db[album_id]['listened'] = True
        self.albums_db[album_id]['date_listened'] = datetime.now().isoformat()
        
        if rating > 0:
            self.albums_db[album_id]['rating'] = rating
            print(f"✓ Marked as listened with {rating} stars!")
        else:
            self.albums_db[album_id]['rating'] = None
            print(f"✓ Marked as listened (no rating)")
        
        save_albums(self.albums_db)
        
        # Mark this album as completed for this session
        self.completed_albums.add(album_id)
        
        print("Continuing to track playback...\n")
    
    def run(self):
        """Main tracking loop"""
        print("🎧 Playback Tracker Started")
        print("Listening for Spotify playback...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                playback = self.get_current_playback()
                
                if playback:
                    item = playback['item']
                    if item['type'] == 'track':
                        track_uri = item['uri']
                        album = item['album']
                        album_id = album['id']
                        
                        # Check if this is a saved album
                        if album_id in self.albums_db:
                            album_data = self.albums_db[album_id]
                            
                            # If we switched to a different album, check if previous was complete
                            if self.current_album_id and self.current_album_id != album_id:
                                if (not self.albums_db[self.current_album_id]['listened'] and 
                                    self.current_album_id not in self.completed_albums):
                                    if self.check_if_album_complete(self.current_album_id):
                                        self.mark_album_listened(self.current_album_id)
                                
                                # Reset for new album
                                self.tracks_played = set()
                            
                            # Update current album
                            self.current_album_id = album_id
                            self.tracks_played.add(track_uri)
                            
                            # Show what's playing
                            progress = len(self.tracks_played)
                            total = album_data['total_tracks']
                            print(f"▶ {item['name']} - {album['name']} ({progress}/{total} tracks)    ", end='\r')
                            
                            # Check if album just completed
                            if (not album_data['listened'] and 
                                album_id not in self.completed_albums):
                                if self.check_if_album_complete(album_id):
                                    # Check if this is the last track
                                    track_number = item['track_number']
                                    if track_number == total:
                                        time.sleep(2)  # Wait a moment to let track finish
                                        self.mark_album_listened(album_id)
                                        self.tracks_played = set()
                else:
                    print("⏸ No playback detected    ", end='\r')
                
                time.sleep(10)  # Check every 10 seconds
                
        except KeyboardInterrupt:
            print("\n\n✓ Tracker stopped")

if __name__ == '__main__':
    tracker = PlaybackTracker()
    tracker.run()