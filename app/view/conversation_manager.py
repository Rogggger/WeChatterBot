from flask import Flask
from flask import Blueprint
from flask import request, jsonify, make_response
from app.chatterbot.storage.sql_storage_new import SQLStorageAdapterNew
from app.chatterbot import languages
import logging
import json
from app.chatterbot.conversation import Statement
from app.chatterbot.conversation import StatementRules

bp_manager = Blueprint('/admin', __name__)
db = SQLStorageAdapterNew(database_uri='sqlite:///db.sqlite3',  tagger_language=languages.CHI)


@bp_manager.route('/test')
def test():
    return "Hello, Conversation Manager"


@bp_manager.route('/init_db')
def init_db():
    db.create_rule(
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
        'r_num': db.count_by_name('statementrules'),
        's_num': db.count_by_name('statement')
    }
    return _make_response(data)


def _make_response(data):
    res = make_response(data)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    # print(res)
    return res


def _statement2dict(s):
    return {
        'id': s.id,
        'text': s.text,
        'in_response_to': s.in_response_to,
        'search_text': s.search_text,
        'search_in_response_to': s.search_in_response_to,
        'tags': s.tags
    }


def _rule2dict(r):
    return {
        'id': r.id,
        'text': r.text,
        'in_response_to': r.in_response_to,
        'search_text': r.search_text,
        'search_in_response_to': r.search_in_response_to,
    }


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
    data = json.loads(request.get_data(as_text=True))
    print(data['text'])
    s_text = data['text']
    s_response = data['response']
    tags = data['tags']
    tag_list = tags.split('+')

    # 调用数据接口
    code = 0
    new_statement = db.create_text(
        text=s_text,
        in_response_to=s_response,
        tags=tag_list
    )

    # new_statement = {'text': s_text, 'in_response_to': s_response, 'tags': tags}
    if new_statement is None:
        code = 0
    else:
        code = 1

    # 调用数据接口
    result = {'code': code, 'statement': _statement2dict(new_statement)}
    return _make_response(result)


@bp_manager.route('/create_rule', methods=['POST'])
def create_rule():
    data = json.loads(request.get_data(as_text=True))
    r_text = data['text']
    r_response = data['response']
    # 调用数据接口
    code = 0
    new_rule = db.create_rule(
        text=r_text,
        in_response_to=r_response
    )
    # new_rule = {'text': r_text, 'in_response_to': r_response}
    if new_rule is None:
        code = 0
    else:
        code = 1

    # 调用数据接口
    data = {'code': code, 'rule': _rule2dict(new_rule)}
    return _make_response(data)


@bp_manager.route('/update_statement', methods=['POST'])
def update():
    data = json.loads(request.get_data(as_text=True))
    s_id = data['id']
    text = data['text']
    response = data['response']
    tags = data['tags']
    tag_list = tags.split('+')
    # 调用数据接口
    code = 1
    new_statement = Statement(text=text, in_response_to=response, id=s_id, tags=tag_list)
    db.update_text(new_statement)
    # db.update_text(Statement(text="I am angry.", in_response_to="sometimes naive!", id=1))
    # 调用数据接口
    result = {'code': code}
    return _make_response(result)


@bp_manager.route('/update_rule', methods=['POST'])
def update_rule():
    data = json.loads(request.get_data(as_text=True))
    r_id = data['id']
    text = data['text']
    response = data['response']

    # 调用数据接口
    code = 1
    new_rule = StatementRules(text=text, in_response_to=response, id=r_id)
    db.update_rule(new_rule)
    # db.update_text(Statement(text="I am angry.", in_response_to="sometimes naive!", id=1))
    # 调用数据接口
    result = {'code': code}
    return _make_response(result)


@bp_manager.route('/search_statement')
def query():
    s_text = request.args.get("text")
    s_id = request.args.get("id")
    # logging.info("aass")
    # 调用数据接口
    code = 0
    number = 0
    if s_id != '':
        statements = list(db.filter_text(id=s_id))
    else:
        statements = list(db.filter_text(text=s_text))
    number = len(statements)
    code = 1

    dict_statements = []
    for s in statements:
        print(s.text)
        dict_statements.append(_statement2dict(s))

    # 调用数据接口
    data = {'code': code, 'number': number, 'statements': dict_statements}
    # print(data)
    return _make_response(data)


@bp_manager.route('/search_rule')
def query_rule():
    r_text = request.args.get("text")
    r_id = request.args.get("id")
    # 调用数据接口
    code = 0
    number = 0
    if r_id != '':
        rules = list(db.filter_rules(id=r_id))
    else:
        rules = list(db.filter_rules(text=r_text))
    number = len(rules)
    code = 1

    dict_rules = []
    for r in rules:
        dict_rules.append(_rule2dict(r))

    # 调用数据接口
    data = {'code': code, 'number': number, 'rules': dict_rules}
    return _make_response(data)


@bp_manager.route('/delete_statement')
def delete_statement():
    statement_id = request.args.get("sid")
    # 调用数据接口
    code = 1
    db.remove_text_by_id(statement_id)

    # 调用数据接口
    data = {'code': code}
    return _make_response(data)


@bp_manager.route('/delete_rule')
def delete_rule():
    rule_id = request.args.get("rid")
    # 调用数据接口
    code = 1
    db.remove_rules_by_id(rule_id)

    # 调用数据接口
    data = {'code': code}
    return _make_response(data)


@bp_manager.route('/delete_all_statement')
def delete_all_statement():
    statement_text = request.args.get("text")
    # 调用数据接口
    number = len(list(db.filter_text(text=statement_text)))

    # 调用数据接口
    data = {'code': 0, 'number': number}
    if number > 0:
        data['code'] = 1
        db.remove_text_by_text(statement_text)

    return _make_response(data)


@bp_manager.route('/delete_all_rule')
def delete_all_rule():
    rule_text = request.args.get("text")
    # 调用数据接口
    number = len(list(db.filter_rules_by_text(text=rule_text)))

    # 调用数据接口
    data = {'code': 0, 'number': number}
    if number > 0:
        data['code'] = 1
        db.remove_rules_by_text(rule_text)
    return _make_response(data)