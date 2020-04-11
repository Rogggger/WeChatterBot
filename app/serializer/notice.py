# coding: utf-8
from marshmallow import Schema, fields


class NoticeParaSchema(Schema):
    title = fields.String(50)  # 标题
    content = fields.String(2000)  # 主体
    created_at = fields.DateTime()  # 时间
    id = fields.Integer()  # 通知id
