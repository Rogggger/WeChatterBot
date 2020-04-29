from flask import Flask
from flask import Blueprint
from flask import request, jsonify, make_response
from app.chatterbot_api import chatterbot
from app.chatterbot_api.chatterbot import languages
from app.chatterbot_api.chatterbot.trainers import ChatterBotCorpusTrainer
from app.chatterbot_api.chatterbot.storage.sql_storage_new import SQLStorageAdapterNew
import logging
import json

bp_manager = Blueprint('/admin', __name__)
db = SQLStorageAdapterNew(database_uri='sqlite:///db.sqlite3')


@bp_manager.route('/test')
def test():
    return "Hello, Conversation Manager"


@bp_manager.route('/init_db')
def init_db():
    db.create_rule(
        id=1,
        text="test rule",
        in_response_to="rule 1!"
    )
    db.create_rule(
        text="search test rule",
        in_response_to="rule 2!"
    )
    db.create_rule(
        text="search test rule 2",
        in_response_to="rule 3!"
    )
    db.create_rule(
        text="update test rule",
        in_response_to="rule 4!"
    )
    db.create_rule(
        text="delete test rule",
        in_response_to="rule 5!"
    )
    db.create_text(
        text="test statement",
        in_response_to="statement 1!"
    )
    db.create_text(
        text="search test statement",
        in_response_to="statement 2!"
    )
    db.create_text(
        text="search test statement",
        in_response_to="statement 3!"
    )
    db.create_text(
        text="update test statement",
        in_response_to="statement 4!"
    )
    db.create_text(
        text="delete test statement",
        in_response_to="statement 5!"
    )
    db.create_text(
        text="text statement with tags",
        in_response_to="cant live without tags",
        tags=["test"]
    )

    data = {
        'r_num': db.count('statementrules'),
        's_num': db.count('statement')
    }
    return _make_response(data)


def _make_response(data):
    res = make_response(data)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    # print(res)
    return res


@bp_manager.route('/login')
def admin_login():
    username = request.args.get("username")
    password = request.args.get("password")
    data = {'code': 0, 'username': username}
    if username == 'wechatterbot' and password == 'buaawechatterbot':
        data['code'] = 1
        return _make_response(data)
    else:
        data['code'] = 0
        data['username'] = ''
        return _make_response(data)


@bp_manager.route('/get_user/<user_id>')
def get_user(user_id):
    data = {'code': 0, 'username': 'wechatterbot'}
    if user_id == 1:
        return _make_response(data)
    else:
        data['username'] = ''
        return _make_response(data)


@bp_manager.route('/create_statement', methods=['POST'])
def create():
    data=json.loads(request.get_data(as_text=True))
    print(data['text'])
    text = data['text']
    response = data['response']
    tags = data['tags']
    search_text = data['text']
    search_response = data['response']
    tag_list = tags.split('+')

    # 调用数据接口
    code = 0
    new_statement = {}

    # 调用数据接口
    result = {'code': code, 'statement': new_statement}
    return _make_response(result)


@bp_manager.route('/create_rule', methods=['POST'])
def create_rule():
    post_text = request.form['text']
    post_response = request.form['response']
    # 调用数据接口
    code = 0
    new_rule = {}

    # 调用数据接口
    data = {'code': code, 'statement': new_rule}
    return _make_response(data)


@bp_manager.route('/update_statement', methods=['POST'])
def update():
    data = json.loads(request.get_data(as_text=True))
    print(data['text'])
    id = data['id']
    text = data['text']
    response = data['response']
    tags = data['tags']
    search_text = data['text']
    search_response = data['response']
    tag_list = tags.split('+')
    # 调用数据接口
    code = 0
    new_statement = {}

    # 调用数据接口
    result = {'code': code, 'statement': new_statement}
    return _make_response(result)


@bp_manager.route('/update_rule', methods=['POST'])
def update_rule():
    post_id = request.form['id']
    post_text = request.form['text']
    post_response = request.form['response']
    # 调用数据接口
    code = 0
    new_rule = {}

    # 调用数据接口
    data = {'code': code, 'statement': new_rule}
    return _make_response(data)


@bp_manager.route('/search_statement')
def query():
    s_text = request.args.get("text")
    s_id = request.args.get("id")
    # logging.info("aass")
    # 调用数据接口
    code = 0
    number = 0
    statements = []

    # 调用数据接口
    data = {'code': code, 'number': number, 'statements': statements}
    return _make_response(data)


@bp_manager.route('/search_rule')
def query_rule():
    r_text = request.args.get("text")
    r_id = request.args.get("id")
    # 调用数据接口
    code = 0
    number = 0
    rules = []

    # 调用数据接口
    data = {'code': code, 'number': number, 'rules': rules}
    return _make_response(data)


@bp_manager.route('/delete_statement')
def delete_statement():
    statement_id = request.args.get("sid")
    # 调用数据接口
    code = 1

    # 调用数据接口
    data = {'code': code}
    return _make_response(data)


@bp_manager.route('/delete_rule')
def delete_rule():
    rule_id = request.args.get("rid")
    # 调用数据接口
    code = 1

    # 调用数据接口
    data = {'code': code}
    return _make_response(data)


@bp_manager.route('/delete_all_statement')
def delete_all_statement():
    statement_text = request.args.get("text")
    # 调用数据接口
    number = 0

    # 调用数据接口
    data = {'code': 0, 'number': number}
    if number > 0:
        data['code'] = 1
    return _make_response(data)


@bp_manager.route('/delete_all_rule')
def delete_all_rule():
    rule_text = request.args.get("text")
    # 调用数据接口
    number = 0

    # 调用数据接口
    data = {'code': 0, 'number': number}
    if number > 0:
        data['code'] = 1
    return _make_response(data)