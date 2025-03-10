import json
import pytest
import unittest
from unittest.mock import MagicMock, patch
from fastapi.responses import JSONResponse
import src.app.open_subsonic_api as api
import src.app.database as db


class TestOpenSubsonicAPI(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.user_mock = MagicMock()
        self.user_mock.login = "testuser"

    async def test_create_user_error(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (None, "Error creating user")
            result = await api.create_user(
                username="testuser", password="testpass", session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 400
            assert result.body == b'{"detail":"Error creating user"}'

    async def test_create_user_success(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (
                db.User(login="testuser"),
                None,
            )

            result = await api.create_user(
                username="testuser", password="testpass", session=self.session_mock
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 200
            assert result.body == b'{"status":"ok"}'

    async def test_delete_user(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock
            result = await api.delete_user(
                username="testuser",
                current_user=self.user_mock,
                session=self.session_mock,
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    async def test_update_user_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = None
            result = await api.update_user(
                username="testuser", session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"User not found"}'

    async def test_update_user_success(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock

            with patch("src.app.database.Session.commit") as mock_commit:
                result = await api.update_user(
                    username="testuser", session=self.session_mock
                )

                assert isinstance(result, JSONResponse)
                assert result.status_code == 200
                assert result.body == b'{"detail":"User updated successfully"}'

                mock_commit.assert_called_once()

    async def test_change_password_success(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock

            with patch("src.app.database.Session.commit") as mock_commit:
                result = await api.change_password(
                    username="testuser",
                    password="newpass",
                    session=self.session_mock,
                    current_user=self.user_mock,
                )

                assert isinstance(result, JSONResponse)
                assert result.status_code == 200
                assert result.body == b'{"status":"ok"}'

                mock_commit.assert_called_once()

    async def test_get_user_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = None
            result = await api.get_user(
                username="testuser",
                session=self.session_mock,
                current_user=self.user_mock,
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"User not found"}'

    async def test_get_user_success(self):
        fake_user = db.User(login="testuser")

        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = fake_user

            result = await api.get_user(
                username="testuser",
                session=self.session_mock,
                current_user=self.user_mock,
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

            expected_response = json.dumps(
                {
                    "subsonic-response": {
                        "status": "ok",
                        "version": "1.16.1",
                        "user": {"username": "testuser", "folder": [1]},
                    }
                }
            ).encode("utf-8")

            assert result.body == expected_response

    async def test_get_users(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.all.return_value = [self.user_mock]
            result = await api.get_users(
                session=self.session_mock, current_user=self.user_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    async def test_update_user_db_error(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.side_effect = Exception("Database error")

            result = await api.update_user(
                username="testuser", session=self.session_mock
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 500
            assert result.body == b'{"detail":"Internal server error"}'

    async def test_change_password_unauthorized(self):
        another_user = MagicMock()
        another_user.login = "another_user"

        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock

            result = await api.change_password(
                username="testuser",
                password="newpass",
                session=self.session_mock,
                current_user=another_user,
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 403
            assert result.body == b'{"detail":"Permission denied"}'

    async def test_create_user_already_exists(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (None, "User already exists")

            result = await api.create_user(
                username="testuser", password="testpass", session=self.session_mock
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 400
            assert result.body == b'{"detail":"User already exists"}'
