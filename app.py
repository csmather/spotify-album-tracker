from flask import Flask, render_template, jsonify
from album_database import load_albums
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
    
    # Sort by name
    album_list.sort(key=lambda x: x['name'])
    
    return jsonify({
        'albums': album_list,
        'total': len(album_list),
        'listened': len([a for a in album_list if a['listened']]),
        'unlistened': len([a for a in album_list if not a['listened']])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)