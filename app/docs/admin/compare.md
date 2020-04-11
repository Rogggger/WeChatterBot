### 对比分析
### admin/compare/ GET
得到调查期
传出
```
{
	[
		{
			"start":""
			"end":""
			"id":""
		}
		,
		{
			
		}
	]
}
```
###admin/compare/ POST
传入 两个调查期的id
```
{
	"id_1":"",
	"id_2":""
}
```
传出
```
{
	"sum":""       #企业总数
	"filing":""     #建档期总岗位数、
	"check":""       # 岗位变化总数
	"percnet":""      #岗位变化占比
}

```


