from flask import Flask
<<<<<<< HEAD
=======
#from app.chatterbot_api.get_response import bp_response
from app.chatterbot_api.conversation_manager import bp_manager
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
>>>>>>> 8f21cf7... add conversation manager

from app.view.get_response import bp_response
from app.view.wechat import bp_wechat

<<<<<<< HEAD
=======
def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    app.debug=True
>>>>>>> ada9325... add create_statement & delete method

<<<<<<< HEAD
def create_app():
    app = Flask(__name__)
=======
    #app.register_blueprint(bp_response,url_prefix='/chatterbot')
    app.register_blueprint(bp_manager, url_prefix='/admin')
    #app.register_blueprint(bp_account)
    #app.register_blueprint(bp_info)
    #app.register_blueprint(bp_data)
    #app.register_blueprint(bp_notification)
    #app.register_blueprint(bp_admin_notification)
    #app.register_blueprint(bp_admin_time)
    #app.register_blueprint(bp_admin_summary)
    #app.register_blueprint(bp_admin_data_check)
    #app.register_blueprint(bp_admin_trend)
    #app.register_blueprint(bp_admin_system)
    #app.register_blueprint(bp_admin_info)
    #app.register_blueprint(bp_admin_compare)
    #app.register_blueprint(bp_admin_sample)
    #app.register_blueprint(bp_admin_user)
    #app.register_blueprint(bp_admin_data)
>>>>>>> 8f21cf7... add conversation manager

    app.register_blueprint(bp_response)
    app.register_blueprint(bp_wechat)

    return app
