from flask_login import LoginManager
from app.models.models import UserModel

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return UserModel.user_by_id(user_id)
