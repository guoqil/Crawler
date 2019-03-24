#!/bin/bash
# author "kael"

for((i=1;i<=12;i++));
do
    month="2017-$i"
    if [ $i -lt 10 ]; then
        month="2017-0$i"
    fi
    echo "${month}"
    bash newscomment2hive.sh ${month}
done

for((i=1;i<=9;i++));
do
    month="2018-$i"
    if [ $i -lt 10 ]; then
        month="2018-0$i"
    fi
    echo "${month}"
    bash newscomment2hive.sh ${month}
done
