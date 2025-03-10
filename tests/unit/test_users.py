import pytest
import unittest
from unittest.mock import MagicMock, patch
from fastapi.responses import JSONResponse
import src.app.open_subsonic_api as api


class TestOpenSubsonicAPI(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.user_mock = MagicMock()
        self.user_mock.login = "testuser"

    @pytest.mark.asyncio
    async def test_create_user_error(self):
        with patch("src.app.service_layer.create_user") as mock_create_user:
            mock_create_user.return_value = (None, "Error creating user")
            result = await api.create_user(
                username="testuser", password="testpass", session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 400
            assert result.body == b'{"detail":"Error creating user"}'

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
    async def test_update_user_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = None
            result = await api.update_user(
                username="testuser", session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"User not found"}'

    @pytest.mark.asyncio
    async def test_change_password_not_found(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.one_or_none.return_value = None
            result = await api.change_password(
                username="testuser",
                password="newpass",
                session=self.session_mock,
                current_user=self.user_mock,
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"User not found"}'

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
    async def test_get_users(self):
        with patch("src.app.database.Session.exec") as mock_exec:
            mock_exec.return_value.all.return_value = [self.user_mock]
            result = await api.get_users(
                session=self.session_mock, current_user=self.user_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200


if __name__ == "__main__":
    unittest.main()
