# coding: utf-8
from functools import wraps
from flask_login import current_user
from app.consts.user import (PERMISSION_ENTERPRISE,
                             PERMISSION_CITY,
                             PERMISSION_PROVINCE)
from app.libs.http import error_jsonify


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.isAdmin == PERMISSION_ENTERPRISE:
            return error_jsonify(10000003)
        return func(*args, **kwargs)

    return decorated_view


def province_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.isAdmin != PERMISSION_PROVINCE:
            return error_jsonify(10000003)
        return func(*args, **kwargs)

    return decorated_view


def city_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.isAdmin != PERMISSION_CITY:
            return error_jsonify(10000003)
        return func(*args, **kwargs)

    return decorated_view
