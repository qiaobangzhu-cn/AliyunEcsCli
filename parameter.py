# -*- coding:utf-8 -*-
'''
Created on 2014-8-17

@author: ruijie.qiao
'''
from optparse import OptionParser
import gblvar
import traceback
import sys
import logs

class inputParameter():
    def __init__(self,clDict):
        self.parser = OptionParser()
        self.csDict=clDict
        return
    def reParameter(self):
        try:
            parm={}
            parm=gblvar.ecsParameters
            parmKeyList=parm.keys()
            parmKeyList.sort()

            #这个lsList保存的是 API中所有参数的小写
            lsList=[]
            #无效参数列表
            InvalidParameter={}
            for o in parmKeyList:
                lsList.append(o.lower())

            for key in self.csDict.keys():
                if not key in lsList:
                    InvalidParameter[key]=self.csDict[key]
                    #print "'"+key+"' is an invalid parameter"

            for parmkey in parmKeyList:
                key2='--'+parmkey.lower()
                key3=key2.replace('.','_')
                if key2=='--id':
                    self.parser.add_option('',self.getCsParm(key3),dest='accessid',help=parm[parmkey])
                elif key2=='--key':
                    self.parser.add_option('',self.getCsParm(key3),dest='accesskey',help=parm[parmkey])
                elif key2=='--output':
                    self.parser.add_option('',self.getCsParm(key3),dest='Format',help=parm[parmkey])
                else:
                    self.parser.add_option('',self.getCsParm(key3),dest=parmkey,help=parm[parmkey])
            for parmkey in InvalidParameter.keys():
                self.parser.add_option('','--'+InvalidParameter[parmkey],dest=parmkey.lower(),help='')
            return self.parser.parse_args()
        except:
            info = traceback.format_exc()
            CustomInfo="The input parameter format not correct, please check the input parameters"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)



    def changeCN(self,content):
        content.encode('gbk')
        return content

    def getCsParm(self,defaultStr):
        strParm=defaultStr[2:].lower()
        if strParm in self.csDict.keys():
            return "--"+self.csDict[strParm]
        else:
            return defaultStr
