from flask import Blueprint
from flask import request
import json
from app.chatterbot.conversation import Statement
from app.chatterbot.conversation import StatementRules
from app.libs.chatbot import chatbot
from app.libs.http import error_jsonify, jsonify
import traceback

bp_manager = Blueprint('admin', __name__, url_prefix='/admin')
db = chatbot.storage


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


@bp_manager.route('/login', methods=['GET'])
def admin_login():
    data = request.args
    check_keys = ('username', 'password')
    keys = ('username', 'password')
    req = {k: data[k] for k in keys if data.get(k) is not None}
    if not all(k in req for k in check_keys):
        return error_jsonify(10000001)

    data = {'username': req['username'], 'userId': 1}
    if req['username'] == 'wechatterbot':
        if req['password'] == 'buaawechatterbot':
            return jsonify(data)
        else:
            return error_jsonify(10000013)
    else:
        return error_jsonify(10000012)


@bp_manager.route('/create_statement', methods=['POST'])
def create():
    data = {}
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('text', 'response')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)

    s_text = data['text']
    s_response = data['response']
    tag_list = []
    if 'tags' in data:
        tags = data['tags']
        tag_list = tags.split('+')
    # 调用数据接口
    code = 0
    new_statement = db.create_text(
        text=s_text,
        in_response_to=s_response,
        tags=tag_list
    )

    if new_statement is None:
        code = 0
    else:
        code = 1

    # 调用数据接口
    result = {'code': code, 'statement': _statement2dict(new_statement)}
    return jsonify(result)


@bp_manager.route('/create_rule', methods=['POST'])
def create_rule():
    data = {}
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('text', 'response')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)

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
    return jsonify(data)


@bp_manager.route('/update_statement', methods=['POST'])
def update():
    data = {}
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('id', 'text', 'response')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)
    s_id = data['id']
    text = data['text']
    response = data['response']
    tag_list = []
    if 'tags' in data:
        tags = data['tags']
        tag_list = tags.split('+')
    # 调用数据接口
    code = 1
    new_statement = Statement(
        text=text, in_response_to=response, id=s_id, tags=tag_list)
    db.update_text(new_statement)
    # 调用数据接口
    result = {'code': code, 'statement': _statement2dict(new_statement)}
    return jsonify(result)


@bp_manager.route('/update_rule', methods=['POST'])
def update_rule():
    data = {}
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('text', 'response', 'id')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)
    r_id = data['id']
    text = data['text']
    response = data['response']

    # 调用数据接口
    code = 1
    new_rule = StatementRules(text=text, in_response_to=response, id=r_id)
    db.update_rule(new_rule)
    # 调用数据接口
    result = {'code': code, 'rule': _rule2dict(new_rule)}
    return jsonify(result)


@bp_manager.route('/search_statement', methods=['GET'])
def query():
    s_text = request.args.get("text")
    s_id = request.args.get("id")
    # 调用数据接口
    if s_id is not None and s_id != '':
        statements = list(db.filter_text(id=s_id))
    elif s_text is not None and s_text != '':
        statements = list(db.filter_text(text=s_text))
    else:
        return error_jsonify(10000001)
    number = len(statements)
    code = 1

    dict_statements = []
    for s in statements:
        # print(s.text)
        dict_statements.append(_statement2dict(s))

    # 调用数据接口
    data = {'code': code, 'number': number, 'statements': dict_statements}
    # print(data)
    return jsonify(data)


@bp_manager.route('/search_rule', methods=['GET'])
def query_rule():
    r_text = request.args.get("text")
    r_id = request.args.get("id")
    # 调用数据接口
    if r_id != ''and r_id is not None:
        rules = list(db.filter_rules(id=r_id))
    elif r_text != ''and r_text is not None:
        rules = list(db.filter_rules(text=r_text))
    else:
        return error_jsonify(10000001)
    number = len(rules)
    code = 1

    dict_rules = []
    for r in rules:
        dict_rules.append(_rule2dict(r))

    # 调用数据接口
    data = {'code': code, 'number': number, 'rules': dict_rules}
    return jsonify(data)


@bp_manager.route('/delete_statement', methods=['GET'])
def delete_statement():
    statement_id = request.args.get("sid")
    if statement_id == '' or statement_id is None:
        return error_jsonify(10000001)
    # 调用数据接口
    code = 1
    db.remove_text_by_id(statement_id)

    # 调用数据接口
    data = {'code': code}
    return jsonify(data)


@bp_manager.route('/delete_rule', methods=['GET'])
def delete_rule():
    rule_id = request.args.get("rid")
    if rule_id == '' or rule_id is None:
        return error_jsonify(10000001)
    # 调用数据接口
    code = 1
    db.remove_rules_by_id(rule_id)

    # 调用数据接口
    data = {'code': code}
    return jsonify(data)
