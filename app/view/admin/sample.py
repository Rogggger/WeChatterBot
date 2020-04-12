#  coding: utf-8

from flask_login import login_required
from flask import Blueprint
import app.libs.http
from app.model.user import User

bp_admin_sample = Blueprint('admin_sample', __name__, url_prefix='/admin/sample')


@bp_admin_sample.route("/", methods=["GET"])
@login_required
def sample_get():  # 返回每个地区的企业总数以及占比
    res = []
    user_list = User.query.filter_by(isAdmin=0).all()  # 找到所有企业用户
    area_list = []
    sum = {}
    for i in user_list:
        if i.area in area_list:
            sum[i.area] = sum[i.area] + 1
        else:
            sum[i.area] = 1
            area_list.append(i.area)
    for i in area_list:
        tmp = {'area': i, 'sum': sum[i]}
        res.append(tmp)
    return app.libs.http.jsonify(res)
