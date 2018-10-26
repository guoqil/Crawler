#!/bin/bash
# 列表页爬虫入口
# author "kael"

if [ $# -eq 0 ]; then
    cal_date="$(date -d '-1 days' +"%Y-%m-%d")"
elif [ $# -eq 1 ]; then
    cal_date=$1
else 
    echo "输入正确参数，例如:2018-10-23"
fi

start_time=${cal_date}"T23:59:59"
end_time=${cal_date}"T00:00:00"

# echo $#
# echo ${cal_date}
echo ${start_time}
echo ${end_time}

python3 list.py \
    -s ${start_time} \
    -e ${end_time}
