# python_12306

### 各个文件介绍

`login.py`: 12306登陆，目前验证码部分的处理是将验证码图片下载到本地，然后通过0-7的序号提交（可以考虑自动识图，如百度识图等）

`query.py`: 12306车次详情查询，这个目前编写较为完善，其中也使用了`prettytable``colorama`等库美化输出格式

`stationName.py`: 12306城市代码生成，通过这个文件可以直接生成各个城市的名称以相应代码，使用方式：python3 stationName.py >> stations.py

`stations.py`: 城市名以及代码文件，通过`stationName.py`生成

`utils.py`: 其他工具类