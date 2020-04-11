#  coding: utf-8
import datetime

from flask_login import login_required, current_user

from flask import Blueprint, request

from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.serializer.notice import NoticeParaSchema
from app.model.notice import Notice

bp_admin_notification = Blueprint('admin_notification', __name__, url_prefix='/admin/notification')


@bp_admin_notification.route("/", methods=["POST"])
@login_required
def notification_manage():  # 管理员设定通知
    if current_user.isAdmin == 0:  # 只能为管理员
        return error_jsonify(10000003)

    json = request.get_json()
    data, errors = NoticeParaSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)
    now = datetime.datetime.now()
    data['created_at'] = now
    data['source'] = '山东省人力资源管理部门'
    data['user_id'] = current_user.id
    new_data = Notice(**data)
    session.add(new_data)
    session.commit()
    return jsonify({})


@bp_admin_notification.route("/", methods=["GET"])
@login_required
def notification_get():  # 管理员获得通知
    if current_user.isAdmin == 0:  # 只能为管理员
        return error_jsonify(10000003)
    if current_user.isAdmin == 2:  # 如果是省级管理员
        res = Notice.query.all()  # 获得所有通知
    if current_user.isAdmin == 1:  # 市级管理员
        res = Notice.query.filter_by(user_id=current_user.id).all()

    data_need, errors = NoticeParaSchema(many=True).dump(res)
    if errors:
        return error_jsonify(10000001, errors)
    return jsonify(data_need)


@bp_admin_notification.route("/<int:id>", methods=["POST"])
@login_required
def notice_manage_id(id):  # 更改管理员获得的通知
    if current_user.isAdmin == 0:  # 只能为管理员
        return error_jsonify(10000003)

    json = request.get_json()
    data, errors = NoticeParaSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)

    data_need = Notice.query.filter_by(id=id)

    if data_need.first() is None:  # 没有这个id，更改失败
        return error_jsonify(10000018)

    data_need.update(data)
    session.commit()
    return jsonify({})


@bp_admin_notification.route("/<int:id>", methods=["DELETE"])
@login_required
def notice_manage_delete(id):  # 删除id对应的通知

    if current_user.isAdmin == 0:  # 只能为管理员
        return error_jsonify(10000003)

    data_need = Notice.query.filter_by(id=id).first()
    if data_need is None:
        return error_jsonify(10000017)

    session.delete(data_need)
    session.commit()
    return jsonify({})
