from typing import Any, Generator
from sqlmodel import SQLModel, Session, create_engine, Field, Relationship

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


# Таблицы связи "многие к многим"
class GenreTrack(SQLModel, table=True):
    __tablename__ = "Genre_Tracks"
    genre_id: int = Field(primary_key=True, foreign_key="Genres.id")
    track_id: int = Field(primary_key=True, foreign_key="Tracks.id")


class ArtistTrack(SQLModel, table=True):
    __tablename__ = "Artist_Tracks"
    artist_id: int = Field(primary_key=True, foreign_key="Artists.id")
    track_id: int = Field(primary_key=True, foreign_key="Tracks.id")


class ArtistAlbum(SQLModel, table=True):
    __tablename__ = "Artist_Albums"
    artist_id: int = Field(primary_key=True, foreign_key="Artists.id")
    album_id: int = Field(primary_key=True, foreign_key="Albums.id")


class CustomTagTrack(SQLModel, table=True):
    __tablename__ = "CustomTag_Tracks"
    custom_tag_id: int = Field(primary_key=True, foreign_key="CustomTags.id")
    track_id: int = Field(primary_key=True, foreign_key="Tracks.id")


class PlaylistTrack(SQLModel, table=True):
    __tablename__ = "Playlist_Tracks"
    playlist_id: int = Field(primary_key=True, foreign_key="Playlists.id")
    track_id: int = Field(primary_key=True, foreign_key="Tracks.id")
    added_at: str

    playlist: "Playlist" = Relationship(back_populates="playlist_tracks")
    track: "Track" = Relationship(back_populates="track_playlists")


class FavouriteTrack(SQLModel, table=True):
    __tablename__ = "Favourite_Tracks"
    user_id: int = Field(primary_key=True, foreign_key="Users.id")
    track_id: int = Field(primary_key=True, foreign_key="Tracks.id")
    added_at: str

    user: "User" = Relationship(back_populates="favourite_tracks")
    track: "Track" = Relationship(back_populates="track_favourites")


class FavouriteAlbum(SQLModel, table=True):
    __tablename__ = "Favourite_Albums"
    user_id: int = Field(primary_key=True, foreign_key="Users.id")
    album_id: int = Field(primary_key=True, foreign_key="Albums.id")
    added_at: str

    user: "User" = Relationship(back_populates="favourite_albums")
    album: "Album" = Relationship(back_populates="album_favourites")


class FavouritePlaylist(SQLModel, table=True):
    __tablename__ = "Favourite_Playlists"
    user_id: int = Field(primary_key=True, foreign_key="Users.id")
    playlist_id: int = Field(primary_key=True, foreign_key="Playlists.id")
    added_at: str

    user: "User" = Relationship(back_populates="favourite_playlists")
    playlist: "Playlist" = Relationship(back_populates="playlist_favourites")


class FavouriteArtist(SQLModel, table=True):
    __tablename__ = "Favourite_Artists"
    user_id: int = Field(primary_key=True, foreign_key="Users.id")
    artist_id: int = Field(primary_key=True, foreign_key="Artists.id")
    added_at: str

    user: "User" = Relationship(back_populates="favourite_artists")
    artist: "Artist" = Relationship(back_populates="artist_favourites")


# Основные таблицы
class User(SQLModel, table=True):
    __tablename__ = "Users"
    id: int = Field(primary_key=True)
    login: str
    password: str
    avatar: str

    playlists: list["Playlist"] = Relationship(back_populates="user")
    favourite_tracks: list["FavouriteTrack"] = Relationship(back_populates="user")
    favourite_albums: list["FavouriteAlbum"] = Relationship(back_populates="user")
    favourite_playlists: list["FavouritePlaylist"] = Relationship(back_populates="user")
    favourite_artists: list["FavouriteArtist"] = Relationship(back_populates="user")


class Track(SQLModel, table=True):
    __tablename__ = "Tracks"
    id: int = Field(primary_key=True)
    file_path: str
    file_size: int
    type: str
    title: str = Field(index=True)
    album_id: int | None = Field(foreign_key="Albums.id")
    album_artist_id: int | None = Field(foreign_key="Artists.id")
    album_position: int | None
    year: str | None
    plays_count: int
    cover: bytes
    cover_type: str

    bit_rate: int
    bits_per_sample: int
    sample_rate: int
    channels: int
    duration: int

    album: "Album" = Relationship(back_populates="tracks")
    genres: list["Genre"] = Relationship(back_populates="tracks", link_model=GenreTrack)
    artists: list["Artist"] = Relationship(
        back_populates="tracks", link_model=ArtistTrack
    )
    custom_tags: list["CustomTag"] = Relationship(
        back_populates="tracks", link_model=CustomTagTrack
    )
    track_playlists: list["PlaylistTrack"] = Relationship(back_populates="track")
    track_favourites: list["FavouriteTrack"] = Relationship(back_populates="track")


class Artist(SQLModel, table=True):
    __tablename__ = "Artists"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    tracks: list["Track"] = Relationship(
        back_populates="artists", link_model=ArtistTrack
    )
    albums: list["Album"] = Relationship(
        back_populates="artists", link_model=ArtistAlbum
    )
    artist_favourites: list["FavouriteArtist"] = Relationship(back_populates="artist")

    def __hash__(self) -> int:
        return hash(self.name)


class Album(SQLModel, table=True):
    __tablename__ = "Albums"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    album_artist_id: int | None = Field(foreign_key="Artists.id")
    total_tracks: int
    year: str | None
    cover: bytes | None
    play_count: int = Field(default=0)

    tracks: list["Track"] = Relationship(back_populates="album")
    artists: list["Artist"] = Relationship(
        back_populates="albums", link_model=ArtistAlbum
    )
    album_favourites: list["FavouriteAlbum"] = Relationship(back_populates="album")


class Playlist(SQLModel, table=True):
    __tablename__ = "Playlists"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    user_id: int = Field(foreign_key="Users.id")
    total_tracks: int
    create_date: str

    user: "User" = Relationship(back_populates="playlists")
    playlist_tracks: list["PlaylistTrack"] = Relationship(
        back_populates="playlist", cascade_delete=True
    )
    playlist_favourites: list["FavouritePlaylist"] = Relationship(
        back_populates="playlist"
    )


class Genre(SQLModel, table=True):
    __tablename__ = "Genres"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    tracks: list["Track"] = Relationship(back_populates="genres", link_model=GenreTrack)

    def __hash__(self) -> int:
        return hash(self.name)


class CustomTag(SQLModel, table=True):
    __tablename__ = "CustomTags"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    value: str
    updated: bool

    tracks: list["Track"] = Relationship(
        back_populates="custom_tags", link_model=CustomTagTrack
    )
