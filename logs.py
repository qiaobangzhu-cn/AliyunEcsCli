#-*- coding:utf-8 -*-
import logging
import gblvar
import os
import time
import sys
import json
import platform

class logs():
    def __init__(self,sysInfo,CustomInfo):
        msg=""
        self.infoType=sysInfo
        if sysInfo!=None:
            i=0
            for n in sysInfo.splitlines():
                msg=msg+ n +" "
        self.sysInfo=msg
        self.CustomInfo=CustomInfo
        self.fName=gblvar.LOGFILE
        return
    def getECSLogger(self):
        """
        if not os.path.exists(self.fName):
            print "Log files are missing, please use to perform config operations."
            sys.exit(1)
        """
        timeInfo=time.strftime('%Y-%m-%d %H:%M:%S')
        if self.CustomInfo!=None:
            self.printFormat(timeInfo,self.CustomInfo,"Error")
        else:
            msgInfo=self.sysInfo.replace(os.linesep," ")
            self.printFormat(timeInfo,self.sysInfo,"Error")
        try:
            logging.basicConfig(
                        level    = logging.DEBUG,
                        format   = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt  = '%Y-%m-%d %H:%M:%S',
                        filename = self.fName,
                        filemode = 'a');
            logging.error(self.sysInfo)


        except:
            #print "Error: An error occurred while writing log. No log write permissions."
            self.printFormat(timeInfo,'An error occurred while writing log. No log write permissions.',"Error")


    def getCustom_Log(self):
        """
        if not os.path.exists(self.fName):
            print "Log files are missing, please use to perform config operations."
            sys.exit(1)
        """
        #format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s] '
        fName=self.fName
        format= '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'
        datefmt='%Y-%m-%d %H:%M:%S'
        filemode="a"
        logging.basicConfig(filename=fName,filemode=filemode,format=format,datefmt=datefmt)

        console = logging.StreamHandler()
        # 设置日志打印格式
        """
        formatter = logging.Formatter(format)
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)
        logger = logging.getLogger('tst')
        """
        formatter = logging.Formatter(format)
        console.setFormatter(formatter)
        logging.getLogger() #  .addHandler(console)
        logger = logging.getLogger('tst')
        timeInfo=time.strftime('%Y-%m-%d %H:%M:%S')
        #print timeInfo,'Error:',self.CustomInfo
        if self.infoType=="Info":
            self.printFormat(timeInfo,self.CustomInfo,self.sysInfo)
        else:
            self.printFormat(timeInfo,self.CustomInfo,'Error')
        return logger


    def checkOutputInfo(self,info):
        return info.decode("utf-8").encode("gbk")

    def printFormat(self,DataInfo,info,infoType):

        errorJson={'messagetype':infoType,'timeInfo':DataInfo,'message':info}
        #errorXml="<root><messagetype>"+infoType+"</messagetype><timeInfo>"+DataInfo+"</timeInfo><message>"+info+"</message><root>"
        errorXml="<root>"+os.linesep
        errorXml=errorXml+"          <messagetype>"+os.linesep
        errorXml=errorXml+"                      "+infoType+os.linesep
        errorXml=errorXml+"          <messagetype>"+os.linesep
        errorXml=errorXml+"          <timeInfo>"+os.linesep
        errorXml=errorXml+"                      "+DataInfo+os.linesep
        errorXml=errorXml+"          <timeInfo>"+os.linesep
        errorXml=errorXml+"          <DataInfo>"+os.linesep
        errorXml=errorXml+"                      "+info+os.linesep
        errorXml=errorXml+"          <DataInfo>"+os.linesep
        errorXml=errorXml+"<root>"+os.linesep

        #此处将response转换成json格式，编码格式转换为 unicode
        jsoninfo = json.dumps(errorJson,sort_keys=True,indent=2,ensure_ascii=False)
        print jsoninfo

