# coding: utf-8

from flask_login import LoginManager

from app.model.user import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
