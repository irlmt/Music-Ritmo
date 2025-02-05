from datetime import datetime
from sqlmodel import Session, select, Field
from sqlalchemy import func
from . import database as db


class ArtistDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def getAllArtists(self, filterName=None):
        if filterName:
            return self.session.exec(
                select(db.Artist).where(
                    func.lower(db.Artist.name).like(f"%{filterName.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Artist)).all()

    def getArtistById(self, id):
        return self.session.exec(
            select(db.Artist).where(db.Artist.id == id)
        ).one_or_none()


class AlbumDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def getAllAlbums(self, filterName=None):
        if filterName:
            return self.session.exec(
                select(db.Album).where(
                    func.lower(db.Album.name).like(f"%{filterName.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Album)).all()

    def getAlbumById(self, id):
        return self.session.exec(
            select(db.Album).where(db.Album.id == id)
        ).one_or_none()


class TrackDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def getAllTracks(self, filterTitle=None):
        if filterTitle:
            return self.session.exec(
                select(db.Track).where(
                    func.lower(db.Track.title).like(f"%{filterTitle.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Track)).all()

    def getTrackById(self, id):
        return self.session.exec(
            select(db.Track).where(db.Track.id == id)
        ).one_or_none()

    def getTrackByArtistId(self, artistId):
        return self.session.exec(
            select(db.Track)
            .join(db.ArtistTrack)
            .where(db.ArtistTrack.artist_id == artistId)
        ).all()


class GenresDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def get_genres_by_name(self, filterName=None):
        if filterName:
            return self.session.exec(
                select(db.Genre).where(func.lower(db.Genre.name) == filterName.lower())
            ).all()
        return self.session.exec(select(db.Genre)).all()

    def getAllGenres(self, filterName=None):
        if filterName:
            return self.session.exec(
                select(db.Genre).where(
                    func.lower(db.Genre.name).like(f"%{filterName.lower()}%")
                )
            ).all()
        return self.session.exec(select(db.Genre)).all()

    def getTrackByName(self, name):
        return self.session.exec(
            select(db.Genre).where(db.Genre.name == name)
        ).one_or_none()


class FavouriteDBHelper:
    def __init__(self, session: Session):
        self.session = session

    def star_track(self, id: int, user_id: int = 0):
        track = TrackDBHelper(self.session).getTrackById(id)
        if track:
            self.session.add(
                db.FavouriteTrack(
                    user_id=user_id, track_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_album(self, id: int, user_id: int = 0):
        album = AlbumDBHelper(self.session).getAlbumById(id)
        if album:
            self.session.add(
                db.FavouriteAlbum(
                    user_id=user_id, album_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_artist(self, id: int, user_id: int = 0):
        artist = ArtistDBHelper(self.session).getArtistById(id)
        if artist:
            self.session.add(
                db.FavouriteArtist(
                    user_id=user_id, artist_id=id, added_at=datetime.today()
                )
            )
            self.session.commit()

    def star_playlist(self, id: int, user_id: int = 0):
        playlist = PlaylistDBHelper(self.session).get_playlist(id)
        if playlist:
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
                    (db.FavouriteTrack.track_id
                    == db.Track.id) & (db.FavouriteTrack.user_id == user_id)
                )
            )
        ).all()

    def get_starred_artists(self, user_id=0):
        return self.session.exec(
            select(db.Artist).where(
                (
                    (db.FavouriteArtist.artist_id
                    == db.Artist.id) & (db.FavouriteArtist.user_id == user_id)
                )
            )
        ).all()

    def get_starred_albums(self, user_id=0):
        return self.session.exec(
            select(db.Album).where(
                (
                    (db.FavouriteAlbum.album_id
                    == db.Album.id) & (db.FavouriteAlbum.user_id == user_id)
                )
            )
        ).all()

    def get_starred_playlists(self, user_id=0):
        return self.session.exec(
            select(db.Playlist).where(
                (
                    (db.FavouritePlaylist.playlist_id
                    == db.Playlist.id) & (db.FavouritePlaylist.user_id == user_id)
                )
            )
        ).all()
