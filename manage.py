from flask_script import Manager, Server
from app import create_app

app = create_app()
manager = Manager(app)

manager.add_command('runserver', Server(
    use_reloader=True,
    host='127.0.0.1',
    port=5000
    # ssl_crt='/etc/letsencrypt/live/yuanw.wang/fullchain.pem',
    # ssl_key='/etc/letsencrypt/live/yuanw.wang/privkey.pem'
)
)

if __name__ == '__main__':
    manager.run()
