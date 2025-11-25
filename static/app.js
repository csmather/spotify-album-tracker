let allAlbums = [];
let currentFilter = 'all';
let currentSort = 'added-newest'; // Default to newest added

async function loadAlbums() {
    const response = await fetch('/api/albums');
    const data = await response.json();
    
    allAlbums = data.albums;
    
    // Update stats
    document.getElementById('total-albums').textContent = data.total;
    document.getElementById('listened-albums').textContent = data.listened;
    document.getElementById('unlistened-albums').textContent = data.unlistened;
    
    displayAlbums();
}

function sortAlbums(albums) {
    const sorted = [...albums];
    
    switch(currentSort) {
        case 'name':
            sorted.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'artist':
            sorted.sort((a, b) => a.artist.localeCompare(b.artist));
            break;
        case 'release-oldest':
            sorted.sort((a, b) => {
                if (!a.release_date) return 1;
                if (!b.release_date) return -1;
                return new Date(a.release_date) - new Date(b.release_date);
            });
            break;
        case 'release-newest':
            sorted.sort((a, b) => {
                if (!a.release_date) return 1;
                if (!b.release_date) return -1;
                return new Date(b.release_date) - new Date(a.release_date);
            });
            break;
        case 'added-oldest':
            sorted.sort((a, b) => {
                if (!a.added_at) return 1;
                if (!b.added_at) return -1;
                return new Date(a.added_at) - new Date(b.added_at);
            });
            break;
        case 'added-newest':
            sorted.sort((a, b) => {
                if (!a.added_at) return 1;
                if (!b.added_at) return -1;
                return new Date(b.added_at) - new Date(a.added_at);
            });
            break;
    }
    
    return sorted;
}

function displayAlbums() {
    const grid = document.getElementById('albums-grid');
    
    let filteredAlbums = allAlbums;
    
    if (currentFilter === 'listened') {
        filteredAlbums = allAlbums.filter(a => a.listened);
    } else if (currentFilter === 'unlistened') {
        filteredAlbums = allAlbums.filter(a => !a.listened);
    }
    
    const sortedAlbums = sortAlbums(filteredAlbums);
    
    grid.innerHTML = sortedAlbums.map(album => `
        <div class="album-card" data-album-id="${album.id}">
            <img class="album-image" src="${album.image_url}" alt="${album.name}">
            <div class="album-name">${album.name}</div>
            <div class="album-artist">${album.artist}</div>
            <div class="album-status">
                <span class="status-badge ${album.listened ? 'status-listened' : 'status-unlistened'}">
                    ${album.listened ? 'Listened' : 'Not Listened'}
                </span>
                ${album.rating ? `<span class="rating">${'★'.repeat(album.rating)}</span>` : ''}
            </div>
            ${album.listened && !album.rating ? `
                <div class="rating-selector">
                    ${[1, 2, 3, 4, 5].map(star => 
                        `<button class="star-btn" onclick="rateAlbum('${album.id}', ${star}, event)">★</button>`
                    ).join('')}
                </div>
            ` : ''}
            <button class="mark-listened-btn" onclick="toggleListened('${album.id}', event)">
                ${album.listened ? 'Mark Unlistened' : 'Mark Listened'}
            </button>
        </div>
    `).join('');
}

async function rateAlbum(albumId, rating, event) {
    event.stopPropagation();
    
    const response = await fetch('/api/rate-album', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ album_id: albumId, rating: rating })
    });
    
    if (response.ok) {
        await loadAlbums();
    }
}

async function toggleListened(albumId, event) {
    event.stopPropagation();
    
    const response = await fetch('/api/toggle-listened', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ album_id: albumId })
    });
    
    if (response.ok) {
        // Reload albums to get updated data
        await loadAlbums();
    }
}

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        displayAlbums();
    });
});

// Sort dropdown
document.getElementById('sort-select').addEventListener('change', (e) => {
    currentSort = e.target.value;
    displayAlbums();
});

// Sync Spotify Library button
document.getElementById('sync-spotify-btn').addEventListener('click', async () => {
    const btn = document.getElementById('sync-spotify-btn');
    btn.disabled = true;
    btn.textContent = 'Syncing...';
    
    try {
        const response = await fetch('/api/sync-spotify', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`Sync complete! Library now has ${data.total} albums.`);
            await loadAlbums();
        } else {
            alert(`Sync failed: ${data.error}`);
        }
    } catch (error) {
        alert('Sync failed: ' + error.message);
    }
    
    btn.disabled = false;
    btn.textContent = 'Sync Spotify Library';
});

// Load albums on page load
loadAlbums();