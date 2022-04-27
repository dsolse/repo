from flask_login import LoginManager
from models.usuarios import Usuarios

login_manager = LoginManager()

login_manager.login_view = "main.login" # type: ignore

@login_manager.user_loader
def load_user(id_user):
    user = Usuarios.query.get(id_user)
    return user