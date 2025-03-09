from datetime import datetime
from sqlalchemy import asc, desc, func
from sqlmodel import Session, select
from typing import List, Optional, Sequence

from . import database as db


class ArtistDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_all_artists(self, filter_name: str | None = None) -> Sequence[db.Artist]:
        query = select(db.Artist)
        if filter_name:
            query = query.where(
                func.lower(db.Artist.name).like(f"%{filter_name.lower()}%")
            )
        return self.session.exec(query).all()

    def get_artists(
        self, size: int, offset: int, filter_name: str | None = None
    ) -> Sequence[db.Artist]:
        query = select(db.Artist)
        if filter_name:
            query = query.where(
                func.lower(db.Artist.name).like(f"%{filter_name.lower()}%")
            )
        query = query.limit(size).offset(offset)
        return self.session.exec(query).all()

    def get_artist_by_id(self, id: int) -> db.Artist | None:
        return self.session.exec(
            select(db.Artist).where(db.Artist.id == id)
        ).one_or_none()


class AlbumDBHelper:
    def __init__(self, session: Session):
        self.session = session
        self.track_db_helper = TrackDBHelper(session)

    def get_all_albums(self, filter_name: str | None = None) -> Sequence[db.Album]:
        query = select(db.Album)
        if filter_name:
            query = query.where(
                func.lower(db.Album.name).like(f"%{filter_name.lower()}%")
            )
        return self.session.exec(query).all()

    def get_albums(
        self, size: int, offset: int, filter_name: str | None = None
    ) -> Sequence[db.Album]:
        query = select(db.Album)
        if filter_name:
            query = query.where(
                func.lower(db.Album.name).like(f"%{filter_name.lower()}%")
            )
        query = query.limit(size).offset(offset)
        return self.session.exec(query).all()

    def get_album_by_id(self, id: int) -> db.Album | None:
        return self.session.exec(
            select(db.Album).where(db.Album.id == id)
        ).one_or_none()

    def get_albums_by_name(self, size: int, offset: int) -> Sequence[db.Album]:
        return self.session.exec(
            select(db.Album).order_by(db.Album.name).limit(size).offset(offset)
        ).all()

    def get_first_track(self, albumId: int) -> db.Track | None:
        return self.session.exec(
            select(db.Track)
            .where(db.Track.album_id == albumId)
            .order_by(db.Track.album_position)  # type: ignore
            .limit(1)
        ).one_or_none()

    def get_album_artist(self, albumId: int) -> db.Artist | None:
        track = self.get_first_track(albumId)
        return self.track_db_helper.get_album_artist(track.id) if track else None

    def get_sorted_artist_albums(
        self, artist_id: int, size: int, offset: int
    ) -> Sequence[db.Album]:
        return self.session.exec(
            select(db.Album)
            .join(db.ArtistAlbum)
            .where(db.ArtistAlbum.album_id == db.Album.id)
            .where(db.ArtistAlbum.artist_id == artist_id)
            .distinct()
            .order_by(desc(db.Album.year), db.Album.name)  # type: ignore
            .limit(size)
            .offset(offset)
        ).all()

    def get_sorted_by_year_albums(
        self,
        min_year: str,
        max_year: str,
        size: int,
        offset: int,
        reversed_order: bool = False,
    ) -> Sequence[db.Album]:
        order = asc if not reversed_order else desc
        return self.session.exec(
            select(db.Album)
            .where(db.Album.year >= min_year)  # type: ignore
            .where(db.Album.year <= max_year)  # type: ignore
            .order_by(order(db.Album.year))  # type: ignore
            .order_by(db.Album.name)
            .limit(size)
            .offset(offset)
        ).all()

    def get_albums_by_genre(
        self, genre: str, size: int, offset: int
    ) -> Sequence[db.Album]:
        return self.session.exec(
            select(db.Album)
            .distinct()
            .join(db.Track, db.Track.album_id == db.Album.id)  # type: ignore
            .join(db.GenreTrack, db.GenreTrack.track_id == db.Track.id)  # type: ignore
            .join(db.Genre, db.Genre.id == db.GenreTrack.genre_id)  # type: ignore
            .where(func.lower(db.Genre.name).like(genre))
            .order_by(db.Album.name)
            .limit(size)
            .offset(offset)
        ).all()

    def get_sorted_albums_by_frequency(
        self, size: int, offset: int
    ) -> Sequence[db.Album]:
        return self.session.exec(
            select(db.Album)
            .order_by(desc(db.Album.play_count))  # type: ignore
            .order_by(db.Album.name)
            .limit(size)
            .offset(offset)
        ).all()


class TrackDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_all_tracks(self, filter_title: str | None = None) -> Sequence[db.Track]:
        query = select(db.Track)
        if filter_title:
            query = query.where(
                func.lower(db.Track.title).like(f"%{filter_title.lower()}%")
            )
        return self.session.exec(query).all()

    def get_tracks(
        self, size: int, offset: int, filter_title: str | None = None
    ) -> Sequence[db.Track]:
        query = select(db.Track)
        if filter_title:
            query = query.where(
                func.lower(db.Track.title).like(f"%{filter_title.lower()}%")
            )
        query = query.limit(size).offset(offset)
        return self.session.exec(query).all()

    def get_track_by_id(self, id: int) -> db.Track | None:
        return self.session.exec(
            select(db.Track).where(db.Track.id == id)
        ).one_or_none()

    def get_album_artist(self, track_id: int) -> db.Artist | None:
        track = self.get_track_by_id(track_id)
        if track is None:
            return None

        if track.album_artist_id is not None:
            artist = self.session.exec(
                select(db.Artist).where(db.Artist.id == track.album_artist_id).limit(1)
            ).one_or_none()
            if artist is not None:
                return artist

        return self.session.exec(
            select(db.Artist)
            .join(db.ArtistTrack)
            .where(db.Artist.id == db.ArtistTrack.artist_id)
            .where(db.ArtistTrack.track_id == track_id)
            .limit(1)
        ).one()

    def get_tracks_by_genre_name(
        self, genre_name: str, size: int | None = None, offset: int | None = None
    ) -> Sequence[db.Track]:
        query = (
            select(db.Track)
            .join(db.GenreTrack)
            .where(db.GenreTrack.track_id == db.Track.id)
            .join(db.Genre)
            .where(db.GenreTrack.genre_id == db.Genre.id)
            .where(db.Genre.name == genre_name)
        )
        if size:
            query = query.limit(size)
        if offset:
            query = query.offset(offset)
        return self.session.exec(query).all()


class GenresDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_all_genres(self) -> Sequence[db.Genre]:
        return self.session.exec(select(db.Genre)).all()


class FavouriteDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def star_track(self, id: int, user_id: int) -> None:
        track = TrackDBHelper(self.session).get_track_by_id(id)

        if track:
            if (id, user_id) in [
                (t.track_id, t.user_id) for t in track.track_favourites
            ]:
                return
            self.session.add(
                db.FavouriteTrack(
                    user_id=user_id, track_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_album(self, id: int, user_id: int) -> None:
        album = AlbumDBHelper(self.session).get_album_by_id(id)
        if album:
            if (id, user_id) in [
                (a.album_id, a.user_id) for a in album.album_favourites
            ]:
                return
            self.session.add(
                db.FavouriteAlbum(
                    user_id=user_id, album_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_artist(self, id: int, user_id: int) -> None:
        artist = ArtistDBHelper(self.session).get_artist_by_id(id)
        if artist:
            if (id, user_id) in [
                (a.artist_id, a.user_id) for a in artist.artist_favourites
            ]:
                return
            self.session.add(
                db.FavouriteArtist(
                    user_id=user_id, artist_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_playlist(self, id: int, user_id: int) -> None:
        playlist = PlaylistDBHelper(self.session).get_playlist(id)
        if playlist:
            if (id, user_id) in [
                (a.playlist_id, a.user_id) for a in playlist.playlist_favourites
            ]:
                return
            self.session.add(
                db.FavouritePlaylist(
                    user_id=user_id, playlist_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def unstar_track(self, id: int, user_id: int) -> None:
        fav_track = self.session.exec(
            select(db.FavouriteTrack).where(
                (db.FavouriteTrack.track_id == id)
                & (db.FavouriteTrack.user_id == user_id)
            )
        ).one_or_none()
        if fav_track:
            self.session.delete(fav_track)
            self.session.commit()

    def unstar_album(self, id: int, user_id: int) -> None:
        fav_album = self.session.exec(
            select(db.FavouriteAlbum).where(
                (db.FavouriteAlbum.album_id == id)
                & (db.FavouriteAlbum.user_id == user_id)
            )
        ).one_or_none()
        if fav_album:
            self.session.delete(fav_album)
            self.session.commit()

    def unstar_artist(self, id: int, user_id: int) -> None:
        fav_artist = self.session.exec(
            select(db.FavouriteArtist).where(
                (db.FavouriteArtist.artist_id == id)
                & (db.FavouriteArtist.user_id == user_id)
            )
        ).one_or_none()
        if fav_artist:
            self.session.delete(fav_artist)
            self.session.commit()

    def unstar_playlist(self, id: int, user_id: int) -> None:
        fav_playlist = self.session.exec(
            select(db.FavouritePlaylist).where(
                (db.FavouritePlaylist.playlist_id == id)
                & (db.FavouritePlaylist.user_id == user_id)
            )
        ).one_or_none()
        if fav_playlist:
            self.session.delete(fav_playlist)
            self.session.commit()

    def get_starred_tracks(self, user_id: int) -> Sequence[db.Track]:
        return self.session.exec(
            select(db.Track).where(
                (
                    (db.FavouriteTrack.track_id == db.Track.id)
                    & (db.FavouriteTrack.user_id == user_id)
                )
            )
        ).all()

    def get_starred_artists(self, user_id: int) -> Sequence[db.Artist]:
        return self.session.exec(
            select(db.Artist).where(
                (
                    (db.FavouriteArtist.artist_id == db.Artist.id)
                    & (db.FavouriteArtist.user_id == user_id)
                )
            )
        ).all()

    def get_starred_albums(self, user_id: int) -> Sequence[db.Album]:
        return self.session.exec(
            select(db.Album).where(
                (
                    (db.FavouriteAlbum.album_id == db.Album.id)
                    & (db.FavouriteAlbum.user_id == user_id)
                )
            )
        ).all()

    def get_starred_playlists(self, user_id: int) -> Sequence[db.Playlist]:
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

    def create_playlist(
        self, name: str, tracks: Sequence[int], user_id: int
    ) -> db.Playlist:
        now = datetime.today()
        playlist = db.Playlist(
            name=name,
            user_id=user_id,
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
        self.session.refresh(playlist)
        return playlist

    def update_playlist(
        self,
        id: int,
        name: str | None = None,
        traks_to_add: Sequence[int] = [],
        track_to_remove: Sequence[int] = [],
    ) -> db.Playlist | None:
        now = datetime.now()
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
            for t in traks_to_add:
                playlist_track = db.PlaylistTrack(
                    added_at=now, track_id=t, playlist_id=id
                )
                playlist.playlist_tracks.append(playlist_track)
            playlist.total_tracks = len(playlist.playlist_tracks)
            self.session.commit()
            self.session.refresh(playlist)
        return playlist

    def delete_playlist(self, id: int) -> bool:
        playlist = self.session.exec(
            select(db.Playlist).where(db.Playlist.id == id)
        ).one_or_none()
        if playlist:
            self.session.delete(playlist)
            self.session.commit()
            return True
        return False

    def get_playlist(self, id: int) -> db.Playlist | None:
        return self.session.exec(
            select(db.Playlist).where(db.Playlist.id == id)
        ).one_or_none()

    def get_all_playlists(self, db_user: db.User | None) -> Sequence[db.Playlist]:
        if db_user is None:
            return self.session.exec(select(db.Playlist)).all()
        else:
            return self.session.exec(
                select(db.Playlist).where(db.Playlist.user_id == db_user.id)
            ).all()


class UserDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_username(self, username: str) -> Optional[db.User]:
        return self.session.exec(
            select(db.User).where(db.User.login == username)
        ).one_or_none()
