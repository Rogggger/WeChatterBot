from flask import Flask
from app.chatterbot_api.get_response import bp_response
from app.wechat.wechat_app import wx_response
#from app.libs.login import login_manager
#from app.libs.db import db
#from app.view.user.helloworld import bp_hello_world
#from app.view.user.account import bp_account
#from app.view.user.info_record import bp_info
#from app.view.user.data_record import bp_data
#from app.view.user.notification import bp_notification
#from app.view.admin.notification_manage import bp_admin_notification
#from app.view.admin.time_manage import bp_admin_time
#from app.view.admin.summary import bp_admin_summary
#from app.view.admin.datacheck import bp_admin_data_check
#from app.view.admin.trend import bp_admin_trend
#from app.view.admin.compare import bp_admin_compare
#from app.view.admin.sample import bp_admin_sample
#from app.view.admin.info import bp_admin_info
#from app.view.admin.system_info import bp_admin_system
#from app.view.admin.account import bp_admin_user
#from app.view.admin.data import bp_admin_data


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    app.register_blueprint(bp_response, url_prefix='/chatterbot')
    app.register_blueprint(wx_response, url_prefix='/api')
    # app.register_blueprint(bp_hello_world)
    # app.register_blueprint(bp_account)
    # app.register_blueprint(bp_info)
    # app.register_blueprint(bp_data)
    # app.register_blueprint(bp_notification)
    # app.register_blueprint(bp_admin_notification)
    # app.register_blueprint(bp_admin_time)
    # app.register_blueprint(bp_admin_summary)
    # app.register_blueprint(bp_admin_data_check)
    # app.register_blueprint(bp_admin_trend)
    # app.register_blueprint(bp_admin_system)
    # app.register_blueprint(bp_admin_info)
    # app.register_blueprint(bp_admin_compare)
    # app.register_blueprint(bp_admin_sample)
    # app.register_blueprint(bp_admin_user)
    # app.register_blueprint(bp_admin_data)
    # login_manager.init_app(app)
    # db.init_app(app)

    return app
