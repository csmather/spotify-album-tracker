let allAlbums = [];
let currentFilter = 'all';

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

function displayAlbums() {
    const grid = document.getElementById('albums-grid');
    
    let filteredAlbums = allAlbums;
    
    if (currentFilter === 'listened') {
        filteredAlbums = allAlbums.filter(a => a.listened);
    } else if (currentFilter === 'unlistened') {
        filteredAlbums = allAlbums.filter(a => !a.listened);
    }
    
    grid.innerHTML = filteredAlbums.map(album => `
        <div class="album-card">
            <img class="album-image" src="${album.image_url}" alt="${album.name}">
            <div class="album-name">${album.name}</div>
            <div class="album-artist">${album.artist}</div>
            <div class="album-status">
                <span class="status-badge ${album.listened ? 'status-listened' : 'status-unlistened'}">
                    ${album.listened ? 'Listened' : 'Not Listened'}
                </span>
                ${album.rating ? `<span class="rating">${'★'.repeat(album.rating)}</span>` : ''}
            </div>
        </div>
    `).join('');
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

// Load albums on page load
loadAlbums();