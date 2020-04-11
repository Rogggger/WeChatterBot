### 数据审核
### admin/datacheck/  GET
传入 ：无
传出
```
{
	[
		{
			"filing" : 99, 
			"check" : 20,
			"other_reason" : "redf",
			"decrease_type":"asdf",
			"main_reason" :"sfdsdf",
			"main_reason_detail" :"gdsdf",
			"second_reason" :"dinsa",
			"second_reason_detail":"dinnsld",
			"third_reason" : "kkkkkkkkkkkk",
			"third_reason_detail" : "idnsldj"
			"id":""
			"name":""
		}
		,
		{
		
		}
	
	]
}


```

### admin/datacheck/   POST
传入
```angular2html
{
	"id":""
	"status":""  # 0 是不通过 1 通过
	"remark":""  # 备注
}

```

