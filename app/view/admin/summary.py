#  coding: utf-8

from flask_login import login_required
from flask import request, Blueprint
from marshmallow import Schema, fields
from app.model.data_collection import DataCollection
from app.model.report_time import ReportTime
from app.libs.http import error_jsonify
from app.model.corporate_Info import Info
from app.libs.http import jsonify

# 数据汇总
bp_admin_summary = Blueprint('admin_summary', __name__, url_prefix='/admin/summary')


class SummaryParaSchema(Schema):
    name = fields.String()


@bp_admin_summary.route("/", methods=["POST"])
@login_required
def data_summary():  # 数据汇总,只汇总给定企业名称，且通过了审核的信息
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
        tmp = {'filing': i.filing, 'check': i.check, 'diff': i.check - i.filing}
        time = ReportTime.query.filter_by(id=i.time_id).first()
        tmp['start'] = time.start_time.date().strftime("%Y-%m-%d")
        tmp['end'] = time.end_time.date().strftime("%Y-%m-%d")
        res.append(tmp)

    return jsonify(res)
