# WeChatterBot 后端代码
本代码已经基本完成，主要包括如下四个单元：
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
运行服务后，通过 ip/chatterbot/<str:text> 即可得到chatterbot的回复。我们的压力测试是在这个URL上进行的。
例:
http://127.0.0.1:5000/chatterbot/你是谁
### 2. wechat api
具体可以查看我们组需求分析文档的外部接口部分，[点击这里](https://github.com/bhsei/20_E/blob/master/%E5%AE%9E%E9%AA%8C1%EF%BC%9A%E8%BD%AF%E4%BB%B6%E9%9C%80%E6%B1%82%E5%88%86%E6%9E%90/E_%E8%BD%AF%E4%BB%B6%E9%9C%80%E6%B1%82%E5%88%86%E6%9E%90%E8%AF%B4%E6%98%8E%E4%B9%A6_V3.0.0.docx)
### 3. admin backend
具体可以查看我们组单独的admin部分接口文档，[点击这里](https://github.com/bhsei/20_E/blob/master/%E5%AE%9E%E9%AA%8C3%EF%BC%9A%E8%BD%AF%E4%BB%B6%E4%BA%A7%E5%93%81%E6%94%B9%E8%BF%9B%E4%B8%8E%E5%B1%95%E7%A4%BA/%E7%BB%B4%E6%8A%A4%E4%BA%BA%E5%91%98%E7%95%8C%E9%9D%A2%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E.docx)

## 单元测试和代码覆盖率统计方法
如果你使用Pycharm，在配置好python环境后，直接右键单击项目底的tests文件夹，选择运行`Test: tests`即可自动运行单元测试。代码覆盖率也可以直接通过Pycharm的coverage执行功能进行测试，也即右键单击tests文件夹，选择运行`Coverage Test: tests`即可。

如果是CLI，你需要安装`unittest`包进行单元测试：`python -m unittest tests`；安装`coverag`e包进行代码覆盖率测试：`python -m coverage run tests/a.py`。更多高阶用法请参考[官方文档](https://coverage.readthedocs.io/en/latest/)

需要注意的是，本项目**仅在**Pycharm下的单元测试和覆盖率测试通过，如果因为系统路径等问题导致的测试失败不在本项目的考虑范围内。
