# coding: utf-8
from flask import Blueprint
from app.model.notice import Notice
from app.model.user import User
from flask_login import login_required, current_user
from app.serializer.notice import NoticeParaSchema
from app.libs.http import jsonify

bp_notification = Blueprint(
    "notification", __name__, url_prefix="/notification")


@bp_notification.route("/", methods=['GET'])
@login_required
def notification_get():
    user_id_list = User.query.filter(
        User.isAdmin >= current_user.isAdmin).with_entities(User.id)
    notice_list = Notice.query.filter(Notice.user_id.in_(user_id_list)).all()
    notice_json, errors = NoticeParaSchema(many=True).dump(notice_list)
    return jsonify(notice_json)
