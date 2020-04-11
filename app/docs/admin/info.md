### 企业备案信息搜索：

### /admin/info/ POST
传入

- area: str 企业所属地区

示例：
~~~
{
	"area": "0531",
}
~~~

传出：
~~~
[
    {
        "main_business": "123",
        "fax": "123456654321",
        "code": "123456",
        "name": "1234",
        "contacts": "wyw",
        "area": [
            "0531",
            "1"
        ],
        "phone": "123456654321",
        "enterprise_kind": "123",
        "belong_to": [
            "123432"
        ],
        "postal_code": "123456",
        "address_detail": "1234432",
        "email": "123@123.com",
        "enterprise_scale": "43"
    }
]
~~~

