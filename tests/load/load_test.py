from locust import HttpUser, task, between
import random

class MusicRitmoUser(HttpUser):
    host = "http://localhost:8000" 
    wait_time = between(1, 3)

    username = "admin"
    password = "admin"
    artists = list(range(1, 9))
    albums = list(range(1, 6))
    tracks = list(range(1, 9))
    genres = ["Рэп", "Хип-хоп", "Рок", "Джент", "Дрифт-фонк"]

    @task(2)
    def search(self):
        query = random.choice(self.genres)
        self.client.get(f"/rest/search3?query={query}&songCount=100&albumCount=100&artistCount=100&songOffset=0&albumOffset=0&artistOffset=0&username={self.username}&u={self.username}&p={self.password}")

    @task(1)
    def get_genres(self):
        self.client.get("/rest/getGenres")
    
    @task(3)
    def get_song(self):
        song_id = random.choice(self.tracks)
        self.client.get(f"/rest/getSong?id={song_id}&username={self.username}&u={self.username}&p={self.password}")

    @task(2)
    def get_artist(self):
        artist_id = random.choice(self.artists)
        self.client.get(f"/rest/getArtist?id={artist_id}")

    @task(2)
    def get_album(self):
        album_id = random.choice(self.albums)
        self.client.get(f"/rest/getAlbum?id={album_id}&username={self.username}&u={self.username}&p={self.password}")

    @task(1)
    def get_starred(self):
        self.client.get(f"/rest/getStarred2?username={self.username}&u={self.username}&p={self.password}")
    
    @task(3)
    def stream_song(self):
        song_id = random.choice(self.tracks)
        self.client.get(f"/rest/stream?id={song_id}")

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --host=http://localhost:8000")