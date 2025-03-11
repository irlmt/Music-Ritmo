import pytest
from unittest.mock import patch, MagicMock
from fastapi.responses import JSONResponse
import src.app.open_subsonic_api as api
from src.app.database import Session
from src.app.service_layer import ArtistService, AlbumService, PlaylistService
from src.app.dto import Artist, Album, Playlist
import src.app.database as db


@pytest.fixture
def session_mock():
    return MagicMock(spec=Session)


@pytest.fixture
def user_mock():
    user = MagicMock(spec=db.User)
    user.login = "testuser"
    user.playlists = [MagicMock(id=1)]
    return user


@patch("src.app.service_layer.ArtistService.get_artist_by_id")
def test_get_artist_success(mock_get_artist, session_mock):
    mock_get_artist.return_value = Artist(id=1, name="Test Artist")
    result = api.get_artist(id=1, session=session_mock)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 200


@patch("src.app.service_layer.ArtistService.get_artist_by_id")
def test_get_artist_not_found(mock_get_artist, session_mock):
    mock_get_artist.return_value = None
    result = api.get_artist(id=999, session=session_mock)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404


@patch("src.app.service_layer.AlbumService.get_album_by_id")
def test_get_album_not_found(mock_get_album, session_mock):
    mock_get_album.return_value = None
    result = api.get_album(id=999, session=session_mock)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404


@patch("src.app.service_layer.PlaylistService.get_playlist")
def test_get_playlist_not_found(mock_get_playlist, session_mock):
    mock_get_playlist.return_value = None
    result = api.get_playlist(id=999, session=session_mock)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404


@patch("src.app.service_layer.PlaylistService.delete_playlist")
def test_delete_playlist_success(mock_delete_playlist, session_mock, user_mock):
    result = api.delete_playlist(id=1, current_user=user_mock, session=session_mock)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 200


@patch("src.app.service_layer.PlaylistService.delete_playlist")
def test_delete_playlist_forbidden(mock_delete_playlist, session_mock, user_mock):
    user_mock.playlists = []
    result = api.delete_playlist(id=2, current_user=user_mock, session=session_mock)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403


@patch("src.app.service_layer.PlaylistService.update_playlist")
def test_update_playlist_success(mock_update_playlist, session_mock, user_mock):
    mock_update_playlist.return_value = True
    result = api.update_playlist(
        playlistId=1,
        name="Updated",
        songIdToAdd=[3],
        songIdToRemove=[],
        current_user=user_mock,
        session=session_mock,
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 200


@patch("src.app.service_layer.PlaylistService.update_playlist")
def test_update_playlist_not_found(mock_update_playlist, session_mock, user_mock):
    mock_update_playlist.return_value = False
    result = api.update_playlist(
        playlistId=1,
        name="Updated",
        songIdToAdd=[3],
        songIdToRemove=[],
        current_user=user_mock,
        session=session_mock,
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404


@patch("src.app.service_layer.PlaylistService.update_playlist")
def test_update_playlist_forbidden(mock_update_playlist, session_mock, user_mock):
    user_mock.playlists = []
    result = api.update_playlist(
        playlistId=2,
        name="Updated",
        songIdToAdd=[3],
        songIdToRemove=[],
        current_user=user_mock,
        session=session_mock,
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403
