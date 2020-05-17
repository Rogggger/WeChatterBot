# WeChatterBot 后端代码
本代码已经基本完成，包括如下三个单元：
1. 微信端
2. 管理员后端
3. chatterbot功能端
4. storage存储端

## 运行方法
使用python 3.7 以上版本安装`requirements.txt`后，运行`python manage.py runserver`，公网测试的话需要将host改为'0.0.0.0'.

如果提示不能`import app.const.keys`的话，需要在`app/const`文件夹下新建`keys.py`，里面的内容是：
~~~
WECHAT_TOKEN = 'xxxxx'
WECHAT_APPID = 'xxxxx'
WECHAT_AESKEY = 'xxxxx'
~~~
缺少微信令牌的后端无法与真正的微信公众号相连，如果你有兴趣，欢迎搭建自己的测试公众号。

## 现在已经完成的api包括
### 1. chatterbot_api
运行服务后，通过 ip/chatterbot/<str:text> 即可得到chatterbot的回复.
例:
http://127.0.0.1:5000/chatterbot/你是谁
### 2. wechat api
### 3. admin backend
