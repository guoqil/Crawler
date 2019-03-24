#!/bin/bash
month=$1
table_name=newsdetail${month/-/_}
echo ${table_name}

output_json_path="/home/kael/datax_jobs/newsdetail2hive.json"
mysql_username="public"
mysql_password="public123"
jdbcUrl="jdbc:mysql://localhost:3306/kael?yearIsDateType=false&zeroDateTimeBehavior=CONVERT_TO_NULL&rewriteBatchedStatements=true"
querySql="select newsid,REPLACE(REPLACE(title,CHAR(10),''),CHAR(13),''),REPLACE(REPLACE(keywords,CHAR(10),''),CHAR(13),''),REPLACE(REPLACE(description,CHAR(10),''),CHAR(13),''),types,news_author,REPLACE(REPLACE(detail,CHAR(10),''),CHAR(13),''),duty_man,insert_time from ${table_name}"

write_column_num=9
preSql="truncate table tmp_newsdetail"
hdfs_path="/user/hive/warehouse/kael.db/tmp_newsdetail"
fileName="${table_name}"

python2.7 mysql2hive.py \
    --output_json_path ${output_json_path} \
    --mysql_username ${mysql_username} \
    --mysql_password ${mysql_password} \
    --jdbcUrl ${jdbcUrl} \
    --querySql "${querySql}" \
    --write_column_num "${write_column_num}" \
    --preSql "${preSql}" \
    --hdfs_path ${hdfs_path} \
    --fileName ${fileName}

hive -e "truncate table kael.tmp_newsdetail;"

python2.7 /opt/datax/bin/datax.py ${output_json_path}

sql="
INSERT OVERWRITE TABLE kael.newsdetail partition
    (month = '${month}')
select newsid,title,keywords,description,types,news_author,detail,
        duty_man,insert_time from
(select newsid,title,keywords,description,types,news_author,detail,
        duty_man,insert_time,
        row_number() over(partition by newsid order by insert_time desc) ranks
 from kael.tmp_newsdetail) a where a.ranks = 1;
"
hive -e "${sql}"

echo "done!"
