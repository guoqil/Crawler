#coding:utf-8
__author__ = 'kael'

import os
import sys
import pwd
from urllib import request
from bs4 import BeautifulSoup
import json
import time
import getopt
import datetime
import pymysql
import traceback

sys.path.append('/home/kael/myobject/common')
from py_common import *
function_name = "get_list"
comm = Py_common(function_name)

class GetList(object):
    def __init__(self,start_time,end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.processes_num = 10
        self.top_list_table = "toplist" + self.start_time[0:7].replace('-','_')
        self.news_list_table = "newslist" + self.start_time[0:7].replace('-','_')


    def __create_table__(self):
        top_list_table_sql = "create table if not exists %s(\
                        live    varchar(10),\
                        client  varchar(100),\
                        device  varchar(100),\
                        topplat varchar(100),\
                        newsid  varchar(100),\
                        title   text,\
                        postdate    varchar(100),\
                        orderdate   varchar(100),\
                        description text,\
                        image   varchar(500),\
                        hitcount    varchar(100),\
                        commentcount    varchar(100),\
                        cid varchar(100),\
                        sid varchar(100),\
                        url varchar(200),\
                        insert_time datetime\
                    )" %self.top_list_table
        news_list_table_sql = "create table if not exists %s(\
                        newsid    text(10),\
                        title   text,\
                        v   text,\
                        orderdate varchar(100),\
                        postdate    varchar(100),\
                        description text,\
                        image   varchar(500),\
                        slink   varchar(500),\
                        hitcount    varchar(100),\
                        commentcount    varchar(100),\
                        cid varchar(100),\
                        url varchar(200),\
                        live varchar(100),\
                        lapinid varchar(100),\
                        forbidcomment   varchar(100),\
                        imagelist text,\
                        c   varchar(500),\
                        client  varchar(100),\
                        isad    varchar(10),\
                        sid varchar(100),\
                        PostDateStr varchar(100),\
                        HitCountStr varchar(200),\
                        WapNewsUrl  varchar(200),\
                        TipClass    varchar(100),\
                        TipName varchar(100),\
                        insert_time datetime\
                    )" %self.news_list_table
        try:
            conn = comm.conn_kael()
            cursor = conn.cursor()
            cursor.execute(top_list_table_sql)
            cursor.execute(news_list_table_sql)
            conn.commit()
            conn.close()
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc()) 

    def get_top_first(self):
        url = "http://api.ithome.com/json/newslist/news"
        top_list = []
        req = request.Request(url=url,headers=self.headers)
        resq = request.urlopen(req)
        string = BeautifulSoup(resq,"html.parser").text
        web_data = json.loads(string)
        if "toplist" in web_data.keys() and len(web_data["toplist"]) != 0:
            toplist = web_data["toplist"][0]
            if "live" in toplist.keys():
                top_list.append(toplist["live"])
                # print(toplist["live"])
            else:
                top_list.append("none")
            top_list.append(toplist["client"])
            top_list.append(toplist["device"])
            top_list.append(toplist["topplat"])
            top_list.append(toplist["newsid"])
            top_list.append(toplist["title"])
            top_list.append(toplist["postdate"])
            top_list.append(toplist["orderdate"])
            top_list.append(toplist["description"])
            top_list.append(toplist["image"])
            top_list.append(toplist["hitcount"])
            top_list.append(toplist["commentcount"])
            top_list.append(toplist["cid"])
            top_list.append(toplist["sid"])
            top_list.append(toplist["url"])

            try:
                conn = comm.conn_kael()
                cursor = conn.cursor()
                sSql = "insert into %s" %self.top_list_table + "(live,client,device,topplat,newsid,title,postdate,orderdate,description,\
                        image,hitcount,commentcount,cid,sid,url,insert_time) values (\
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                        %s,%s,%s,now())" 
                cursor.execute(sSql,top_list)
                conn.commit()
                conn.close()
            except Exception as e:
                comm.print_log("error","%s" %traceback.format_exc())
        else:
            comm.print_log("info","No top_news!")

    def get_slide_list(self):
        url = "http://api.ithome.com/json/slide/index"
        req = request.Request(url=url,headers=self.headers)
        resq = request.urlopen(req)
        string = BeautifulSoup(resq,"html.parser").text
        web_data = json.loads(string)

        print(web_data)
   
    def get_list(self):
        # t = int(time.time())*1000
        st = time.strptime(self.start_time,"%Y-%m-%dT%H:%M:%S")
        int_st = int(time.mktime(st))*1000
        et = time.strptime(self.end_time,"%Y-%m-%dT%H:%M:%S")
        int_et = int(time.mktime(et))*1000

        last_time = int_st
        ot = 0
        while last_time > int_et:
            ot = last_time
            url = "https://m.ithome.com/api/news/newslistpageget?Tag=&ot={}&page=0".format(str(ot))
            req = request.Request(url=url,headers=self.headers)
            resq = request.urlopen(req)
            string = BeautifulSoup(resq,"html.parser").text
            web_data = json.loads(string)
            if "Result" in web_data.keys():
                news_list = web_data["Result"]
                if len(news_list) != 0:
                    t = news_list[len(news_list)-1]["orderdate"][0:19]
                    lt = time.strptime(t,"%Y-%m-%dT%H:%M:%S")
                    last_time = int(time.mktime(lt))*1000 - 1000

                    for i in range(len(news_list)):
                        if news_list[i]["orderdate"][0:19] > self.end_time:
                            news_info = []
                            news_info.append(news_list[i]["newsid"])
                            news_info.append(news_list[i]["title"])
                            if news_list[i]["v"] == None:
                                news_info.append("null")
                            else:
                                news_info.append(news_list[i]["v"])
                            news_info.append(news_list[i]["orderdate"])
                            news_info.append(news_list[i]["postdate"])
                            news_info.append(news_list[i]["description"])
                            news_info.append(news_list[i]["image"])
                            if news_list[i]["slink"] == None:
                                news_info.append("null")
                            else:
                                news_info.append(news_list[i]["slink"])
                            news_info.append(news_list[i]["hitcount"])
                            news_info.append(news_list[i]["commentcount"])
                            news_info.append(news_list[i]["cid"])
                            news_info.append(news_list[i]["url"])
                            news_info.append(news_list[i]["live"])
                            if news_list[i]["lapinid"] == None:
                                news_info.append("null")
                            else:
                                news_info.append(news_list[i]["lapinid"])
                            if news_list[i]["forbidcomment"] == None:
                                news_info.append("null")
                            else:
                                news_info.append(news_list[i]["forbidcomment"])
                            if news_list[i]["imagelist"] == None:
                                news_info.append("null")
                            else:
                                imagelist = ""
                                for image in news_list[i]["imagelist"]:
                                    imagelist = imagelist + image + "|"
                                news_info.append(imagelist)

                            if news_list[i]["c"] == None:
                                news_info.append("null")
                            else:
                                news_info.append(news_list[i]["c"])
                            if news_list[i]["client"] == None:
                                news_info.append("null")
                            else:
                                news_info.append(news_list[i]["client"])
                            news_info.append(news_list[i]["isad"])
                            news_info.append(news_list[i]["sid"])
                            news_info.append(news_list[i]["PostDateStr"])
                            if news_list[i]["HitCountStr"] == None:
                                news_info.append("null")
                            else:
                                news_info.append(news_list[i]["HitCountStr"])
                            news_info.append(news_list[i]["WapNewsUrl"])
                            if len(news_list[i]["NewsTips"]) == 0:
                                news_info.append("null")
                                news_info.append("null")
                            else:
                                NewsTips = news_list[i]["NewsTips"][0]
                                news_info.append(NewsTips["TipClass"])
                                news_info.append(NewsTips["TipName"])

                            # print(news_info)
                            
                            try:
                                conn = comm.conn_kael()
                                cursor = conn.cursor()
                                sSql = "insert into %s (newsid,title,v,orderdate,postdate,description,image,slink,hitcount,\
                                        commentcount,cid,url,live,lapinid,forbidcomment,imagelist,c,client,\
                                        isad,sid,PostDateStr,HitCountStr,WapNewsUrl,TipClass,TipName,insert_time)" %self.news_list_table + "values(\
                                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                                        %s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
                                cursor.execute(sSql,news_info)
                                conn.commit()
                                conn.close()
                            except Exception as e:
                                comm.print_log("error","[%s][%s]" %(traceback.format_exc(),news_info))
                        else:
                            break
                    
    
    def run(self):
        try:
            self.__create_table__()
            self.get_top_first()
            self.get_list()
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())

if __name__ == '__main__':
    comm.print_log("info","start get list")
    start_time = ""
    end_time = ""
    opts,args = getopt.getopt(sys.argv[1:],"s:e:")
    for op,val in opts:
        if op == "-s":
            start_time = val 
        if op == "-e":
            end_time = val
    print(start_time)
    print(end_time)
    cal = GetList(start_time,end_time)
    cal.run()
    comm.print_log("info","end get list")