from sqlmodel import Session, select 
from . import database as db

class ArtistDao:
    def __init__(self, session: Session):
        self.session = session
    
    def getAllArtists(self):
        return self.session.exec(select(db.Artist)).all()
    
    def getArtistById(self, id):
        return self.session.exec(select(db.Artist).where(db.Artist.id == id)).one_or_none()
    

class AlbumDao:
    def __init__(self, session: Session):
        self.session = session
    
    def getAllAlbums(self):
        return self.session.exec(select(db.Album)).all()
    
    def getAlbumById(self, id):
        return self.session.exec(select(db.Album).where(db.Album.id == id)).one_or_none()
    

class TrackDao:
    def __init__(self, session: Session):
        self.session = session
    
    def getAllTracks(self):
        return self.session.exec(select(db.Track)).all()
    
    def getTrackById(self, id):
        return self.session.exec(select(db.Track).where(db.Track.id == id)).one_or_none()
    
class GenresDao:
    def __init__(self, session: Session):
        self.session = session
    
    def getAllGenres(self):
        return self.session.exec(select(db.Genre)).all()
    
    def getTrackByName(self, name):
        return self.session.exec(select(db.Genre).where(db.Genre.name == name)).one_or_none()