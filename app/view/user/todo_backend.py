from flask import Blueprint

bp_hello_world = Blueprint('helloworld', __name__)


@bp_hello_world.route('/')
def hello_world():
    return 'Hello World!'

# session.add(Label(
#         id=123,
#         name='str',
#         color=0,
#         user_id=1,
#         last_modified='2017-01-01 00:00:00',
#         deleted=False)
#     )
#     session.flush()
