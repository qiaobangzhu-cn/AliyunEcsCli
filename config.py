# -*- coding:utf-8 -*-
'''
Created on 2014-8-18

@author: ruijie.qiao
'''
import ConfigParser
import sys
import gblvar
import os
import traceback
import logs

class config():
    def __init__(self):
        return

    #将id和key保存到文件
    def set_configure2(self):
        cfg=file(gblvar.CONFIGFILE,"r")
        cfgInfo=cfg.readlines()


    #将id和key保存到文件
    def set_configure(self):
        """
        if gblvar.options.accessid is None or gblvar.options.accesskey is None:
            print "%s miss parameters, use --id=[accessid] --key=[accesskey] to specify id/key pair" % gblvar.args[0]
            sys.exit(1)
        """
        try:
            parm={}
            boolPD=False
            curSec=""
            boolID=False
            sectionName=None
            config = ConfigParser.RawConfigParser()
            if os.path.exists(gblvar.CONFIGFILE):
                config.read(gblvar.CONFIGFILE)
                #如果没有获取到【config】则表明配置文件中没有，需要添加
                section=config.sections()
                if gblvar.DEFAULTCONFIG in section:
                    sectionName=config.get(gblvar.DEFAULTCONFIG,gblvar.DEFAULTCONFIG)
                else:
                    config.add_section(gblvar.DEFAULTCONFIG)
                    #指定默认的【config】---->config指向
                    config.set(gblvar.DEFAULTCONFIG, 'config',gblvar.CONFIGSECTION)
                    #配置 日志路径
                    config.add_section(gblvar.CONFIGSECTION)
                    sectionName=gblvar.CONFIGSECTION
            else:
                config.add_section(gblvar.DEFAULTCONFIG)
                #指定默认的【config】---->config指向
                config.set(gblvar.DEFAULTCONFIG, 'config',gblvar.CONFIGSECTION)
                #配置 日志路径
                config.add_section(gblvar.CONFIGSECTION)
                sectionName=gblvar.CONFIGSECTION

            self.checkFile(gblvar.LOGFILE)

            if gblvar.options.host is not None:
                config.set(sectionName, 'host', gblvar.options.host)
            if gblvar.options.accessid is not None:
                config.set(sectionName, 'accessid', gblvar.options.accessid)
            if gblvar.options.accesskey is not None:
                config.set(sectionName, 'accesskey', gblvar.options.accesskey)
            if gblvar.options.Format is not None:
                gblvar.options.Format=self.checkOutputType(gblvar.options.Format)
                config.set(sectionName, 'output', gblvar.options.Format)

            #配置 用户的输出文本路径
            if gblvar.options.outputfile is not None:
                config.set(sectionName, 'outputfile', gblvar.options.outputfile)
                if gblvar.options.outputfile!="":
                    self.checkFile(gblvar.options.outputfile)
            #如果用户输入了RegionId，则需呀将该ID保存
            if gblvar.options.RegionId !=None:
                config.set(sectionName, 'RegionId', gblvar.options.RegionId)
            #保存用户的ZoneId
            if gblvar.options.ZoneId !=None:
                config.set(sectionName, 'ZoneId', gblvar.options.ZoneId)
            #保存用户的showURL
            if gblvar.options.showURL !=None:
                config.set(sectionName, 'showURL', gblvar.options.showURL)

            if gblvar.options.OwnerId !=None:
                config.set(gblvar.CONFIGSECTION, 'ownerid', gblvar.options.OwnerId)
            self.checkFile(gblvar.CONFIGFILE)
            cfgfile = open(gblvar.CONFIGFILE, 'w')
            config.write(cfgfile)
            CustomInfo="Your configuration is saved into %s." % gblvar.CONFIGFILE
            logs.logs("Info",CustomInfo).getCustom_Log().info(CustomInfo)
            #cfgfile.close()

        except Exception:
            self.checkFile(gblvar.LOGFILE)
            info = traceback.format_exc()
            CustomInfo="Revision of a failed save configuration information, please check the log"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #如果id和key为空，则提取文本中的参数
    def get_configure(self):
        config = ConfigParser.ConfigParser()
        try:
            config.read(gblvar.CONFIGFILE)
            try:
                gblvar.ECS_HOST = config.get(gblvar.CONFIGSECTION, 'host')
            except Exception:
                pass
            section=config.sections()
            if gblvar.options.config is None:
                config_Section=config.get(gblvar.DEFAULTCONFIG, 'config')
            else:
                config_Section=gblvar.options.config
            gblvar.ID = config.get(config_Section, 'accessid')
            gblvar.KEY = config.get(config_Section, 'accesskey')
            if gblvar.options.accessid is not None:
                gblvar.ID = gblvar.options.accessid
            if gblvar.options.accesskey is not None:
                gblvar.KEY = gblvar.options.accesskey
            if gblvar.options.host is not None:
                gblvar.ECS_HOST = gblvar.options.host
            try:
                if gblvar.options.OwnerId ==None:
                    gblvar.options.OwnerId=config.get(config_Section, 'ownerid')
            except:
                pass
            #以下加上 try 目的是即使config中没有取到对应的参数时，继续执行，取下面的参数
            if gblvar.options.Format==None:
                try:
                    gblvar.options.Format = config.get(config_Section, 'output')
                except:
                    gblvar.options.Format='json'
            else:
                gblvar.options.Format=self.checkOutputType(gblvar.options.Format)
            try:
                if gblvar.options.outputfile is None:
                    gblvar.options.outputfile=config.get(config_Section, 'outputfile')
                    if gblvar.options.outputfile==None or gblvar.options.outputfile=="":
                        gblvar.options.outputfile=None
            except:
                pass
            try:
                #如果用户没有输入了RegionId，则从配置中获取
                if gblvar.options.RegionId ==None:
                    gblvar.options.RegionId=config.get(config_Section, 'RegionId')
            except:
                pass
            try:
                #保存用户的ZoneId
                if gblvar.options.ZoneId ==None:
                    gblvar.options.ZoneId=config.get(config_Section, 'ZoneId')
            except:
                pass
            try:
                #是否在提交时显示url链接
                if gblvar.options.showURL ==None:
                    gblvar.options.showURL=config.get(config_Section, 'showURL')
            except:
                if gblvar.options.showURL==None:
                    gblvar.options.showURL='false'

        except Exception:
            if gblvar.options.accessid is not None:
                gblvar.ID = gblvar.options.accessid
            if gblvar.options.accesskey is not None:
                gblvar.KEY = gblvar.options.accesskey
            if gblvar.options.host is not None:
                gblvar.ECS_HOST = gblvar.options.host
            if len(gblvar.ID) == 0 or len(gblvar.KEY) == 0:
                info="can't get accessid/accesskey, setup use : config --id=accessid --key=accesskey"
                logs.logs(info,info).getECSLogger()
                sys.exit(1)

    def checkOutputType(self,output=None):
        ls=['json','text','table','xml']
        if output==None:
            return "json"
        else:
            if gblvar.options.Format in ls:
                return output
            else:
                info="The input parameter 'output' value is not correct, output only ['json','text','table','xml']"
                logs.logs(info,info).getCustom_Log().error(info)
                sys.exit(1)

    def checkFile(self,filePath):
        """
        检查ecs的日志文件是否存在如果不存在则根据配置文件创建创建日志文件
        :return:
        """
        try:
            (ml,fileName)=os.path.split(filePath)
            if not os.path.isfile(filePath):
                if  ml!=None and ml!="":
                    if not os.path.exists(ml):
                        os.makedirs(ml)
                if fileName!=None:
                    file1= open(filePath,'w+')
                    file1.close()
                return
        except:
            info="Create a file or folder fail. Path: ",filePath
            logs.logs(info,info).getECSLogger()
            sys.exit(1)



    def changeFilePath(self,filePath):
        #转换绝对路径为符合系统要求的路径格式
        try:
            a=filePath.split(os.path.sep)
            fp=a[0]
            for i in range(1,len(a)):
                fp=fp+os.path.sep+a[i]
            return fp
        except:
            info= "Conversion path format error, the original path format:",filePath
            logs.logs(info,info).getECSLogger()
            sys.exit(1)