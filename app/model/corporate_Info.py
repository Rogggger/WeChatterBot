#  coding: utf-8
from sqlalchemy import Column, Integer, String, Sequence
from app.libs.db import db


class Info(db.Model):
    id = Column(Integer, Sequence('info_id'), primary_key=True, autoincrement=True)
    address = Column(String(100), nullable=False)  # 联系地址
    area = Column(String(100), nullable=False)  # 所属地区
    belong_to = Column(String(100), nullable=False)  # 所属行业
    code = Column(String(20), nullable=False)  # 组织机构代码
    contacts = Column(String(100), nullable=False)  # 联系人
    email = Column(String(50), nullable=True)  # email
    enterprise = Column(String(100), nullable=False)  # 企业性质+企业规模
    fax = Column(String(55), nullable=False)  # 传真
    main_business = Column(String(100), nullable=False)  # 主营业务
    name = Column(String(100), nullable=False)  # 企业名称
    phone = Column(String(100), nullable=False)  # 联系电话
    postal_code = Column(String(100), nullable=False)  # 邮政编码
    user_id = Column(Integer, nullable=False)

    @classmethod
    def is_exist(cls, user_id):
        res = cls.query.filter_by(user_id=user_id).all()
        if res:
            return True
        else:
            return False
