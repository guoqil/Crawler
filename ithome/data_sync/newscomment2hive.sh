#!/bin/bash
month=$1
table_name=newscomment${month/-/_}
echo ${table_name}

output_json_path="/home/kael/datax_jobs/newscomment2hive.json"
mysql_username="public"
mysql_password="public123"
jdbcUrl="jdbc:mysql://localhost:3306/kael?yearIsDateType=false&zeroDateTimeBehavior=CONVERT_TO_NULL&rewriteBatchedStatements=true"
querySql="select newsid,l,comment_id,REPLACE(REPLACE(comment,CHAR(10),''),CHAR(13),'') comment,nick_name,userid,user_location,comment_time,support,disagree,device_name,r,clientid,ir,sf,user_level,tl,rl,reply_userid,m,headimg,writetime,clientname,userindexurl,insert_time from ${table_name}"

write_column_num=25
preSql="truncate table tmp_newscomment"
hdfs_path="/user/hive/warehouse/kael.db/tmp_newscomment"
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

hive -e "truncate table kael.tmp_newscomment;"

python2.7 /opt/datax/bin/datax.py ${output_json_path}

sql="
INSERT OVERWRITE TABLE kael.newscomment partition
    (month = '${month}')
select newsid,l,comment_id,comment,nick_name,userid,user_location,
        comment_time,support,disagree,device_name,r,clientid,ir,sf,
        user_level,tl,rl,reply_userid,m,headimg,writetime,clientname,
        userindexurl,insert_time from
(select newsid,l,comment_id,comment,nick_name,userid,user_location,
        comment_time,support,disagree,device_name,r,clientid,ir,sf,
        user_level,tl,rl,reply_userid,m,headimg,writetime,clientname,
        userindexurl,insert_time,
        row_number() over(partition by comment_id order by insert_time desc) ranks
 from kael.tmp_newscomment) a where a.ranks = 1;
"
hive -e "${sql}"

echo "done!"