# Storage Adapter New相关说明
    Storage Adapter New是根据Wechatterbot的需求定义的Storage Adapter，主要添加了有关对话规则的处理，目前已实现SQL的Storage Adapter New,且已连接SQLite测试过。

# SQL Storage Adapter New相关接口以及说明

## 相关说明
SQL Storage Adapter New 兼容了SQL Storage Adapter 关于statement的增删改查接口 名字均与SQL Storage Adapter 中接口名字一致。
## 表结构
statement与chatterbot一致，statementrules之包含id,text,in_response_to,search_text,search_in_response_to字段，具体类型可看model.py

## 初始化
需要提供数据库的uri,若不设置则默认uri为'sqlite:///db.sqlite3'


例子：
```python
test = SQLStorageAdapterNew(database_uri='sqlite:///db.sqlite3')
```

## Count
需要输入相对应的表获得当前数据库中相关表的元组数目，目前支持的输入：'statement','tag','statementrules'
接口为count_by_name

例子:
```python
test.count_by_name('statementrules')
test.count_by_name('statement')
```

## Create
对话(statement)创建的函数为create_text,对话规则(statementrules)创建的函数为create_rule
create_text，create_rule中text是必需字段，in_response_to在statementrules中必须写。
create_text，create_rule中id可以不需要（不声明id数据库回把当前最大值id+1赋值给该元组）

例子：
```python
test.create_rule(id=1,
                 text="1",
                 in_response_to="2")
test.create_rule(
                 text="How are you?",
                 in_response_to="I'm fine.")
test.create_text(id=1,
                 text="Hello")
test.create_text(id=2,
                 text="Hello!")
test.create_text(text="How are you?")
```

## Remove
对话以及对话规则删除均提供了三种接口：remove,remove_by_id,remove_by_text
remove:根据输入的结果来删除相关结果
remove_by_id:参数为id，根据id来删除结果
remove_by_text:参数为text，根据text来删除结果

对话相关删除函数:remove_text,remove_text_by_id,remove_text_by_text
对话规则相关删除函数：remove_rules,remove_rules_by_id,remove_rules_by_text

例子：
```python
test.remove_rules_by_id(1)
test.remove_rules_by_text("too young too simple!")
test.remove_rules(id=1)
test.remove_text_by_id(1)
test.remove_text_by_text("too young too simple!")
test.remove_text(id=1)
```

## Update
对话以及对话规则提供的更新接口为update_text(statement),update_rule(statement)
其中statement是一个对话/对话规则对象
如果statement中声明id，则根据id先查找，再将内容更新
若未声明id,则根据text查找，再进行赋值
对话以及对话规则的search_text均会根据text在tagger中查找
若提供了in_response_to,search_in_response_to会根据in_response_to在tagger中查找
建议更新时别空in_response_to

例子：
```python
test.update_text(Statement(text="I am angry.",in_response_to="too young too simple!"))
test.update_text(Statement(text="I am angry.",in_response_to="sometimes naive!",id=1))
test.update_rule(StatementRules(text="I am angry.",in_response_to="too young too simple!"))
test.update_rule(StatementRules(text="I am angry.",in_response_to="too simple!",id=2))
```

## Filter
对话以及对话规则提供的查询接口为filter_text和filter_rules
根据输入的参数进行查找，若不输入参数则返回全部结果

例子：
```python
test.filter_text(text="I am angry.")
test.filter_rules(search_text="I am angry.")
#res为查询的所有结果的list
res=list(test.filter_rules(id=1))
```