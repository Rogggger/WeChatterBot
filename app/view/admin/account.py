#  coding: utf-8

from flask_login import login_required
from flask import Blueprint, request
from app.libs.db import session
from app.serializer.account import AccountParaSchema
from app.decorator.auth import province_required
from app.libs.http import jsonify
from app.model.user import User
from app.libs.http import error_jsonify

bp_admin_user = Blueprint('admin_user', __name__, url_prefix='/admin/user')


@bp_admin_user.route("/", methods=["GET"])
@login_required
@province_required
def get():
    user_list = User.query.all()
    json = AccountParaSchema(many=True).dump(user_list).data
    return jsonify(json)


@bp_admin_user.route("/<int:pk>/", methods=["POST"])
@login_required
@province_required
def modify(pk):
    json = request.json
    data, error = AccountParaSchema(exclude=('is_admin', 'id', 'area')).load(json)
    if error:
        return error_jsonify(10000001, error)

    user = User.query.filter_by(id=pk).first()
    if user is None:
        return error_jsonify(10000012)
    for k, v in data.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    return jsonify({})


@bp_admin_user.route("/<int:pk>/", methods=["DELETE"])
@login_required
@province_required
def delete(pk):
    user = User.query.filter_by(id=pk).first()
    if user is None:
        return error_jsonify(10000012)
    session.delete(user)
    session.commit()
    return jsonify({})
