import unittest
from unittest.mock import MagicMock, patch
from fastapi.responses import Response, JSONResponse
from src.app.frontend_endpoints import generate_random_avatar, get_tags
import json


class TestAvatarEndpoints(unittest.TestCase):
    def setUp(self):
        self.user_mock = MagicMock()

    @patch("src.app.service_layer.generate_and_save_avatar")
    def test_generate_random_avatar_success(self, mock_generate):
        mock_generate.return_value = b"fake_avatar"
        response = generate_random_avatar(self.user_mock, MagicMock())
        self.assertEqual(response.media_type, "image/png")
        self.assertEqual(response.body, b"fake_avatar")

    @patch("src.app.service_layer.generate_and_save_avatar")
    def test_generate_random_avatar_failure(self, mock_generate):
        mock_generate.return_value = None
        response = Response(status_code=500)
        self.assertEqual(response.status_code, 500)


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.data_mock = {"artist": "New Artist"}

    @patch("src.app.utils.get_base_tags", return_value={"title": "Song"})
    @patch("src.app.utils.get_custom_tags", return_value={"mood": "Happy"})
    def test_get_tags_success(self, mock_get_custom, mock_get_base):
        response = get_tags(1, MagicMock())
        expected_response = {"title": "Song", "mood": "Happy"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), expected_response)

    def test_get_tags_not_found(self):
        response = JSONResponse(content={"detail": "No such id"}, status_code=404)
        expected_response = {"detail": "No such id"}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.body), expected_response)

    def test_update_tags_not_found(self):
        response = JSONResponse(content={"detail": "No such id"}, status_code=404)
        expected_response = {"detail": "No such id"}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.body), expected_response)


if __name__ == "__main__":
    unittest.main()
