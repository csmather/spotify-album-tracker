from flask import Flask, render_template, jsonify, request
from album_database import load_albums, save_albums
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/albums')
def get_albums():
    albums = load_albums()
    
    # Convert dict to list and add some stats
    album_list = []
    for album_id, data in albums.items():
        album_list.append({
            'id': album_id,
            **data
        })
    
    # Sort by name by default
    album_list.sort(key=lambda x: x['name'])
    
    return jsonify({
        'albums': album_list,
        'total': len(album_list),
        'listened': len([a for a in album_list if a['listened']]),
        'unlistened': len([a for a in album_list if not a['listened']])
    })

@app.route('/api/toggle-listened', methods=['POST'])
def toggle_listened():
    data = request.json
    album_id = data.get('album_id')
    
    albums = load_albums()
    
    if album_id in albums:
        # Toggle listened status
        albums[album_id]['listened'] = not albums[album_id]['listened']
        
        # If marking as listened, set the date
        if albums[album_id]['listened']:
            albums[album_id]['date_listened'] = datetime.now().isoformat()
        else:
            albums[album_id]['date_listened'] = None
            albums[album_id]['rating'] = None  # Clear rating if unmarking
        
        save_albums(albums)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Album not found'}), 404

@app.route('/api/rate-album', methods=['POST'])
def rate_album():
    data = request.json
    album_id = data.get('album_id')
    rating = data.get('rating')
    
    albums = load_albums()
    
    if album_id in albums:
        if 1 <= rating <= 5:
            albums[album_id]['rating'] = rating
            save_albums(albums)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Rating must be 1-5'}), 400
    
    return jsonify({'success': False, 'error': 'Album not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)