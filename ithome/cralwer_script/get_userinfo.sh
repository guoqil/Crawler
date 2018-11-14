#!/bin/bash
# 用户信息爬虫入口
# author "kael"

# if [ $# -eq 0 ]; then
#     cal_date="$(date -d '-1 days' +"%Y-%m-%d")"
# elif [ $# -eq 1 ]; then
#     cal_date=$1
# else 
#     echo "输入正确参数，例如:2018-10-23"
# fi
s_userid=$1
e_userid=$2

# post_date=${cal_date}

# echo $#
# echo ${cal_date}
echo ${s_userid}
echo ${e_userid}

python3 get_userinfo.py \
    -s ${s_userid} \
    -e ${e_userid}