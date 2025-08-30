document.addEventListener('DOMContentLoaded', () => {
    console.log('YouTube Music App Initialized');

    const mainContent = document.getElementById('main-content');
    const API_BASE_URL = 'http://localhost:8000';

    async function fetchCharts() {
        try {
            const response = await fetch(`${API_BASE_URL}/youtubemusic/charts`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data.results;
        } catch (error) {
            console.error('Error fetching charts:', error);
            return null;
        }
    }

    function renderCharts(charts) {
        if (!charts) {
            mainContent.innerHTML = '<h1>Error loading charts</h1>';
            return;
        }

        let html = '<h1>Top Charts</h1><div class="charts-grid">';

        if(charts.videos && charts.videos.items) {
            html += '<h2>Top Videos</h2>';
            charts.videos.items.forEach(item => {
                html += `
                    <a href="#song/${item.videoId}" class="chart-item">
                        <img src="${item.thumbnails[0].url}" alt="${item.title}">
                        <h3>${item.title}</h3>
                        <p>${item.artists.map(a => a.name).join(', ')}</p>
                    </a>
                `;
            });
        }

        html += '</div>';
        mainContent.innerHTML = html;
    }

    function navigate() {
        const hash = window.location.hash || '#home';
        loadContent(hash);
    }

    async function loadContent(hash) {
        if (hash === '#home' || hash === '#charts') {
            mainContent.innerHTML = '<h1>Loading Charts...</h1>';
            const charts = await fetchCharts();
            renderCharts(charts);
        } else {
            mainContent.innerHTML = `<h1>${hash.substring(1)} Page</h1><p>Content for ${hash.substring(1)} page will be loaded here.</p>`;
        }
    }

    async function fetchSearch(query) {
        try {
            const response = await fetch(`${API_BASE_URL}/youtubemusic/search?q=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data.results;
        } catch (error) {
            console.error('Error fetching search results:', error);
            return null;
        }
    }

    function renderSearchResults(results) {
        if (!results) {
            mainContent.innerHTML = '<h1>Error loading search results</h1>';
            return;
        }

        let html = '<h1>Search Results</h1><div class="search-results-grid">';

        results.forEach(item => {
            let link = '#';
            if (item.resultType === 'song') {
                link = `#song/${item.videoId}`;
            } else if (item.resultType === 'album') {
                link = `#album/${item.browseId}`;
            } else if (item.resultType === 'artist') {
                link = `#artist/${item.browseId}`;
            }
            html += `
                <a href="${link}" class="search-result-item">
                    <img src="${item.thumbnails[0].url}" alt="${item.title}">
                    <h3>${item.title}</h3>
                    <p>${item.artists ? item.artists.map(a => a.name).join(', ') : item.resultType}</p>
                </a>
            `;
        });

        html += '</div>';
        mainContent.innerHTML = html;
    }

    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');

    searchButton.addEventListener('click', async () => {
        const query = searchInput.value;
        if (query) {
            window.location.hash = `#search?q=${encodeURIComponent(query)}`;
        }
    });

    searchInput.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value;
            if (query) {
                window.location.hash = `#search?q=${encodeURIComponent(query)}`;
            }
        }
    });

    const audioPlayer = document.getElementById('audio-player');
    const playPauseButton = document.getElementById('play-pause-button');
    const progressBar = document.getElementById('progress-bar');
    const volumeSlider = document.getElementById('volume-slider');

    playPauseButton.addEventListener('click', () => {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playPauseButton.textContent = '⏸️';
        } else {
            audioPlayer.pause();
            playPauseButton.textContent = '▶️';
        }
    });

    audioPlayer.addEventListener('timeupdate', () => {
        progressBar.value = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    });

    progressBar.addEventListener('input', () => {
        audioPlayer.currentTime = (progressBar.value / 100) * audioPlayer.duration;
    });

    volumeSlider.addEventListener('input', () => {
        audioPlayer.volume = volumeSlider.value;
    });


    window.addEventListener('hashchange', navigate);
    navigate(); // Load initial content

    async function fetchSong(videoId) {
        try {
            const response = await fetch(`${API_BASE_URL}/youtubemusic/song/${videoId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching song:', error);
            return null;
        }
    }

    function renderSong(song) {
        if (!song) {
            mainContent.innerHTML = '<h1>Error loading song</h1>';
            return;
        }

        const audioPlayer = document.getElementById('audio-player');
        const audioSource = song.streamingData.formats.find(f => f.mimeType.startsWith('audio'));
        if (audioSource) {
            audioPlayer.src = audioSource.url;
            audioPlayer.play();
        }


        let html = `
            <div class="song-details">
                <img src="${song.videoDetails.thumbnail.thumbnails.pop().url}" alt="${song.videoDetails.title}">
                <h1>${song.videoDetails.title}</h1>
                <h2>${song.videoDetails.author}</h2>
            </div>
        `;
        mainContent.innerHTML = html;
    }

    async function fetchAlbum(browseId) {
        try {
            const response = await fetch(`${API_BASE_URL}/youtubemusic/album/${browseId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching album:', error);
            return null;
        }
    }

    function renderAlbum(album) {
        if (!album) {
            mainContent.innerHTML = '<h1>Error loading album</h1>';
            return;
        }

        let html = `
            <div class="album-details">
                <img src="${album.thumbnails.pop().url}" alt="${album.title}">
                <h1>${album.title}</h1>
                <h2>${album.artists.map(a => a.name).join(', ')}</h2>
                <div class="track-list">
                    ${album.tracks.map(track => `
                        <a href="#song/${track.videoId}" class="track-item">
                            <p>${track.title}</p>
                            <p>${track.duration}</p>
                        </a>
                    `).join('')}
                </div>
            </div>
        `;
        mainContent.innerHTML = html;
    }

    async function fetchArtist(artistId) {
        try {
            const response = await fetch(`${API_BASE_URL}/youtubemusic/artist/${artistId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching artist:', error);
            return null;
        }
    }

    function renderArtist(artist) {
        if (!artist) {
            mainContent.innerHTML = '<h1>Error loading artist</h1>';
            return;
        }

        let html = `
            <div class="artist-details">
                <img src="${artist.thumbnails.pop().url}" alt="${artist.name}">
                <h1>${artist.name}</h1>
                <p>${artist.description}</p>
            </div>
        `;
        mainContent.innerHTML = html;
    }

    async function loadContent(hash) {
        const [page, ...rest] = hash.substring(1).split('/');
        const id = rest.join('/');

        if (page === 'home' || page === 'charts' || page === '') {
            mainContent.innerHTML = '<h1>Loading Charts...</h1>';
            const charts = await fetchCharts();
            renderCharts(charts);
        } else if (page === 'search') {
            const queryParams = new URLSearchParams(id);
            const query = queryParams.get('q');
            mainContent.innerHTML = `<h1>Searching for "${decodeURIComponent(query)}"...</h1>`;
            const results = await fetchSearch(decodeURIComponent(query));
            renderSearchResults(results);
        } else if (page === 'song' && id) {
            mainContent.innerHTML = '<h1>Loading song...</h1>';
            const song = await fetchSong(id);
            renderSong(song);
        } else if (page === 'album' && id) {
            mainContent.innerHTML = '<h1>Loading album...</h1>';
            const album = await fetchAlbum(id);
            renderAlbum(album);
        } else if (page === 'artist' && id) {
            mainContent.innerHTML = '<h1>Loading artist...</h1>';
            const artist = await fetchArtist(id);
            renderArtist(artist);
        } else {
            mainContent.innerHTML = `<h1>${page} Page</h1><p>Content for ${page} page will be loaded here.</p>`;
        }
    }
});
