import datetime
import jwt
from flask import request, jsonify, Blueprint, render_template, url_for, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import UserModel

SECRET_KEY = "5CAFEE97B58AE2C8FE35A74655E23"

auth_bp = Blueprint("auth", __name__)


def generate_token(user_id):
    payload = {
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
        "iat": datetime.datetime.now(datetime.UTC),
        "sub": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.json if request.is_json else request.form
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Missing data"}), 400

        # hashed_password = generate_password_hash(password)

        new_user = UserModel(username=username, password=password, is_superuser=False)
        new_user.save()
        print(f"User {new_user.username} created with ID: {new_user._id}")
        login_user(new_user)
        return redirect(url_for("auth.login"))
        # token = generate_token(str(new_user._id))

    else:
        return render_template("enter.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json if request.is_json else request.form
        username = data.get("username")
        password = data.get("password")

        user = UserModel.find_by_username(username)

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("home.homepage"))
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    else:
        return render_template("enter.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    try:
        logout_user()
        session.clear()
        return redirect(url_for("auth.login"))
    except Exception as e:
        return jsonify({"message": "Error."}), 500