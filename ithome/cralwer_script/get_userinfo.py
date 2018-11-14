#coding:utf-8
__author__ = 'kael'

import sys
import io
import urllib
from urllib import request
import ssl
from bs4 import BeautifulSoup
import re
import traceback
import time
import getopt
import datetime
import pymysql

sys.path.append('/home/kael/myobject/common')
from py_common import *

function_name = "get_user_info"
comm = Py_common(function_name)

class GetUserInfo(object):
    def __init__(self,s_userid,e_userid):
        self.s_userid = s_userid
        self.e_userid = e_userid
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
        self.user_info_table = "userinfo" + time.strftime('%Y_%m',time.localtime(time.time()))

    def __create_table__(self):
        user_info_table_sql = "create table if not exists %s(\
                                userid    varchar(100),\
                                nick_name varchar(100),\
                                user_level varchar(100),\
                                user_app varchar(100),\
                                re_time varchar(100),\
                                comment_cnt varchar(100),\
                                post_cnt varchar(100),\
                                insert_time datetime\
                                )" %self.user_info_table
        try:
            conn = comm.conn_kael()
            cursor = conn.cursor()
            cursor.execute(user_info_table_sql)
            conn.commit()
            conn.close()
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())


    def get_user_info(self):
        user_id = self.s_userid
        while int(user_id) <= int(self.e_userid):
            user_info = [user_id]
            ssl._create_default_https_context = ssl._create_unverified_context
            url = "https://m.ithome.com/user/%s" %user_id
            req = request.Request(url=url,headers=self.headers)
            resq = request.urlopen(req)
            soup = BeautifulSoup(resq,"html.parser")

            try:
                info1 = soup.find_all("div",{"class":"user-uib"})
                nick_name = info1[0].find("span",{"class":"un"}).get_text()
                user_info.append(nick_name)
                lv = info1[0].find("span",{"class":"lv"}).get_text()   
                user_info.append(lv)
                # print(nick_name)
                # print(lv)
                active = ""
                for i in info1[0].find_all("i"):
                    if re.search('active',str(i)):
                        active = active + '\t' + i.get('class')[0]
                user_info.append(active.lstrip())
                # print(active.lstrip())
                re_time = info1[0].find("span",{"class":"uzt"}).get_text()
                user_info.append(re_time.replace("注册时间：",""))
                # print(re_time.replace("注册时间：",""))

            except Exception as e:
                comm.print_log("error","%s" %traceback.format_exc())
    
            try:
                info2 = soup.find_all("div",{"class":"user-column"})
                t = info2[0].find_all("span")
                for i in t:
                    user_info.append(re.findall(r'[（](.*?)[）]',i.get_text())[0])
                    # print(re.findall(r'[（](.*?)[）]',i.get_text())[0])            
            except Exception as e:
                comm.print_log("error","%s" %traceback.format_exc())
            
            sSql="insert into %s (userid,nick_name,user_level,user_app,re_time,comment_cnt,\
                post_cnt,insert_time)" %self.user_info_table + "values(\
                %s,%s,%s,%s,%s,%s,%s,now())"

            try:
                conn = comm.conn_kael()
                cursor = conn.cursor()
                cursor.execute(sSql,user_info)
                conn.commit()
                conn.close()
            except Exception as e:
                comm.print_log("error","%s" %traceback.format_exc())

            user_id = str(int(user_id) + 1)
    
    def run(self):
        try:
            self.__create_table__()
            self.get_user_info()

        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())


if __name__ == '__main__':
    comm.print_log("info","start get useinfo")
    s_userid = ""
    e_userid = ""
    opts,args = getopt.getopt(sys.argv[1:],"s:e:")
    for op,val in opts:
        if op == "-s":
            s_userid = val
        if op == "-e":
            e_userid = val
    print(s_userid)
    print(e_userid)
    cal = GetUserInfo(s_userid,e_userid)
    cal.run()
    comm.print_log("info","get userinfo")