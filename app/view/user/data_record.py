#  coding: utf-8
import datetime

from flask_login import login_required, current_user
from sqlalchemy import and_
from flask import Blueprint, request
from marshmallow import Schema, fields

from app.model.data_collection import DataCollection
from app.model.report_time import ReportTime
from app.model.user import User
from app.model.corporate_Info import Info
from app.libs.http import jsonify, error_jsonify
from app.libs.db import session
from app.serializer.data import DataParaSchema

# 企业数据填报
bp_data = Blueprint("data", __name__, url_prefix="/data")


class DataGetParaSchema(Schema):
    start = fields.DateTime()  # 结束时间
    end = fields.DateTime()  # 开始时间


@bp_data.route("/record", methods=['POST'])
@login_required
def info_record():
    json = request.get_json()
    data, errors = DataParaSchema().load(json)

    if errors:
        return error_jsonify(10000001, errors)
    tmp_info = Info.query.filter_by(user_id=current_user.id).first()  # 找到企业信息中是否有当前用户的信息
    if tmp_info is None:
        return error_jsonify(10000021)

    now = datetime.datetime.now()
    data['time'] = now
    admin_user = User.query.filter_by(isAdmin=2).first()  # 找到省管理员账户id
    report_time = ReportTime.query.filter(and_(ReportTime.user_id == admin_user.id, ReportTime.start_time <= now,
                                               ReportTime.end_time >= now)).first()
    # 找到省级管理员设置的提交时间中符合条件的
    if report_time:  # 如果在当前时间段
        tmp_data = DataCollection.query.filter_by(user_id=current_user.id, time_id=report_time.id)
        # 找到企业填报的符合条件的数据
        if tmp_data.first():  # 修改企业条目，并保存
            if tmp_data.first().status != 0:
                return error_jsonify(10000016)
            tmp_data.update(data)
            session.commit()
        else:  # 新建一个企业填报条目，并保存
            data['time_id'] = report_time.id
            data['status'] = 0
            data['user_id'] = current_user.id
            new_data = DataCollection(**data)
            session.add(new_data)
            session.commit()
    else:  # 现在不在任何可以填报的时间段内
        return error_jsonify(10000014)
    return jsonify({})


@bp_data.route("/get", methods=['GET'])
@login_required
def info_record_get():
    now = datetime.datetime.now()
    admin_user = User.query.filter_by(isAdmin=2).first()  # 找到省管理员账户id
    report_time = ReportTime.query.filter(and_(ReportTime.user_id == admin_user.id, ReportTime.start_time <= now,
                                               ReportTime.end_time >= now)).first()
    if report_time:
        tmp_data = DataCollection.query.filter_by(user_id=current_user.id, time_id=report_time.id).first()
        # 找到企业填报的符合条件的数据
        if tmp_data:
            data_need, errors = DataParaSchema(exclude=('id', 'name')).dump(tmp_data)
            return jsonify(data_need)
    else:
        return jsonify({})


@bp_data.route("/report", methods=['POST'])
@login_required
def info_report():
    json = request.get_json()
    data, errors = DataParaSchema().load(json)

    if errors:
        return error_jsonify(10000001, errors)

    tmp_info = Info.query.filter_by(user_id=current_user.id).first()  # 找到企业信息中是否有当前用户的信息
    if tmp_info is None:
        return error_jsonify(10000021)

    now = datetime.datetime.now()
    data['time'] = now
    admin_user = User.query.filter_by(isAdmin=2).first()  # 找到省管理员账户id
    report_time = ReportTime.query.filter(and_(ReportTime.user_id == admin_user.id, ReportTime.start_time <= now,
                                               ReportTime.end_time >= now)).first()
    # 找到省级管理员设置的提交时间中符合条件的
    if report_time:  # 如果在当前时间段
        tmp_data = DataCollection.query.filter_by(user_id=current_user.id, time_id=report_time.id)
        # 找到企业填报的符合条件的数据
        if tmp_data:  # 上报
            if tmp_data.first().status != 0:
                return error_jsonify(10000016)
            data['status'] = 1
            tmp_data.update(data)
            session.commit()
        else:  # 没有找到说明没有保存
            return error_jsonify(10000015)
    else:  # 现在不在任何可以填报的时间段内
        return error_jsonify(10000014)
    return jsonify({})


@bp_data.route("/record", methods=['GET'])
@login_required
def info_get():
    args = request.args
    data, errors = DataGetParaSchema().load(args)
    if errors:
        return error_jsonify(10000001)

    res = DataCollection.query.filter(
        and_(DataCollection.user_id == current_user.id, DataCollection.time >= data['start'],
             DataCollection.time <= data['end'])).all()
    data_need, errors = DataParaSchema(many=True, exclude=('id', 'name')).dump(res)
    if errors:
        return error_jsonify(10000001)
    return jsonify(data_need)
