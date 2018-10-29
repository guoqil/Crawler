#coding:utf-8
__author__ = 'kael'

import sys
import os
import traceback
import time
import getopt
import datetime
import pymysql
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import json

sys.path.append('/home/kael/myobject/common')
from py_common import *
function_name = "get_news_comment"
comm = Py_common(function_name)

class GetNewsComment(object):
    def __init__(self,post_date):
        self.post_date = post_date
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
        self.news_comment_table = "newscomment" + self.post_date[0:7].replace('-','_')
        self.process_num = 10

    def __create_table__(self):
        news_comment_table_sql = "create table if not exists %s(\
                                    newsid    varchar(10),\
                                    l   varchar(100),\
                                    comment_id  varchar(100),\
                                    comment mediumtext,\
                                    nick_name   varchar(100),\
                                    userid  varchar(100),\
                                    user_location   varchar(100),\
                                    comment_time    varchar(100),\
                                    support varchar(100),\
                                    disagree  varchar(100),\
                                    device_name  varchar(100),\
                                    r   varchar(100),\
                                    clientid    varchar(100),\
                                    ir  varchar(100),\
                                    sf  varchar(100),\
                                    user_level  varchar(100),\
                                    tl  varchar(100),\
                                    rl  varchar(100),\
                                    reply_userid    varchar(100),\
                                    m   varchar(100),\
                                    headimg varchar(200),\
                                    writetime   varchar(100),\
                                    clientname  varchar(100),\
                                    userindexurl    varchar(200),\
                                    insert_time datetime\
                                    ) DEFAULT CHARSET=utf8mb4" %self.news_comment_table
        try:
            conn = comm.conn_kael()
            cursor = conn.cursor()
            cursor.execute(news_comment_table_sql)
            conn.commit()
            conn.close()
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())                           

    def get_news_id(self):
        newslist_table = "newslist" + self.post_date[0:7].replace('-','_')
        sSql = "select distinct newsid from %s \
        where substr(postdate,1,10) = '%s'" %(newslist_table,self.post_date)

        try:
            conn = comm.conn_kael()
            cursor = conn.cursor()
            cursor.execute(sSql)
            newsid_list = cursor.fetchall()
            conn.close()
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())

        pool = Pool(processes=self.process_num)
        for newsid in (newsid_list):
            print(newsid)
            pool.apply_async(self.get_news_comment,(newsid,))
        pool.close()
        pool.join()
        print("done!")
    
    def get_news_comment(self,newsid):
        url = "https://m.ithome.com/api/comment/newscommentlistget?NewsID=%s" %newsid
        success = 1
        while success == 1:
            req = requests.get(url=url,headers=self.headers)
            soup = BeautifulSoup(req.text,"html.parser").text
            web_data = json.loads(soup)

            success = success * web_data["Success"]
            if success == 0:
                break
            else:
                clist = web_data["Result"]["Clist"]
                last_f = clist[len(clist)-1]
                last_cid = last_f["M"]["Ci"]
                url = "https://m.ithome.com/api/comment/newscommentlistget?NewsID=%s&LapinID=&MaxCommentID=%s&Latest=" %(newsid,last_cid)

                for comments in clist:
                    comment = comments["M"]
                    cl = [newsid]
                    for i in comment.keys():
                        cl.append(comment[i])                
                    try:
                        conn = comm.conn_kael()
                        cursor = conn.cursor()
                        sSql = "insert into %s (newsid,l,comment_id,comment,nick_name,userid,user_location,\
                                    comment_time,support,disagree,device_name,r,clientid,ir,sf,\
                                    user_level,tl,rl,reply_userid,m,headimg,writetime,clientname,\
                                    userindexurl,insert_time)" %self.news_comment_table + "values(\
                                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                                    %s,%s,%s,%s,%s,%s,%s,%s,now())"
                        cursor.execute(sSql,cl)
                        conn.commit()
                        conn.close()
                    except Exception as e:
                        comm.print_log("error","[%s][%s]" %(traceback.format_exc(),news_info))

                    if len(comments["R"]) > 0:
                        for commentr in comments["R"]:
                            cr = [newsid]
                            for j in commentr.keys():
                                cr.append(commentr[j])
                            try:
                                conn = comm.conn_kael()
                                cursor = conn.cursor()
                                sSql = "insert into %s (newsid,l,comment_id,comment,nick_name,userid,user_location,\
                                    comment_time,support,disagree,device_name,r,clientid,ir,sf,\
                                    user_level,tl,rl,reply_userid,m,headimg,writetime,clientname,\
                                    userindexurl,insert_time)" %self.news_comment_table + "values(\
                                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                                    %s,%s,%s,%s,%s,%s,%s,%s,now())"
                                cursor.execute(sSql,cr)
                                conn.commit()
                                conn.close()
                            except Exception as e:
                                comm.print_log("error","[%s][%s]" %(traceback.format_exc(),news_info))




    def run(self):
        try:
            self.__create_table__()
            self.get_news_id()
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())

if __name__ == '__main__':
    comm.print_log("info","start get newscomment")
    post_date = ""
    opts,args = getopt.getopt(sys.argv[1:],"p:")
    for op,val in opts:
        if op == "-p":
            post_date = val
    print(post_date)
    cal = GetNewsComment(post_date)
    cal.run()
    comm.print_log("info","get newscomment")