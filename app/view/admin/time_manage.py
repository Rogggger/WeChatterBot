#  coding: utf-8
from flask_login import login_required, current_user
from flask import request, Blueprint
from marshmallow import Schema, fields
from app.model.report_time import ReportTime
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session

bp_admin_time = Blueprint('admin_time', __name__, url_prefix='/admin/time')


class TimeParaSchema(Schema):
    start_time = fields.DateTime()  # 结束时间
    end_time = fields.DateTime()  # 开始时间
    id = fields.Integer()  # 时间id


@bp_admin_time.route("/", methods=["POST"])
@login_required
def time_manage():  # 省级管理员设定上交开始时间，结束时间
    json = request.get_json()
    data, errors = TimeParaSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)

    if current_user.isAdmin != 2:  # 只能省级管理员
        return error_jsonify(10000003)
    new_time = ReportTime(start_time=data['start_time'], end_time=data['end_time'], user_id=current_user.id)
    session.add(new_time)
    session.commit()
    return jsonify({})


@bp_admin_time.route("/", methods=["GET"])
@login_required
def time_get():  # 获得所有的设定时间段
    if current_user.isAdmin != 2:  # 只能省级管理员
        return error_jsonify(10000003)

    res = ReportTime.query.all()
    data_need, errors = TimeParaSchema(many=True).dump(res)
    if errors:
        return error_jsonify(10000001)
    return jsonify(data_need)


@bp_admin_time.route("/<int:id>", methods=["POST"])
@login_required
def time_manage_id(id):  # 省级管理员更改上交开始时间，结束时间
    json = request.get_json()
    data, errors = TimeParaSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)

    if current_user.isAdmin != 2:  # 只能省级管理员
        return error_jsonify(10000003)

    data_need = ReportTime.query.filter_by(id=id)
    if data_need.first() is None:
        return error_jsonify(10000018)
    data_need.update(data)
    session.commit()
    return jsonify({})


@bp_admin_time.route("/<int:id>", methods=["DELETE"])
@login_required
def time_manage_delete(id):  # 省级管理员删除时间段

    if current_user.isAdmin != 2:  # 只能省级管理员
        return error_jsonify(10000003)

    data_need = ReportTime.query.filter_by(id=id).first()
    if data_need is None:
        return error_jsonify(10000017)
    session.delete(data_need)
    session.commit()
    return jsonify({})
