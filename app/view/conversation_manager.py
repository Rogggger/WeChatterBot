from flask import Blueprint
from flask import request
import json
from app.chatterbot.conversation import Statement
from app.chatterbot.conversation import StatementRules
from app.libs.chatbot import chatbot
from app.libs.http import error_jsonify, jsonify
import traceback
import time
import base64
import hmac

bp_manager = Blueprint('admin', __name__, url_prefix='/admin')
db = chatbot.storage
dictionary = {'wechatterbot': b'buaa'}


def _statement2dict(s):
    return {
        'id': s.id,
        'text': s.text,
        'in_response_to': s.in_response_to,
        'search_text': s.search_text,
        'search_in_response_to': s.search_in_response_to,
        'tags': s.get_tags()
    }


def _rule2dict(r):
    return {
        'id': r.id,
        'text': r.text,
        'in_response_to': r.in_response_to,
        'search_text': r.search_text,
        'search_in_response_to': r.search_in_response_to,
    }


def get_db():
    return db


def generate_token(key, expire_time=86400):
    # expire_time:1天
    ts_str = str(time.time() + expire_time)
    ts_byte = ts_str.encode("utf-8")
    sha1_ts = hmac.new(key, ts_byte, 'sha1').hexdigest()
    token = ts_str+':'+sha1_ts
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def certify_token(username, token):
    if username not in dictionary:
        return False, error_jsonify(10000044, status_code=401)
    key = dictionary[username]
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False, error_jsonify(10000042, status_code=401)
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token 过期
        return False, error_jsonify(10000043, status_code=401)
    known_sha1_ts = token_list[1]
    sha1 = hmac.new(key, ts_str.encode('utf-8'), 'sha1')
    calc_sha1_ts = sha1.hexdigest()
    if calc_sha1_ts != known_sha1_ts:
        # token 验证不成功
        return False, error_jsonify(10000044, status_code=401)
    # token certification success
    data = {'result': 'success'}
    return True, jsonify(data)


@bp_manager.route('/certify', methods=['POST'])
def check_user():
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)
    check_keys = ('username', 'token')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)
    username = data['username']
    b, result = certify_token(
        username,
        data['token'].encode('utf-8')
    )
    if b:
        return jsonify({'code': 1})
    else:
        return result


@bp_manager.route('/login', methods=['GET'])
def admin_login():
    username = request.args.get("username")
    password = request.args.get("password")
    if password is None or password == '':
        return error_jsonify(10000001)
    if username is None or username == '':
        return error_jsonify(10000001)

    if username == 'wechatterbot':
        if password == 'buaawechatterbot':
            data = {
                'username': username,
                'userId': 1,
                'token': generate_token(dictionary[username])
            }
            return jsonify(data)
        else:
            return error_jsonify(10000013)
    else:
        return error_jsonify(10000012)


