document.addEventListener('DOMContentLoaded', () => {
    console.log('YouTube Music App Initialized');

    const mainContent = document.getElementById('main-content');
    const API_BASE_URL = 'https://swipeapis.vercel.app';

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

        let html = '<h1>Listen Now</h1>';

        if(charts.videos && charts.videos.items) {
            html += '<div class="charts-grid">';
            charts.videos.items.forEach(item => {
                html += `
                    <a href="#song/${item.videoId}" class="chart-item">
                        <img src="${item.thumbnails.pop().url}" alt="${item.title}">
                        <h3>${item.title}</h3>
                        <p>${item.artists.map(a => a.name).join(', ')}</p>
                    </a>
                `;
            });
            html += '</div>';
        }

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

        const songs = results.filter(item => item.resultType === 'song');
        const albums = results.filter(item => item.resultType === 'album');
        const artists = results.filter(item => item.resultType === 'artist');

        let html = '<h1>Search Results</h1>';

        if (songs.length > 0) {
            html += '<h2>Songs</h2><div class="charts-grid">';
            songs.forEach(item => {
                html += `
                    <a href="#song/${item.videoId}" class="chart-item">
                        <img src="${item.thumbnails.pop().url}" alt="${item.title}">
                        <h3>${item.title}</h3>
                        <p>${item.artists.map(a => a.name).join(', ')}</p>
                    </a>
                `;
            });
            html += '</div>';
        }

        if (albums.length > 0) {
            html += '<h2>Albums</h2><div class="charts-grid">';
            albums.forEach(item => {
                html += `
                    <a href="#album/${item.browseId}" class="chart-item">
                        <img src="${item.thumbnails.pop().url}" alt="${item.title}">
                        <h3>${item.title}</h3>
                        <p>${item.artists.map(a => a.name).join(', ')}</p>
                    </a>
                `;
            });
            html += '</div>';
        }

        if (artists.length > 0) {
            html += '<h2>Artists</h2><div class="charts-grid">';
            artists.forEach(item => {
                html += `
                    <a href="#artist/${item.browseId}" class="chart-item">
                        <img src="${item.thumbnails.pop().url}" alt="${item.title}">
                        <h3>${item.title}</h3>
                        <p>Artist</p>
                    </a>
                `;
            });
            html += '</div>';
        }

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
            playPauseButton.textContent = '⏸️';
        }

        const backgroundArt = song.videoDetails.thumbnail.thumbnails.pop().url;
        mainContent.style.backgroundImage = `url(${backgroundArt})`;

        document.getElementById('footer-thumb').src = backgroundArt;
        document.getElementById('footer-title').textContent = song.videoDetails.title;
        document.getElementById('footer-artist').textContent = song.videoDetails.author;


        let html = `
            <div class="song-details-container">
                <div class="song-details">
                    <img src="${backgroundArt}" alt="${song.videoDetails.title}">
                    <h1>${song.videoDetails.title}</h1>
                    <h2>${song.videoDetails.author}</h2>
                </div>
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

        const backgroundArt = album.thumbnails.pop().url;
        mainContent.style.backgroundImage = `url(${backgroundArt})`;

        let html = `
            <div class="album-details-container">
                <div class="album-header">
                    <img src="${backgroundArt}" alt="${album.title}">
                    <div class="album-info">
                        <h1>${album.title}</h1>
                        <h2>${album.artists.map(a => a.name).join(', ')}</h2>
                        <p>${album.year} · ${album.trackCount} songs</p>
                    </div>
                </div>
                <div class="track-list">
                    ${album.tracks.map(track => `
                        <a href="#song/${track.videoId}" class="track-item">
                            <p class="track-number">${track.trackNumber}</p>
                            <p class="track-title">${track.title}</p>
                            <p class="track-duration">${track.duration}</p>
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

        const backgroundArt = artist.thumbnails.pop().url;
        mainContent.style.backgroundImage = `url(${backgroundArt})`;

        let html = `
            <div class="artist-details-container">
                <div class="artist-header">
                    <img src="${backgroundArt}" alt="${artist.name}">
                    <h1>${artist.name}</h1>
                </div>
                <div class="artist-section">
                    <h2>Top Songs</h2>
                    <div class="track-list">
                        ${artist.songs.results.map(track => `
                            <a href="#song/${track.videoId}" class="track-item">
                                <img src="${track.thumbnails.pop().url}" class="track-thumbnail">
                                <p class="track-title">${track.title}</p>
                                <p class="track-duration">${track.duration}</p>
                            </a>
                        `).join('')}
                    </div>
                </div>
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
