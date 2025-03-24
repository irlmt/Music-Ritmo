from locust import HttpUser, task, between
import random
import logging
import urllib3

class UnlimitedSubsonicUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://localhost:8000"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.album_ids = list(range(1, 6)) 
        self.track_ids = list(range(1, 9))
        self.username = "admin"
        self.password = "admin"
        
        self.client.verify = False
        self.client.timeout = None 

    def _get_params(self):
        return {
            "user": self.username,
            "u": self.username,
            "p": self.password,
        }

    def _make_unlimited_request(self, path, params=None, name=None):
        try:
            response = self.client.get(
                path,
                params={**self._get_params(), **(params or {})},
                name=name or path,
                timeout=None
            )
            if response.status_code >= 400:
                logging.warning(f"Request failed: {path} - Status {response.status_code}")
            return response
        except Exception as e:
            logging.error(f"Request error: {path} - {str(e)}")
            return None

    @task(5)
    def test_ping(self):
        self._make_unlimited_request("/rest/ping")

    @task(10)
    def test_get_album(self):
        self._make_unlimited_request(
            "/rest/getAlbum",
            params={"id": random.choice(self.album_ids)}
        )

    @task(8)
    def test_get_random_songs(self):
        self._make_unlimited_request(
            "/rest/getRandomSongs",
            params={"size": 5}
        )

    @task(3)
    def test_stream(self):
        self._make_unlimited_request(
            "/rest/stream",
            params={"id": random.choice(self.track_ids)},
            stream=True
        )

    @task(1)
    def test_search(self):
        self._make_unlimited_request(
            "/rest/search2",
            params={"query": random.choice(["рэп", "alla", "songs"])}
        )