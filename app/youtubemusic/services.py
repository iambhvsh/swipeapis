from ytmusicapi import YTMusic
from typing import List, Dict, Any

class YouTubeMusicSearchError(Exception):
    """Custom exception for errors during a YouTube Music search."""
    pass

def youtube_music_search_service(query: str) -> List[Dict[str, Any]]:
    """
    Service to search for music on YouTube Music.
    """
    if not query:
        raise ValueError("Search query cannot be empty.")

    try:
        ytmusic = YTMusic()
        search_results = ytmusic.search(query)
        return search_results
    except Exception as e:
        raise YouTubeMusicSearchError(f"Error fetching YouTube Music search results: {e}")

def get_song_service(video_id: str) -> Dict[str, Any]:
    """
    Service to get song details from YouTube Music.
    """
    if not video_id:
        raise ValueError("Video ID cannot be empty.")

    try:
        ytmusic = YTMusic()
        song = ytmusic.get_song(video_id)
        return song
    except Exception as e:
        raise YouTubeMusicSearchError(f"Error fetching song details: {e}")

def get_album_service(browse_id: str) -> Dict[str, Any]:
    """
    Service to get album details from YouTube Music.
    """
    if not browse_id:
        raise ValueError("Browse ID cannot be empty.")

    try:
        ytmusic = YTMusic()
        album = ytmusic.get_album(browse_id)
        return album
    except Exception as e:
        raise YouTubeMusicSearchError(f"Error fetching album details: {e}")

def get_artist_service(artist_id: str) -> Dict[str, Any]:
    """
    Service to get artist details from YouTube Music.
    """
    if not artist_id:
        raise ValueError("Artist ID cannot be empty.")

    try:
        ytmusic = YTMusic()
        artist = ytmusic.get_artist(artist_id)
        return artist
    except Exception as e:
        raise YouTubeMusicSearchError(f"Error fetching artist details: {e}")

def get_lyrics_service(video_id: str) -> Dict[str, Any]:
    """
    Service to get lyrics for a song from YouTube Music.
    """
    if not video_id:
        raise ValueError("Video ID cannot be empty.")

    try:
        ytmusic = YTMusic()
        watch_playlist = ytmusic.get_watch_playlist(video_id)
        if 'lyrics' not in watch_playlist:
            raise YouTubeMusicSearchError("No lyrics found for this song.")
        lyrics_browse_id = watch_playlist['lyrics']
        lyrics = ytmusic.get_lyrics(lyrics_browse_id)
        return lyrics
    except Exception as e:
        raise YouTubeMusicSearchError(f"Error fetching lyrics: {e}")

def get_charts_service() -> Dict[str, Any]:
    """
    Service to get the top charts from YouTube Music.
    """
    try:
        ytmusic = YTMusic()
        charts = ytmusic.get_charts()
        return charts
    except Exception as e:
        raise YouTubeMusicSearchError(f"Error fetching charts: {e}")
