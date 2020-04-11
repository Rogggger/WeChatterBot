from flask import Blueprint

bp_hello_world = Blueprint('helloworld', __name__)


@bp_hello_world.route('/')
def hello_world():
    return 'Hello World!'
