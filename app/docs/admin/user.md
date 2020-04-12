### 用户管理：

### /admin/user/ GET
得到所有的User

传入

- 无


传出：
~~~
[
    {
        "id": 1,
        "password_md5": "123456",
        "is_admin": 2,
        "email": "sheng",
        "area": "0531"
    },
    {
        "id": 2,
        "password_md5": "654321",
        "is_admin": 1,
        "email": "qiye",
        "area": "0532"
    }
]
~~~

### /admin/user/\<int:id\> POST
更改用户信息

传入

- email: str 用户的用户名
- password_md5: str 用户的密码
- area: str 用户所在市

示例
~~~
{
        "password_md5": "654321",
        "email": "qiye",
        "area": "0532"
}
~~~
传出：
~~~
{}  # 表示成功
~~~


### /admin/user/\<int:id\> DELETE
删除用户信息（谨慎操作）

传入

- 无

传出：
~~~
{}  # 表示成功
~~~
