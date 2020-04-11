# coding: utf-8
import binascii
import hashlib

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Sequence
from app.libs.db import db


class User(db.Model, UserMixin):
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # 姓名
    password = Column(String(200), nullable=False)  # 密码
    isAdmin = Column(Integer, nullable=False)  # 管理员权限
    salt = Column(String(50))
    area = Column(String(5))  # 所属市的代码

    @classmethod
    def is_exist(cls, name, area):
        res = cls.query.filter_by(name=name, area=area).all()
        if res:
            return True
        return False

    def has_right_password(self, password_md5):
        # We don't use salt now:
        # new_password = self.__class__.get_hashed_password(password_md5, self.salt)
        if password_md5 != self.password:
            return False
        return True

    def set_password_with_salt(self, password_md5, salt):
        self.password = User.get_hashed_password(password_md5, salt)
        self.salt = salt

    @classmethod
    def get_hashed_password(cls, password_md5, salt):
        dk = hashlib.pbkdf2_hmac('sha256', bytes(password_md5), bytes(salt), 100000)
        return str(binascii.hexlify(dk))
