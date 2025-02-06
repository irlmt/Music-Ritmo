from datetime import datetime
from typing import List
from sqlmodel import Session, select
from sqlalchemy import func
from . import database as db


class ArtistDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_all_artists(self, filter_name=None):
        if filter_name:
            return self.session.exec(
                select(db.Artist).where(
                    func.lower(db.Artist.name).like(f"%{filter_name.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Artist)).all()

    def get_artist_by_id(self, id):
        return self.session.exec(
            select(db.Artist).where(db.Artist.id == id)
        ).one_or_none()


class AlbumDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_all_albums(self, filter_name=None):
        if filter_name:
            return self.session.exec(
                select(db.Album).where(
                    func.lower(db.Album.name).like(f"%{filter_name.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Album)).all()

    def get_album_by_id(self, id):
        return self.session.exec(
            select(db.Album).where(db.Album.id == id)
        ).one_or_none()


class TrackDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_all_tracks(self, filter_title=None):
        if filter_title:
            return self.session.exec(
                select(db.Track).where(
                    func.lower(db.Track.title).like(f"%{filter_title.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Track)).all()

    def get_track_by_id(self, id):
        return self.session.exec(
            select(db.Track).where(db.Track.id == id)
        ).one_or_none()

    def get_track_by_artist_id(self, artist_id):
        return self.session.exec(
            select(db.Track)
            .join(db.ArtistTrack)
            .where(db.ArtistTrack.artist_id == artist_id)
        ).all()


class GenresDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_genres_by_name(self, filter_name=None):
        if filter_name:
            return self.session.exec(
                select(db.Genre).where(func.lower(db.Genre.name) == filter_name.lower())
            ).all()
        return self.session.exec(select(db.Genre)).all()

    def get_all_genres(self, filter_name=None):
        if filter_name:
            return self.session.exec(
                select(db.Genre).where(
                    func.lower(db.Genre.name).like(f"%{filter_name.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Genre)).all()

    def get_track_by_name(self, name):
        return self.session.exec(
            select(db.Genre).where(db.Genre.name == name)
        ).one_or_none()


class FavouriteDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def star_track(self, id: int, user_id: int = 0):
        track = TrackDBHelper(self.session).get_track_by_id(id)

        if track:
            if (id, user_id) in [(t.track_id, t.user_id) for t in track.track_favourites]:
                return
            self.session.add(
                db.FavouriteTrack(
                    user_id=user_id, track_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_album(self, id: int, user_id: int = 0):
        album = AlbumDBHelper(self.session).get_album_by_id(id)
        if album:
            if (id, user_id) in [(a.album_id, a.user_id) for a in album.album_favourites]:
                return
            self.session.add(
                db.FavouriteAlbum(
                    user_id=user_id, album_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_artist(self, id: int, user_id: int = 0):
        artist = ArtistDBHelper(self.session).get_artist_by_id(id)
        if artist:
            if (id, user_id) in [(a.artist_id, a.user_id) for a in artist.artist_favourites]:
                return
            self.session.add(
                db.FavouriteArtist(
                    user_id=user_id, artist_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_playlist(self, id: int, user_id: int = 0):
        playlist = PlaylistDBHelper(self.session).get_playlist(id)
        if playlist:
            if (id, user_id) in [(a.playlist_id, a.user_id) for a in playlist.playlist_favourites]:
                return
            self.session.add(
                db.FavouritePlaylist(
                    user_id=user_id, playlist_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def unstar_track(self, id: int, user_id: int = 0):
        fav_track = self.session.exec(
            select(db.FavouriteTrack).where(
                (db.FavouriteTrack.track_id == id)
                & (db.FavouriteTrack.user_id == user_id)
            )
        ).one_or_none()
        if fav_track:
            self.session.delete(fav_track)
            self.session.commit()

    def unstar_album(self, id: int, user_id: int = 0):
        fav_album = self.session.exec(
            select(db.FavouriteAlbum).where(
                (db.FavouriteAlbum.album_id == id)
                & (db.FavouriteAlbum.user_id == user_id)
            )
        ).one_or_none()
        if fav_album:
            self.session.delete(fav_album)
            self.session.commit()

    def unstar_artist(self, id: int, user_id: int = 0):
        fav_artist = self.session.exec(
            select(db.FavouriteArtist).where(
                (db.FavouriteArtist.artist_id == id)
                & (db.FavouriteArtist.user_id == user_id)
            )
        ).one_or_none()
        if fav_artist:
            self.session.delete(fav_artist)
            self.session.commit()

    def unstar_playlist(self, id: int, user_id: int = 0):
        fav_playlist = self.session.exec(
            select(db.FavouritePlaylist).where(
                (db.FavouritePlaylist.playlist_id == id)
                & (db.FavouritePlaylist.user_id == user_id)
            )
        ).one_or_none()
        if fav_playlist:
            self.session.delete(fav_playlist)
            self.session.commit()

    def get_starred_tracks(self, user_id=0):
        return self.session.exec(
            select(db.Track).where(
                (
                    (db.FavouriteTrack.track_id == db.Track.id)
                    & (db.FavouriteTrack.user_id == user_id)
                )
            )
        ).all()

    def get_starred_artists(self, user_id=0):
        return self.session.exec(
            select(db.Artist).where(
                (
                    (db.FavouriteArtist.artist_id == db.Artist.id)
                    & (db.FavouriteArtist.user_id == user_id)
                )
            )
        ).all()

    def get_starred_albums(self, user_id=0):
        return self.session.exec(
            select(db.Album).where(
                (
                    (db.FavouriteAlbum.album_id == db.Album.id)
                    & (db.FavouriteAlbum.user_id == user_id)
                )
            )
        ).all()

    def get_starred_playlists(self, user_id=0):
        return self.session.exec(
            select(db.Playlist).where(
                (
                    (db.FavouritePlaylist.playlist_id == db.Playlist.id)
                    & (db.FavouritePlaylist.user_id == user_id)
                )
            )
        ).all()


class PlaylistDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def create_playlist(self, name, tracks: List[int], user_id=0):
        now = datetime.today()
        playlist = db.Playlist(
            name=name,
            # user_id=user_id,
            total_tracks=len(tracks),
            create_date=now,
        )
        for t in tracks:
            playlist_track = db.PlaylistTrack(
                playlist_id=playlist.id, track_id=t, added_at=now
            )
            playlist.playlist_tracks.append(playlist_track)
        self.session.add(playlist)
        self.session.commit()
        return playlist.id

    def update_playlist(
        self, id, name=None, traks_to_add=List[int], track_to_remove=List[int]
    ):
        now = datetime.today()
        playlist = self.session.exec(
            select(db.Playlist).where(db.Playlist.id == id)
        ).one_or_none()
        if playlist:
            if name:
                playlist.name = name
            for t in track_to_remove:
                playlist_track = self.session.exec(
                    select(db.PlaylistTrack).where(
                        (db.PlaylistTrack.track_id == t)
                        & (db.PlaylistTrack.playlist_id == playlist.id)
                    )
                ).one_or_none()
                if playlist_track:
                    playlist.playlist_tracks.remove(playlist_track)
                    # self.session.delete(playlist_track)
            for t in traks_to_add:
                playlist_track = db.PlaylistTrack(
                    added_at=now, track_id=t, playlist_id=id
                )
                playlist.playlist_tracks.append(playlist_track)
            playlist.total_tracks = len(playlist.playlist_tracks)
            self.session.commit()
        return playlist

    def delete_playlist(self, id):
        playlist = self.session.exec(
            select(db.Playlist).where(db.Playlist.id == id)
        ).one_or_none()
        if playlist:
            self.session.delete(playlist)
            self.session.commit()

    def get_playlist(self, id):
        return self.session.exec(
            select(db.Playlist).where(db.Playlist.id == id)
        ).one_or_none()

    def get_all_playlists(self):
        return self.session.exec(select(db.Playlist)).all()
