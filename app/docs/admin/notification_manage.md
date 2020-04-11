### 通知管理

### /admin/notification/ POST

传入:

{
    "title":"",    #标题
    "content":"",    #主体
    "created_at":""    #时间
}


传出：
{}

~~~

### /admin/notification/ GET

传入：无

传出：

[
    {
        "title":"",    #标题
        "content":"",    #主体
        "created_at":"",    #时间
        "id":""    #通知id
    },
    {
        "title":"",    #标题
        "content":"",    #主体
        "created_at":"",    #时间
        "id":""    #通知id
    },
    ...
]

### /admin/notification/<int:id> POST

传入：
{
    "title":"",    #标题
    "content":"",    #主体
    "created_at":"",    #时间
    "id":""    #通知id
}

传出：{}

### /admin/notification/<int:id> DELETE

传入：无

传出：{}