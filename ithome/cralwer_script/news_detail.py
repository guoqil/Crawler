#coding:utf-8
__author__ = 'kael'

import sys
import io
import urllib
from urllib import request
import ssl
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import traceback
import time
import getopt
import datetime
import pymysql

sys.path.append('/home/kael/myobject/common')
from py_common import *

function_name = "get_news_detail"
comm = Py_common(function_name)

class GetNewsDetail(object):
    def __init__(self,post_date):
        self.newsid = ""
        self.post_date = post_date
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
        self.news_detail_table = "newsdetail" + self.post_date[0:7].replace('-','_')

        self.process_num = 10

    def __create_table__(self):
        news_detail_table_sql = "create table if not exists %s(\
                                    newsid    varchar(10),\
                                    title   text,\
                                    keywords   text,\
                                    description text,\
                                    types varchar(100),\
                                    news_author varchar(100),\
                                    detail MEDIUMTEXT,\
                                    duty_man varchar(100),\
                                    insert_time datetime\
                                )" %self.news_detail_table
        try:
            conn = comm.conn_kael()
            cursor = conn.cursor()
            cursor.execute(news_detail_table_sql)
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
            pool.apply_async(self.get_news_detail,(newsid,))
            # self.get_news_detail(newsid)
        pool.close()
        pool.join()
        print("done!")

    def get_news_detail(self,newsid):
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://m.ithome.com/html/%s.htm" %newsid
        req = request.Request(url=url,headers=self.headers)
        resq = request.urlopen(req)
        soup = BeautifulSoup(resq,"html.parser")
        news_detail = [newsid]
        try:
            title = soup.find("title").get_text()
            news_detail.append(title)
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            news_detail.append("title_error")
        
        try:
            keywords = soup.find_all("meta",{"name":"keywords"})
            news_detail.append(keywords[0].get('content'))
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            news_detail.append("keywords_error")
        
        try:
            description = soup.find_all("meta",{"name":"description"})
            news_detail.append(description[0].get('content'))
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            news_detail.append("description_error")
        
        try:
            t = soup.find_all("a",href=re.compile('https://m.ithome.com'))
            types = ""
            for i in range(1,4):
                types = types + t[i].get_text() + "|"
            news_detail.append(types)
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            news_detail.append("types_error")

        try:
            news_author = soup.find_all("span",{"class":"news-author"})
            news_detail.append(news_author[0].get_text())
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            news_detail.append("news_author_error")

        try:
            detail = ""
            d = soup.find_all("div",{"class":"news-content"})
            de = d[0].find_all("p")
            for i in de:
                det = i.find_all("img")
                if len(det) == 0:
                    detail = detail + i.get_text()
                    # print(i.get_text())
                else:
                    for img in det:
                        detail = detail + "|" + img.get('data-original')
                        # print(img.get('data-original'))
            news_detail.append(detail)
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            news_detail.append("detail_error")
        
        try:
            duty_man = soup.find_all("span",{"class":"duty-man"})
            news_detail.append(duty_man[0].get_text())
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            news_detail.append("duty_manl_error")
        
        sSql="insert into %s (newsid,title,keywords,description,types,news_author,\
                detail,duty_man,insert_time)" %self.news_detail_table + "values(\
                %s,%s,%s,%s,%s,%s,%s,%s,now())"

        try:
            conn = comm.conn_kael()
            cursor = conn.cursor()
            cursor.execute(sSql,news_detail)
            conn.commit()
            conn.close()
        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())
            


    
    def run(self):
        try:
            self.__create_table__()
            self.get_news_id()

        except Exception as e:
            comm.print_log("error","%s" %traceback.format_exc())


if __name__ == '__main__':
    comm.print_log("info","start get newsdetail")
    post_date = ""
    opts,args = getopt.getopt(sys.argv[1:],"p:")
    for op,val in opts:
        if op == "-p":
            post_date = val
    print(post_date)
    cal = GetNewsDetail(post_date)
    cal.run()
    comm.print_log("info","get newsdetail")