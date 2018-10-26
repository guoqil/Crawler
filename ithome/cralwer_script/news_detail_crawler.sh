#!/bin/bash
# 文章详情页爬虫入口
# author "kael"

if [ $# -eq 0 ]; then
    cal_date="$(date -d '-1 days' +"%Y-%m-%d")"
elif [ $# -eq 1 ]; then
    cal_date=$1
else 
    echo "输入正确参数，例如:2018-10-23"
fi

post_date=${cal_date}

# echo $#
# echo ${cal_date}
echo ${post_date}

python3 news_detail.py \
    -p ${post_date}