@bp_manager.route('/create_statement', methods=['POST'])
def create():
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('text', 'response', 'username', 'token')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)
    b, result = certify_token(
        data['username'],
        data['token'].encode('utf-8')
    )
    if not b:
        return result

    s_text = data['text']
    s_response = data['response']
    if s_text == '' or s_response == '':
        return error_jsonify(10000045)
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
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('text', 'response', 'username', 'token')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)
    b, result = certify_token(
        data['username'],
        data['token'].encode('utf-8')
    )
    if not b:
        return result

    r_text = data['text']
    r_response = data['response']
    if r_text == '' or r_response == '':
        return error_jsonify(10000045)
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
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('id', 'text', 'response', 'username', 'token')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)
    b, result = certify_token(
        data['username'],
        data['token'].encode('utf-8')
    )
    if not b:
        return result

    s_id = data['id']
    try:
        int(s_id)
    except Exception:
        return error_jsonify(10000001)
    text = data['text']
    response = data['response']
    if text == '' or response == '':
        return error_jsonify(10000045)
    if s_id == '':
        return error_jsonify(10000046)
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
    try:
        data = json.loads(request.get_data(as_text=True))
    except ValueError:
        return error_jsonify(10000041)
    except Exception:
        traceback.print_exc()
        return error_jsonify(10000002)

    check_keys = ('id', 'text', 'response', 'username', 'token')
    if not all(k in data for k in check_keys):
        return error_jsonify(10000001)
    b, result = certify_token(
        data['username'],
        data['token'].encode('utf-8')
    )
    if not b:
        return result

    r_id = data['id']
    try:
        int(r_id)
    except Exception:
        return error_jsonify(10000001)
    text = data['text']
    response = data['response']
    if text == '' or response == '':
        return error_jsonify(10000045)
    if r_id == '':
        return error_jsonify(10000046)

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

    token = request.args.get("token")
    username = request.args.get("username")
    if token is None or token == '':
        return error_jsonify(10000001, status_code=400)
    if username is None or username == '':
        return error_jsonify(10000001, status_code=400)

    # 调用数据接口
    if s_id is not None and s_id != '':
        try:
            int(s_id)
        except Exception:
            return error_jsonify(10000001)
        statements = list(db.filter_text(id=s_id))
    elif s_text is not None and s_text != '':
        statements = list(db.filter_text(text=s_text))
    else:
        return error_jsonify(10000001)

    b, result = certify_token(username, token.encode('utf-8'))
    if not b:
        return result

    number = len(statements)
    code = 1

    dict_statements = []
    for s in statements:
        # print(s.text)
        s = db.Session().merge(s)
        dict_statements.append(_statement2dict(s))

    # 调用数据接口
    data = {'code': code, 'number': number, 'statements': dict_statements}
    # print(data)
    return jsonify(data)


@bp_manager.route('/search_rule', methods=['GET'])
def query_rule():
    r_text = request.args.get("text")
    r_id = request.args.get("id")

    token = request.args.get("token")
    username = request.args.get("username")
    if token is None or token == '':
        return error_jsonify(10000001, status_code=400)
    if username is None or username == '':
        return error_jsonify(10000001, status_code=400)
    # 调用数据接口

    if r_id != ''and r_id is not None:
        try:
            int(r_id)
        except Exception:
            return error_jsonify(10000001)
        rules = list(db.filter_rules(id=r_id))
    elif r_text != ''and r_text is not None:
        rules = list(db.filter_rules(text=r_text))
    else:
        return error_jsonify(10000001)
    b, result = certify_token(username, token.encode('utf-8'))
    if not b:
        return result
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
    token = request.args.get("token")
    username = request.args.get("username")
    if token is None or token == '':
        return error_jsonify(10000001, status_code=400)
    if username is None or username == '':
        return error_jsonify(10000001, status_code=400)
    if statement_id == '' or statement_id is None:
        return error_jsonify(10000001)
    b, result = certify_token(username, token.encode('utf-8'))
    if not b:
        return result
    try:
        int(statement_id)
    except Exception:
        return error_jsonify(10000001)
    # 调用数据接口
    code = 1
    db.remove_text_by_id(statement_id)

    # 调用数据接口
    data = {'code': code}
    return jsonify(data)


@bp_manager.route('/delete_rule', methods=['GET'])
def delete_rule():
    token = request.args.get("token")
    username = request.args.get("username")
    if token is None or token == '':
        return error_jsonify(10000001, status_code=400)
    if username is None or username == '':
        return error_jsonify(10000001, status_code=400)
    b, result = certify_token(username, token.encode('utf-8'))
    if not b:
        return result
    rule_id = request.args.get("rid")
    if rule_id == '' or rule_id is None:
        return error_jsonify(10000001)
    try:
        int(rule_id)
    except Exception:
        return error_jsonify(10000001)
    # 调用数据接口
    code = 1
    db.remove_rules_by_id(rule_id)

    # 调用数据接口
    data = {'code': code}
    return jsonify(data)
