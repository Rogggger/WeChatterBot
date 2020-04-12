# coding: utf-8
from marshmallow import Schema, fields, pre_dump, post_load


class AccountParaSchema(Schema):
    email = fields.String(required=True)
    password_md5 = fields.String(required=True, validate=lambda x: len(x) >= 6)
    is_admin = fields.Integer(required=True)
    area = fields.String(required=True)
    id = fields.Integer()

    @pre_dump
    def export_user(self, obj):
        obj.email = obj.name
        obj.password_md5 = obj.password
        obj.is_admin = obj.isAdmin

    @post_load
    def import_user(self, data):
        data['name'] = data.pop('email')
        data['password'] = data.pop('password_md5')
        if 'is_admin' in data:
            data['isAdmin'] = data.pop('is_admin')
