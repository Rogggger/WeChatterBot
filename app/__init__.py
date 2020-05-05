from flask import Flask
from app.chatterbot_api.get_response import bp_response
from app.view.wechat import bp_wechat


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    app.register_blueprint(bp_response, url_prefix='/chatterbot')
    app.register_blueprint(bp_wechat)

    return app
