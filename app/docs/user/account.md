###用户账户管理

###/account/register POST #注册

传入：
{
    "name":"",
    "password":"".
    "isAdmin":"".
    "area":""
}

传出：
10000003   #权限不足
{}    #正常返回

###/account/login POST

传入：
{
    "name":"",
    "password":""
}

传出：
{
    "is_admin":"",
    "area":""
}

###/account/logout GET,POST
传入：无
传出：{}