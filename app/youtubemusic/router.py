from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from .services import (
    youtube_music_search_service,
    get_song_service,
    get_album_service,
    get_artist_service,
    get_lyrics_service,
    get_charts_service,
    YouTubeMusicSearchError,
)

router = APIRouter()


@router.get("/search", response_model=Dict[str, Any])
async def search_youtube_music(
    q: str = Query(..., description="The search query string."),
):
    """
    Performs a YouTube Music search and returns a list of results.
    """
    try:
        results = youtube_music_search_service(query=q)
        return {"results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except YouTubeMusicSearchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@router.get("/song/{video_id}", response_model=Dict[str, Any])
async def get_song(video_id: str):
    """
    Gets song details from YouTube Music.
    """
    try:
        song = get_song_service(video_id=video_id)
        return song
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except YouTubeMusicSearchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@router.get("/album/{browse_id}", response_model=Dict[str, Any])
async def get_album(browse_id: str):
    """
    Gets album details from YouTube Music.
    """
    try:
        album = get_album_service(browse_id=browse_id)
        return album
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except YouTubeMusicSearchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@router.get("/artist/{artist_id}", response_model=Dict[str, Any])
async def get_artist(artist_id: str):
    """
    Gets artist details from YouTube Music.
    """
    try:
        artist = get_artist_service(artist_id=artist_id)
        return artist
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except YouTubeMusicSearchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@router.get("/lyrics/{video_id}", response_model=Dict[str, Any])
async def get_lyrics(video_id: str):
    """
    Gets lyrics for a song from YouTube Music.
    """
    try:
        lyrics = get_lyrics_service(video_id=video_id)
        return lyrics
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except YouTubeMusicSearchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@router.get("/charts", response_model=List[Dict[str, Any]])
async def get_charts():
    """
    Gets the top charts from YouTube Music.
    """
    try:
        charts = get_charts_service()
        return charts
    except YouTubeMusicSearchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
