import json
import pytest
import unittest
from unittest.mock import MagicMock, patch
from fastapi.responses import JSONResponse
import src.app.open_subsonic_api as api
import src.app.database as db
import src.app.subsonic_response as s_resp


class TestOpenSubsonicAPI(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.user_mock = MagicMock()
        self.user_mock.login = "testuser"
        self.sr = s_resp.SubsonicResponse()

    def test_create_user_error(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (None, "Error creating user")
            result = api.create_user(
                username="testuser", password="testpass", session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 400
            assert result.body == b'{"detail":"Error creating user"}'

    def test_create_user_success(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (
                db.User(login="testuser"),
                None,
            )

            result = api.create_user(
                username="testuser", password="testpass", session=self.session_mock
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 200
            expected_response = self.sr.data
            actual_response = json.loads(result.body)["subsonic-response"]
            assert actual_response == expected_response

    def test_update_user_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = None

            result = api.update_user(
                username="testuser",
                current_user=self.user_mock,
                session=self.session_mock,
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

            expected_response = self.sr.data
            actual_response = json.loads(result.body)["subsonic-response"]
            assert actual_response == expected_response

    def test_update_user_success(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock

            with patch("src.app.database.Session.commit") as mock_commit:
                result = api.update_user(
                    username="testuser",
                    current_user=self.user_mock,
                    session=self.session_mock,
                )

                assert isinstance(result, JSONResponse)
                assert result.status_code == 200

                expected_response = self.sr.data
                actual_response = json.loads(result.body)["subsonic-response"]
                assert actual_response == expected_response

    def test_delete_user(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock
            result = api.delete_user(
                username="testuser",
                current_user=self.user_mock,
                session=self.session_mock,
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_change_password_success(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock
            with patch("src.app.database.Session.commit") as mock_commit:
                result = api.change_password(
                    username="testuser",
                    password="newpass",
                    session=self.session_mock,
                    current_user=self.user_mock,
                )

                assert isinstance(result, JSONResponse)
                assert result.status_code == 200

    def test_get_user_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value = MagicMock()
            mock_exec.return_value.one_or_none.return_value = None

            self.session_mock.exec.return_value = mock_exec.return_value

            result = api.get_user(
                username="testuser",
                session=self.session_mock,
                current_user=self.user_mock,
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 404

    def test_get_user_success(self):
        with patch("src.app.database.Session.exec") as mock_exec:

            class UserMock:
                def __init__(self, login):
                    self.login = login

            user_mock = UserMock(login="testuser")

            mock_exec.return_value = MagicMock()
            mock_exec.return_value.one_or_none.return_value = user_mock

            self.session_mock.exec.return_value = mock_exec.return_value

            result = api.get_user(
                username="testuser",
                session=self.session_mock,
                current_user=user_mock,
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_get_users(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.all.return_value = [self.user_mock]
            result = api.get_users(
                session=self.session_mock, current_user=self.user_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_change_password_unauthorized(self):
        another_user = MagicMock()
        another_user.login = "another_user"

        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock

            result = api.change_password(
                username="testuser",
                password="newpass",
                session=self.session_mock,
                current_user=another_user,
            )

            assert isinstance(result, JSONResponse)
            expected_response = self.sr.set_error(
                50, "The user can only change his password"
            )
            expected_response = self.sr.data
            actual_response = json.loads(result.body)["subsonic-response"]
            assert actual_response == expected_response

    def test_create_user_already_exists(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (None, "User already exists")

            result = api.create_user(
                username="testuser", password="testpass", session=self.session_mock
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 400

    def test_delete_user_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = None
            result = api.delete_user(
                username="testuser",
                current_user=self.user_mock,
                session=self.session_mock,
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_update_user_unauthorized(self):
        another_user = MagicMock()
        another_user.login = "another_user"

        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = self.user_mock

            result = api.update_user(
                username="testuser",
                password="newpass",
                session=self.session_mock,
                current_user=another_user,
            )

            assert isinstance(result, JSONResponse)
            expected_response = self.sr.set_error(
                50, "User can only update their own data"
            )
            expected_response = self.sr.data
            actual_response = json.loads(result.body)["subsonic-response"]
            assert actual_response == expected_response

    def test_get_users_empty(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.all.return_value = []

            result = api.get_users(
                session=self.session_mock, current_user=self.user_mock
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 200
            assert json.loads(result.body)["subsonic-response"]["users"] == {"user": []}

    def test_change_password_user_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value = MagicMock()
            mock_exec.return_value.one_or_none.return_value = None

            result = api.change_password(
                username="testuser",
                password="newpass",
                session=self.session_mock,
                current_user=self.user_mock,
            )

            assert isinstance(result, JSONResponse)
            expected_response = self.sr.set_error(
                50, "The user can only change his password"
            )
            expected_response = self.sr.data
            actual_response = json.loads(result.body)["subsonic-response"]
            assert actual_response == expected_response

    def test_create_user_missing_password(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (None, "Password is required")

            result = api.create_user(
                username="testuser", password="", session=self.session_mock
            )

            assert isinstance(result, JSONResponse)
            assert result.status_code == 400
