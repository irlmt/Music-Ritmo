from dataclasses import dataclass


@dataclass
class Genre:
    albumCount: int
    songCount: int
    name: str
