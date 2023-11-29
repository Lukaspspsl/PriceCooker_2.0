import jwt
from flask import jsonify, redirect
from app.auth.auth import generate_token, register, login
from app.auth.auth import SECRET_KEY
from app.models.models import UserModel

class TestGenerateToken:

    #  Generates a JWT token with a valid user ID
    def test_generate_token_valid_user_id(self):
        user_id = "12345"
        token = generate_token(user_id)
        assert isinstance(token, str)
        assert token != ""

    #  Returns a string containing the encoded JWT token
    def test_generate_token_encoded_token(self):
        user_id = "12345"
        token = generate_token(user_id)
        assert isinstance(token, str)
        assert token != ""

    #  Uses the current datetime to set the token expiration date
    def test_generate_token_expiration_date(self):
        user_id = "12345"
        token = generate_token(user_id)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        assert "exp" in decoded_token
        assert isinstance(decoded_token["exp"], int)

    #  Raises an exception if the user ID is not provided
    def test_generate_token_no_user_id(self):
        with pytest.raises(TypeError):
            generate_token()

    #  Raises an exception if the SECRET_KEY is not provided
    def test_generate_token_no_secret_key(self):
        user_id = "12345"
        with pytest.raises(TypeError):
            generate_token(user_id)

    #  Raises an exception if the datetime module is not available
    def test_generate_token_no_datetime_module(self, monkeypatch):
        monkeypatch.delattr("datetime")
        user_id = "12345"
        with pytest.raises(AttributeError):
            generate_token(user_id)


class TestRegister:

    #  User provides valid username and password, and a new user is created and logged in.
    def test_valid_username_and_password(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.is_json", return_value=True)
        mocker.patch("flask.request.json", return_value={"username": "test_user", "password": "test_password"})
        mocker.patch("app.auth.auth.UserModel.find_by_username", return_value=None)
        mocker.patch("app.auth.auth.UserModel.save")
        mocker.patch("app.auth.auth.login_user")

        response = register()

        assert response.status_code == 302
        assert response.location == "/auth/login"

    #  User provides valid username and password, but user already exists, so an error message is returned.
    def test_existing_user(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.is_json", return_value=True)
        mocker.patch("flask.request.json", return_value={"username": "existing_user", "password": "test_password"})
        mocker.patch("app.auth.auth.UserModel.find_by_username",
                     return_value=UserModel(username="existing_user", password="test_password"))
        mocker.patch("flask.jsonify")

        response = register()

        assert response.status_code == 400

    #  User provides valid username and password, but there is an error creating the user, so an error message is returned.
    def test_error_creating_user(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.is_json", return_value=True)
        mocker.patch("flask.request.json", return_value={"username": "test_user", "password": "test_password"})
        mocker.patch("app.auth.auth.UserModel.find_by_username", return_value=None)
        mocker.patch("app.auth.auth.UserModel.save", side_effect=Exception)
        mocker.patch("flask.jsonify")

        response = register()

        assert response.status_code == 500

    #  User provides an empty username, so an error message is returned.
    def test_empty_username(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.is_json", return_value=True)
        mocker.patch("flask.request.json", return_value={"username": "", "password": "test_password"})
        mocker.patch("flask.jsonify")

        response = register()

        assert response.status_code == 400

    #  User provides an empty password, so an error message is returned.
    def test_empty_password(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.is_json", return_value=True)
        mocker.patch("flask.request.json", return_value={"username": "test_user", "password": ""})
        mocker.patch("flask.jsonify")

        response = register()

        assert response.status_code == 400

    #  User provides a username that is too long, so an error message is returned.
    def test_long_username(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.is_json", return_value=True)
        mocker.patch("flask.request.json", return_value={"username": "a" * 101, "password": "test_password"})
        mocker.patch("flask.jsonify")

        response = register()

        assert response.status_code == 400


# Generated by CodiumAI

# Dependencies:
# pip install pytest-mock
import pytest


class TestLogin:

    #  Login with valid username and password redirects to homepage
    def test_valid_username_and_password_redirects_to_homepage(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.json", return_value={"username": "test_user", "password": "test_password"})
        mocker.patch("app.auth.auth.UserModel.find_by_username",
                     return_value=UserModel(username="test_user", password="test_password"))
        mocker.patch("app.auth.auth.login_user")
        mocker.patch("flask.url_for", return_value="/homepage")

        response = login()

        assert response == redirect("/homepage")

    #  Login with valid username and invalid password returns 401 error
    def test_valid_username_and_invalid_password_returns_401_error(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.json", return_value={"username": "test_user", "password": "test_password"})
        mocker.patch("app.auth.auth.UserModel.find_by_username",
                     return_value=UserModel(username="test_user", password="wrong_password"))
        mocker.patch("flask.jsonify")
        mocker.patch("flask.url_for", return_value="/login")

        response = login()

        assert response == jsonify({"message": "Invalid username or password"}), 401

    #  Login with empty username returns 401 error
    def test_empty_username_returns_401_error(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.json", return_value={"username": "", "password": "test_password"})
        mocker.patch("flask.jsonify")
        mocker.patch("flask.url_for", return_value="/login")

        response = login()

        assert response == jsonify({"message": "Invalid username or password"}), 401

    #  Login with empty password returns 401 error
    def test_empty_password_returns_401_error(self, mocker):
        mocker.patch("flask.request")
        mocker.patch("flask.request.method", return_value="POST")
        mocker.patch("flask.request.json", return_value={"username": "test_user", "password": ""})
        mocker.patch("flask.jsonify")
        mocker.patch("flask.url_for", return_value="/login")

        response = login()

        assert response == jsonify({"message": "Invalid username or password"}), 401

    def test_logout_success(self):
        response = self.client.get('/logout')
        assert response.status_code == 302
        assert response.location == 'http://localhost/'
