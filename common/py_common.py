#coding:utf-8
# 公共函数
import os
import pwd
import pymysql
import datetime
import time
from time import sleep
import traceback


class Py_common(object):
    def __init__(self,function_name):
        self.function_name = function_name
        self.script_base_fold = "/home/kael"
        
        conf_path = "%s/myobject/conf/common.conf" %(self.script_base_fold)
        self.gConf = self.load_conf(conf_path)

        secret_path = "%s/myobject/conf/.secret.common.conf" %(self.script_base_fold)
        self.load_secret(secret_path,self.gConf)

    def load_conf(self,conf_file_path):
        conf = {}
        f = open(conf_file_path)
        line = f.readline()
        while line:
            line = line.strip()
            if line.find("#") != 0 and line.find("=") > 0:
                item = line.split("=")
                if len(item) == 2:
                    conf[item[0].strip()] = item[1].strip()
            line = f.readline()
        f.close()
        return conf
    
    def load_secret(self,secret_file_path,conf):
        if os.path.exists(secret_file_path) == True:
            f = open(secret_file_path)
            line = f.readline()
            while line:
                line = line.strip()
                if line.find("#") != 0 and line.find("=") > 0:
                    item = line.split("=")
                    if len(item) == 2:
                        conf[item[0].strip()] = item[1].strip()
                line = f.readline()
            f.close()

    def print_log(self,level,msg):
        all_msg = "[%s][%s][%s][%s]" %(msg,str(datetime.datetime.now())[:19],self.function_name,level)
        print(all_msg)

    def conn_kael(self):
        self.print_log("info","start conn_kael")
        retry_times = 3
        cnx = None
        while True:
            try:
                retry_times -= 1
                cnx = pymysql.Connect(user=self.gConf['conn_kael.user'],password=self.gConf['conn_kael.pwd'],host=self.gConf['conn_kael.host'],port=int(self.gConf['conn_kael.port']),database=self.gConf['conn_kael.db'],charset='utf8')
                break
            except Exception as e:
                if retry_times == 0:
                    raise Exception(traceback.format_exc())
                self.print_log("info","retrying.....")
                time.sleep(3)
        self.print_log("info","end conn_kael")
        return cnx
            

