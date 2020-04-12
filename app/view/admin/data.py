#  coding: utf-8
from datetime import timedelta
from flask_login import login_required
from flask import request, Blueprint
from marshmallow import Schema, fields, post_load, pre_load
from marshmallow.validate import OneOf
from app.model.user import User
from app.model.data_collection import DataCollection
from app.model.corporate_Info import Info
from app.serializer.data import DataParaSchema
from app.decorator.auth import admin_required
from app.libs.http import error_jsonify
from app.libs.http import jsonify
from app.libs.db import session


# 数据汇总
bp_admin_data = Blueprint('admin_data', __name__, url_prefix='/admin/data')


class DataSearchSchema(Schema):
    select_list = ['name', 'area', 'enterprise_kind', 'belong_to', 'user_name', 'user_is_admin', 'status',
                   'start_at', 'end_at', 'month', 'season']
    select = fields.String(required=True, validate=OneOf(select_list))
    condition = fields.String()
    time = fields.Date(missing='1980-01-01')

    @pre_load
    def pre_select(self, json):
        if not json['time']:
            json.pop('time')
        return json

    @post_load
    def import_select(self, data):
        user_list = ['user_name', 'user_is_admin']
        data_list = ['status', 'start_at', 'end_at', 'month', 'season']
        info_list = ['name', 'area', 'enterprise_kind', 'belong_to']
        select = data['select']
        if select in user_list:
            data['class'] = User
            data['select'] = 'name' if select == 'user_name' else 'isAdmin'
        elif select in data_list:
            data['class'] = DataCollection
        elif select in info_list:
            data['class'] = Info
            if select == 'enterprise_kind':
                data['select'] = 'enterprise'
                data['condition'] = u'{}%'.format(data['condition'])
        return data


@bp_admin_data.route("/", methods=["POST"])
@login_required
@admin_required
def data_search():
    json = request.get_json()
    data, errors = DataSearchSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)
    klass = data['class']
    select = data['select']
    condition = data['condition']
    time = data['time']
    q = DataCollection.query
    if select == 'start_at':
        q = q.filter(DataCollection.time >= time)
    elif select == 'end_at':
        q = q.filter(DataCollection.time <= time)
    elif select == 'month':
        q = q.filter(DataCollection.time >= time, DataCollection.time <= time + timedelta(days=30))
    elif select == 'season':
        q = q.filter(DataCollection.time >= time, DataCollection.time <= time + timedelta(days=90))
    elif select == 'status':
        q = q.filter_by(status=int(condition))
    else:
        if klass == User:
            co = User.id == DataCollection.user_id
        elif klass == Info:
            co = Info.user_id == DataCollection.user_id
        else:
            raise ValueError('GG')
        q = q.join(klass, co)
        if select == 'enterprise':
            q = q.filter(getattr(klass, select).like(condition))
        else:
            q = q.filter(getattr(klass, select) == condition)
    data_list = q.all()
    json = DataParaSchema(many=True).dump(data_list).data

    return jsonify(json)


@bp_admin_data.route('/<int:pk>', methods=["POST"])
@login_required
@admin_required
def data_modify(pk):
    json = request.get_json()
    data, error = DataParaSchema().load(json)
    if error:
        return error_jsonify(10000001, error)

    data_c = DataCollection.query.filter_by(id=pk).first()
    if data_c is None:
        return error_jsonify(10000018)
    if data_c.status == 5:
        return error_jsonify(10000022)

    data['time'] = data_c.time
    data['time_id'] = data_c.time_id
    data['status'] = data_c.status
    data['user_id'] = data_c.user_id
    data_c.status = 5
    session.add(data_c)
    new_data = DataCollection(**data)
    session.add(new_data)
    session.commit()
    return jsonify({})
