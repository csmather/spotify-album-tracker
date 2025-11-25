import json
import os

DATABASE_FILE = 'albums_data.json'

def load_albums():
    """Load albums from JSON file"""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_albums(albums_dict):
    """Save albums to JSON file"""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(albums_dict, f, indent=2, ensure_ascii=False)

def sync_spotify_library(sp):
    """Fetch all saved albums from Spotify and update database"""
    existing_albums = load_albums()
    
    albums = []
    results = sp.current_user_saved_albums(limit=50)
    
    while results:
        albums.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    
    # Update database with new albums
    for item in albums:
        album = item['album']
        album_id = album['id']
        added_at = item['added_at']  # Get the date you added it
        
        # Update or add album
        if album_id in existing_albums:
            # Update existing album but preserve user data
            existing_albums[album_id]['name'] = album['name']
            existing_albums[album_id]['artist'] = album['artists'][0]['name']
            existing_albums[album_id]['image_url'] = album['images'][0]['url'] if album['images'] else None
            existing_albums[album_id]['total_tracks'] = album['total_tracks']
            existing_albums[album_id]['release_date'] = album['release_date']
            existing_albums[album_id]['added_at'] = added_at  # Add this
            # Keep listened, rating, date_listened as they were
        else:
            # Add new album with default values
            existing_albums[album_id] = {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'image_url': album['images'][0]['url'] if album['images'] else None,
                'total_tracks': album['total_tracks'],
                'release_date': album['release_date'],
                'added_at': added_at,  # Add this
                'listened': False,
                'rating': None,
                'date_listened': None
            }
    
    save_albums(existing_albums)
    print(f"Synced {len(existing_albums)} albums to database")
    return existing_albums