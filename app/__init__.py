from flask import Flask
from app.view.conversation_manager import bp_manager

from app.view.get_response import bp_response
from app.view.wechat import bp_wechat


def create_app():
    app = Flask(__name__)

    app.register_blueprint(bp_manager, url_prefix='/admin')
    app.register_blueprint(bp_response)
    app.register_blueprint(bp_wechat)

    return app
