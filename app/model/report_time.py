# coding: utf-8
from sqlalchemy import Column, Integer, Sequence, DateTime
from app.libs.db import db


# 记录数据填报时间段
class ReportTime(db.Model):
    id = Column(Integer, Sequence('time_id'), primary_key=True, autoincrement=True)
    start_time = Column(DateTime, nullable=False, default='1980-01-01 00:00:00', doc=u'填报开始时间')
    end_time = Column(DateTime, nullable=False, default='1980-01-01 00:00:00', doc=u'填报结束时间')
    user_id = Column(Integer, nullable=False, doc=u'此填报时间创始人')
