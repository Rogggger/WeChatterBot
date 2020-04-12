# coding: utf-8
from sqlalchemy import Column, Integer, String, Sequence, DateTime, func
from app.libs.db import db


class Notice(db.Model):
    id = Column(Integer, Sequence('info_id'), primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)  # 标题
    content = Column(String(2000), nullable=False)  # 主体
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())  # 时间
    source = Column(String(50), nullable=False)  # 发布单位
    user_id = Column(Integer, nullable=False)

    @classmethod
    def is_exist(cls, user_id):
        res = cls.query.filter_by(user_id=user_id).all()
        if res:
            return True
        else:
            return False
