from flask import Blueprint
from app.libs.chatbot import chatbot

bp_response = Blueprint('chatterbot', __name__, url_prefix='/chatterbot')


@bp_response.route('/<message>')
def response(message):
    res = chatbot.get_response(message)
    return res.text
