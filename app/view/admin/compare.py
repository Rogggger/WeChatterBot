#  coding: utf-8

from flask_login import login_required
from flask import Blueprint, request
from marshmallow import Schema, fields
from sqlalchemy import or_
from app.libs.http import jsonify, error_jsonify
from app.model.data_collection import DataCollection
from app.model.report_time import ReportTime

bp_admin_compare = Blueprint('admin_compare', __name__, url_prefix='/admin/compare')


class DataCompareParaSchema(Schema):
    id_1 = fields.Integer()  # 两个要比对的id
    id_2 = fields.Integer()


@bp_admin_compare.route("/", methods=["GET"])  # 得到调查期
@login_required
def data_compare_get():
    time_list = ReportTime.query.all()
    res = []
    for i in time_list:
        tmp = {'start': i.start_time.date().strftime("%Y-%m-%d"), 'end': i.end_time.date().strftime("%Y-%m-%d"),
               'id': i.id}
        res.append(tmp)
    return jsonify(res)


@bp_admin_compare.route("/", methods=["POST"])  # 得到调查期
@login_required
def data_compare():
    json = request.get_json()
    data, errors = DataCompareParaSchema().load(json)

    if errors:
        return error_jsonify(10000001, errors)
    data_list_1 = DataCollection.query.filter(or_(DataCollection.status == 2, DataCollection.status == 3),
                                              DataCollection.time_id == data['id_1']).all()
    data_list_2 = DataCollection.query.filter(or_(DataCollection.status == 2, DataCollection.status == 3),
                                              DataCollection.time_id == data['id_2']).all()
    res = []
    if not data_list_1 or not data_list_2:
        return error_jsonify(10000020)
    tmp_1 = {'sum': 0, 'filing': 0, 'check': 0, 'diff': 0, 'percent': 0}
    for i in data_list_1:
        tmp_1['filing'] = tmp_1['filing'] + i.filing
        tmp_1['check'] = tmp_1['check'] + i.check
    tmp_1['sum'] = len(data_list_1)
    tmp_1['diff'] = tmp_1['check'] - tmp_1['filing']
    tmp_1['percent'] = int(float(tmp_1['diff']) / tmp_1['filing'] * 100)
    res.append(tmp_1)

    tmp_2 = {'sum': 0, 'filing': 0, 'check': 0, 'diff': 0, 'percent': 0}
    for i in data_list_2:
        tmp_2['filing'] = tmp_2['filing'] + i.filing
        tmp_2['check'] = tmp_2['check'] + i.check
    tmp_2['sum'] = len(data_list_2)
    tmp_2['diff'] = tmp_2['check'] - tmp_2['filing']
    tmp_2['percent'] = int(float(tmp_2['diff']) / tmp_2['filing'] * 100)
    res.append(tmp_2)

    return jsonify(res)
