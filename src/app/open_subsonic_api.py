from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from . import database as db

open_subsonic_router = APIRouter(prefix="/rest")


class SubsonicResponse:
    def __init__(self):
        self.data = {}
        self.data["status"] = "ok"
        self.data["version"] = "1.16.1"
        self.data["type"] = "MusicRitmo"
        self.data["serverVersion"] = "0.1"
        self.data["openSubsonic"] = True

    def to_json_rsp(self) -> JSONResponse:
        return JSONResponse({"subsonic-response": self.data})


@open_subsonic_router.get("/ping")
async def ping():
    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/search")
async def search(query: dict=Body(), session: Session = Depends(db.get_session)):
    name = query["query"]
    artistCount = query.get("artistCount", 20)
    artistOffset = query.get("artistOffset", 0)
    albumCount = query.get("albumCount", 20)
    albumOffset = query.get("albumOffset", 0)
    songCount = query.get("songCount", 20)
    songOffset = query.get("songOffset", 0)

    artists = session.exec(select(db.Artist)).all()
    if artistCount * artistOffset >= len(artists):
        artists = []
    else:
        artists = [a for a in artists if name in a.name]
        albumNum = [len(a.albums) for a in artists]
        artists = [a.model_dump() for a in artists]
        for i in range(len(artists)):
            artists[i]["albumCount"] = albumNum[i]
            artists[i]["coverArt"] = "ar-100000002"
            artists[i]["starred"] = "2021-02-22T05:54:18Z"
        artists = artists[artistCount*artistOffset:min(len(artists), artistCount*artistOffset+artistCount)]

    albums = session.exec(select(db.Album)).all()
    if albumCount * albumOffset >= len(albums):
        albums = []
    else:
        albums = [a for a in albums if name in a.name]
        songs = [s.tracks for s in albums]
        names = [n.name for n in albums]
        years = [y.year for y in albums]
        albArtists = [a.artists for a in albums]
        albums = [a.model_dump() for a in albums]
        for i in range(len(albums)):
            albums[i]["parent"] = "100000036"
            albums[i]["coverArt"] = "ar-100000002"
            albums[i]["album"] = names[i]
            albums[i]["title"] = names[i]
            albums[i]["name"] = names[i]
            albums[i]["created"] = years[i]
            albums[i]["year"] = years[i]
            albums[i]["isDir"] = True
            albums[i]["songCount"] = len(songs[i])
            albums[i]["playCount"] = 0
            albums[i]["artistId"] = albArtists[i][0].id
            albums[i]["artist"] = albArtists[i][0].name
            duration = sum([s.duration for s in songs[i]])
            albums[i]["duration"] = duration
            genres = [g.genres for g in songs[i]]
            albums[i]["genre"] = "Pop"
        albums = albums[albumCount*albumOffset:min(len(albums), albumCount*albumOffset+albumCount)]

    tracks = session.exec(select(db.Track)).all()
    if songCount * songOffset >= len(tracks):
        tracks = []
    else:
        tracks = [a for a in tracks if name in a.title]
        artistTrack = [a.artists for a in tracks]
        albumTrack = [a.album for a in tracks]
        trackTitles = [t.title for t in tracks]
        filePath = [p.file_path for p in tracks]
        playCount = [c.plays_count for c in tracks]
        tracks = [t.model_dump() for t in tracks]
        for i in range(len(tracks)):
            tracks[i]["parent"] = "e8a0685e3f3ec6f251649af2b58b8617"
            tracks[i]["isDir"] = False
            tracks[i]["title"] = trackTitles[i]
            tracks[i]["album"] = albumTrack[i].name if albumTrack[i] is not None else "Without album"
            artist = [a.name for a in artistTrack[i]]
            tracks[i]["artist"] = " ".join(artist)
            tracks[i]["track"] = 1
            tracks[i]["coverArt"] = ["mf-082f435a363c32c57d5edb6a678a28d4_6410b3ce"]
            tracks[i]["size"] = 19866778
            tracks[i]["contentType"] = "mp3/flac"
            tracks[i]["suffix"] = "mp3"
            tracks[i]["starred"] = "2023-03-27T09:45:27Z"
            tracks[i]["bitRate"] = 880
            tracks[i]["bitDepth"] = 16
            tracks[i]["simplingRate"] = 44100
            tracks[i]["channelCount"] = 2
            tracks[i]["path"] = filePath[i]
            tracks[i]["playCount"] = playCount[i]
            tracks[i]["discNumber"] = 1
            tracks[i]["created"] = ""
            tracks[i]["albumId"] = albumTrack[i].id if albumTrack[i] is not None else -1
            print(artistTrack)
            tracks[i]["artistId"] = -1
            tracks[i]["type"] = "music"
            tracks[i]["isVideo"] = False
        tracks = tracks[songCount*songOffset:min(len(tracks), songCount*songOffset+songCount)]

    searchResult = {}
    searchResult["artist"] = artists
    searchResult["song"] = tracks
    searchResult["album"] = albums
    rsp = SubsonicResponse()
    rsp.data["searchResult"] = searchResult
    return rsp.to_json_rsp()

