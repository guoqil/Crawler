#coding:utf-8
import json
import argparse
import ast

# JSON模板
template_json = {\
    "job": {\
        "setting": {\
            "speed": {\
                 "channel": 3\
            },\
            "errorLimit": {\
                "record": 0,\
                "percentage": 0.02\
            }\
        },\
        "content": [\
            {\
                "reader": {\
                    "name": "mysqlreader",\
                    "parameter": {\
                        "username": "",\
                        "password": "",\
                        "connection": [\
                            {\
                                "querySql": [\
                                    ""\
                                ],\
                                "jdbcUrl": [\
                                    ""\
                                ]\
                            }\
                        ],\
                        "sliceRecordCount": 10\
                    }\
                },\
                "writer": {\
                    "name": "hdfswriter",\
                    "parameter": {\
                        "encoding": "UTF-8",\
                        "defaultFS": "hdfs://kael-Precision-T3610:9000",\
                        "fileType": "TEXT",\
                        "path": "/user/hive/warehouse/kael.db/tmp_newscomment",\
                        "fileName": "newscomment2017_05",\
                        "preSql": [""],\
                        "column": [],\
                        "hadoopProxyUser":"kael",\
                        "writeMode": "nonConflict",\
                        "fieldDelimiter": "\001",\
                        "compress":"gzip"\
                    }\
                }\
            }\
        ]\
    }\
}

# 接收参数传入
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--output_json_path', type=str, default='/home/kael/datax_jobs/mysql2hive.json',help='生成的DataX JSON配置文件存放路径')

parser.add_argument('--mysql_username', type=str, default=None,help='mysql库账户')
parser.add_argument('--mysql_password', type=str, default=None,help='mysql库密码')
parser.add_argument('--jdbcUrl', type=str, default='jdbc:mysql://localhost:3306/kael?yearIsDateType=false&zeroDateTimeBehavior=CONVERT_TO_NULL&rewriteBatchedStatements=true',help='')
parser.add_argument('--querySql', type=str, default=None, help='若有多个用","隔开')

parser.add_argument('--write_column_num', type=str, default=None,help='导入的列的个数')
parser.add_argument('--preSql', type=str, default=None,help='')
parser.add_argument('--hdfs_path', type=str, default=None, help=None)
parser.add_argument('--fileName', type=str, default=None, help=None)



# 省略若干参数
## ...

args = parser.parse_args()

# 填入参数
template_json['job']['content'][0]['reader']['parameter']['username'] = args.mysql_username
template_json['job']['content'][0]['reader']['parameter']['password'] = args.mysql_password
template_json['job']['content'][0]['reader']['parameter']['connection'][0]['jdbcUrl'][0] = args.jdbcUrl
template_json['job']['content'][0]['reader']['parameter']['connection'][0]['querySql'][0] = args.querySql

columns = []
columnsStr = args.write_column_num
# print(columnsStr)
column = {"name":"","type":"string"}
for i in range(int(columnsStr)):
    column['name'] = "c" + str(i)
    columns.append(column)

template_json['job']['content'][0]['writer']['parameter']['column'] = columns
template_json['job']['content'][0]['writer']['parameter']['preSql'][0] = args.preSql
template_json['job']['content'][0]['writer']['parameter']['path'] = args.hdfs_path
template_json['job']['content'][0]['writer']['parameter']['fileName'] = args.fileName

# 输出JSON配置文件
with open(args.output_json_path,'w') as f:
    f.write(json.dumps(template_json))
