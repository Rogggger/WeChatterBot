#  coding: utf-8

from flask_login import login_required

from flask import Blueprint, request
from marshmallow import Schema, fields
from app.libs.http import jsonify, error_jsonify
from app.model.data_collection import DataCollection
from app.model.corporate_Info import Info
from app.model.report_time import ReportTime


# 趋势信息获取，得到所有给定企业名称的趋势

bp_admin_trend = Blueprint('admin_trend', __name__, url_prefix='/admin/trend')


class SummaryParaSchema(Schema):
    name = fields.String()


@bp_admin_trend.route("/", methods=['POST'])
@login_required
def trend_get():
    json = request.get_json()
    data, errors = SummaryParaSchema().load(json)
    if errors:
        return error_jsonify(10000001, errors)
    tmp_user = Info.query.filter_by(name=data['name']).first()  # 找到企业姓名对应的user_id
    if tmp_user is None:
        return error_jsonify(10000019)
    data_list = DataCollection.query.filter_by(user_id=tmp_user.user_id).all()  # 找到所有的填报信息
    res = []
    for i in data_list:
        if i.status == 0 or i.status == 1 or i.status == 4:
            continue
        tmp = {}
        time = ReportTime.query.filter_by(id=i.time_id).first()
        amount = int(float(i.check - i.filing) / i.check * 100)
        st_time = time.start_time.date().strftime("%Y-%m-%d")
        ed_time = time.end_time.date().strftime("%Y-%m-%d")
        tmp['amount'] = amount
        tmp['date'] = st_time + '-->' + ed_time
        res.append(tmp)
    return jsonify(res)
