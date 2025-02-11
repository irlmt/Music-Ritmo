from typing import Any, Sequence

from src.app.dto import *


class OpenSubsonicFormatter:
    @staticmethod
    def format_genre(genre: Genre) -> dict[str, Any]:
        return {
            "albumCount": genre.albumCount,
            "songCount": genre.songCount,
            "value": genre.name,
        }

    @staticmethod
    def format_genres(genres: Sequence[Genre]) -> dict[str, Any]:
        return {"genre": list(map(OpenSubsonicFormatter.format_genre, genres))}
