###企业数据填报

### /data/record POST

传入：

传出：
10000016  #信息不能修改
10000014  #不在可以填报的时间内
{}  #成功

### /data/get GET

传入：

传出：
{
    "filing":Integer,  # 初次建档时就业人数
    "check":Integer,  # 本次调查期就业人数
    "other_reason":""  # 其他原因
    "decrease_type":""  # 就业人数减少类型
    "main_reason":""  # 主要原因
    "main_reason_detail":""  # 主要原因说明
    "second_reason":""   # 次要原因
    "second_reason_detail":""  # 次要原因说明
    "third_reason":""  # 第三原因
    "third_reason_detail":""  # 第三原因
    "status":Integer #状态
}    #成功
{}#失败

### /data/report POST

传入：
{
    "filing":"",  # 初次建档时就业人数
    "check":"",  # 本次调查期就业人数
    "other_reason":""  # 其他原因
    "decrease_type":""  # 就业人数减少类型
    "main_reason":""  # 主要原因
    "main_reason_detail":""  # 主要原因说明
    "second_reason":""   # 次要原因
    "second_reason_detail":""  # 次要原因说明
    "third_reason":""  # 第三原因
    "third_reason_detail":""  # 第三原因
}

传出：
10000014 #不在可以填报的时间段内
10000015 #没有保存
10000016 #不能修改
{} #成功

### /data/record GET
传入：

传出：
{
    "filing":Integer,  # 初次建档时就业人数
    "check":Integer,  # 本次调查期就业人数
    "other_reason":""  # 其他原因
    "decrease_type":""  # 就业人数减少类型
    "main_reason":""  # 主要原因
    "main_reason_detail":""  # 主要原因说明
    "second_reason":""   # 次要原因
    "second_reason_detail":""  # 次要原因说明
    "third_reason":""  # 第三原因
    "third_reason_detail":""  # 第三原因
    "status":Integer #状态
}