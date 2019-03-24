#!/bin/bash
# author "kael"

if [ $# -eq 0 ]; then
    cal_date="$(date -d '-1 days' +"%Y-%m-%d")"
else
    cal_date=$1
fi

echo ${cal_date}
comm_date=`date -d"${cal_date} -14 days" +"%Y-%m-%d"`

echo ${comm_date}

bash /home/kael/myobject/ithome/cralwer_script/list_crawler.sh ${cal_date} > /home/kael/myobject/logs/list_crawler_${cal_date}.log

bash /home/kael/myobject/ithome/cralwer_script/news_detail_crawler.sh ${cal_date} > /home/kael/myobject/logs/news_detail_${cal_date}.log

bash /home/kael/myobject/ithome/cralwer_script/news_comment_crawler.sh ${comm_date} > /home/kael/myobject/logs/news_comment_${comm_date}.log

day=${cal_date:8:2}
echo ${day}
sync_month=`date -d"${cal_date} -1 months" +"%Y-%m"`
if [ "${day}" -eq "02" ]; then
    echo "同步详情页爬虫"
    bash /home/kael/myobject/ithome/data_sync/newsdetail2hive.sh ${sync_month} > /home/kael/myobject/logs/newsdetail2hive_${sync_month}.log
elif [ "${day}" -eq "16" ]; then
    echo "同步评论页爬虫"
    bash /home/kael/myobject/ithome/data_sync/newscomment2hive.sh ${sync_month} > /home/kael/myobject/logs/newscomment2hive_${sync_month}.log
else
    echo "时间未到，无需同步数据"
fi

echo "done!"