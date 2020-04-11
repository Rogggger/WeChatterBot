#  coding: utf-8

from flask_login import login_required, current_user
from sqlalchemy import and_
from flask import Blueprint, request
from marshmallow import Schema, fields
from app.libs.http import jsonify, error_jsonify
from app.model.data_collection import DataCollection
from app.model.corporate_Info import Info
from app.model.user import User
from app.libs.db import session

bp_admin_data_check = Blueprint('admin_data_check', __name__, url_prefix='/admin/datacheck')


class DataCheckParaSchema(Schema):
    filing = fields.Integer()  # 初次建档时就业人数
    check = fields.Integer()  # 本次调查期就业人数
    other_reason = fields.String(55)  # 其他原因
    decrease_type = fields.String(50)  # 就业人数减少类型
    main_reason = fields.String(50)  # 主要原因
    main_reason_detail = fields.String(100)  # 主要原因说明
    second_reason = fields.String(50)  # 次要原因
    second_reason_detail = fields.String(100)  # 次要原因说明
    third_reason = fields.String(50)  # 第三原因
    third_reason_detail = fields.String(100)  # 第三原因
    id = fields.Integer()  # id


class PassParaSchema(Schema):
    id = fields.Integer()
    status = fields.Integer()
    remark = fields.String()


@bp_admin_data_check.route("/", methods=["GET"])
@login_required
def find_data():  # 返回所有当前用户可以审核的条目
    if current_user.isAdmin == 0:
        return error_jsonify(10000003)
    res = []
    if current_user.isAdmin == 1:
        area = current_user.area
        user_list = User.query.filter_by(area=area).all()  # 找到所有地区相同的user
        for i in user_list:  # 循环
            if i.id == current_user.id:
                continue
            data_tmp = DataCollection.query.filter(
                and_(DataCollection.user_id == i.id, DataCollection.status == 1)).all()  # 找到这个企业填报的信息
            if len(data_tmp) != 0:
                for j in data_tmp:
                    tmp, errors = DataCheckParaSchema().dump(j)
                    res.append(tmp)
        return jsonify(res)
    if current_user.isAdmin == 2:
        data_list = DataCollection.query.filter_by(status=2).all()
        for i in data_list:
            tmp, errors = DataCheckParaSchema().dump(i)
            tmp['name'] = Info.query.filter_by(user_id=i.user_id).first().name
            res.append(tmp)
        return jsonify(res)


@bp_admin_data_check.route("/", methods=["POST"])
@login_required
def pass_or_not():  # 审核是否通过
    json = request.get_json()
    data, errors = PassParaSchema().load(json)

    if errors:
        return error_jsonify(10000001, errors)
    data_need = DataCollection.query.filter_by(id=data['id'])
    if data_need.first() is None:
        return error_jsonify(10000020)
    data_update = {}
    if current_user.isAdmin == 1:  # 市级审核
        if data['status'] == 0:
            data_update['status'] = 4
        else:
            data_update['status'] = 2
    elif current_user.isAdmin == 2:  # 省级审核
        if data['status'] == 0:
            data_update['status'] = 4
        else:
            data_update['status'] = 3
    else:
        return error_jsonify(10000003)
    data_need.update(data_update)
    session.commit()
    return jsonify({})
