# zzpy
Python3 Utilities
```shell
# pip3 install zzpy -i https://pypi.org/simple
# pip3 install zzpy --upgrade -i https://pypi.org/simple
```


# 待验证
- [ ] zgeo


# 未完成
- [ ] zexcel
- [ ] zcaptcha
- [ ] zbrowser
- [ ] zjson
- [ ] zrun
- [ ] ztime


# 已完成
- [x] zrandom
- [x] zconfig
- [x] zfile
- [x] zmongo
- [x] zmysql
- [x] zredis
- [x] zsys


# release log
* 1.1.9: excel
* 1.1.6: +zfunction.list_or_args; +zredis.publish/listen; zredis.brpop/blpop+safe
* 1.0.20200827: +ES处理zes
* 1.0.20200825: +zfile.download_file
* 1.0.20200824: +zmongo.mongo_collection
* 1.0.20200821.4: 删除ztime无用方法
* 1.0.20200821.3: ztime
* 1.0.20200821:zalioss+url
* 1.0.20200820.10:zalioss+list+delete
* 1.0.20200820.8: 私有库推送
* 1.0.20200817: 重构OssFile，支持oss_url格式，去掉OssFile，新增AliOss
* 1.0.20200812.6: excel->csv
* 1.0.20200812.5: zalioss修复默认配置的bug
* 1.0.20200812.4: +zalioss
* 1.0.20200812.3: zjson.jsondumps cls参数默认值为DateEncoder
* 1.0.20200812.2: zmysql.mysql_iter_table fix default parameters
* 1.0.20200812.1: zmysql.mysql_iter_table+fields
* 1.0.20200812: zmysql+mysql_iter_table
* 1.0.20200723: zmysql.MySQLConfig对MYSQL_URL解析规则问题修复
* 1.0.20200721: ztime+get_month
* 1.0.9: build.sh
* 1.0.8: +get_today, +get_date
* 1.0.7: jsondumps+params
* 1.0.6: +jsondumps
