# -*- coding:UTF-8 -*-
import os
import sys
import json
import logs
import traceback
import platform

class contoXML():
    def __init__(self):
        return

    def clBefTag(self,tag,level=0):
        if tag !=None and tag!="":
            return "        "*int(level) + "<"+tag+">"
    def clLasTag(self,tag,level=0):
        if tag !=None and tag!="":
            return "        "*int(level) + "</"+tag+">"
    def clMidValue(self,value,level=1):
        if value !=None:
            return "        "*int(level) + str(value)

    def clTag(self,tag):
        if tag[len(tag)-2:]=="es":
            return tag[:len(tag)-2]
        elif tag[len(tag)-1:]:
            return tag[:len(tag)-1]
        else:
            return tag


    def dictToXml(self,dictData,tag,level):
        """

        """
        xmlStr=""
        xmlStrList=[]
        keyList=[]
        keyList=dictData.keys()
        keyList.sort()
        for key in keyList:
            if isinstance(dictData[key],dict):
                xmlStrList.append(self.clBefTag(key,int(level)))
                xmlStrList=xmlStrList+(self.dictToXml(dictData[key],None,int(level)+1))
                xmlStrList.append(self.clLasTag(key,int(level)))
            elif isinstance(dictData[key],list):
                xmlStrList.append(self.clBefTag(key,int(level)))
                xmlStrList=xmlStrList+(self.listToXml(dictData[key],key,int(level)+1))
                xmlStrList.append(self.clLasTag(key,int(level)))
            else:
                xmlStr=""
                xmlStr=self.checkValueType(self.clBefTag(key,int(level)))
                xmlKK=self.checkValueType(dictData[key])
                xmlStr=xmlStr+xmlKK+self.checkValueType("</"+key+">")

                xmlStrList.append(xmlStr)
        return xmlStrList



    def listToXml(self,listData,tag,level):
        xmlStr=""
        xmlStrList=[]
        newTag=self.clTag(tag)
        for value in listData:
            if isinstance(value,dict):
                xmlStrList.append(self.clBefTag(newTag,int(level)))
                xmlStrList=xmlStrList+self.dictToXml(value,None,int(level)+1)
                xmlStrList.append(self.clLasTag(newTag,int(level)))
            elif isinstance(value,list):
                xmlStrList.append(self.clBefTag(newTag,int(level)))
                xmlStrList=xmlStrList+self.listToXml(value,None,int(level)+1)
                xmlStrList.append(self.clLasTag(newTag,int(level)))
            else:
                xmlStr=self.checkValueType(self.clBefTag(newTag,int(level)))
                strK=self.checkValueType(value)
                xmlStr=xmlStr+strK+self.checkValueType("</"+newTag+">")
                xmlStrList.append(xmlStr)
        return xmlStrList

    def checkValueType(self,object):
        value=None
        try:
            if isinstance(object,unicode):
                sysstr = platform.system()
                if(sysstr =="Windows"):
                    value=object.encode('gbk')
                else:
                    value=object.encode('utf-8')
            elif isinstance(object,bool):
                if object==True:
                    value="true"
                else:
                    value="false"
            elif isinstance(object,int):
                value=str(object)
            elif isinstance(object,float):
                value=str(object)
            elif isinstance(object,str):
                value=object
            else:
                value=object
            return value
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)



    def getDictToXml(self,dictData,outputPath=None):
        """
        外部调用时传入 字典和 xml结果的存储路径
        """
        try:
            xmlStrList=[]
            newXmlList=[]
            xmlStr=""
            tag="root"
            sysstr = platform.system()
            #开头
            befStr=self.clBefTag("root",0)
            newXmlList.append(self.checkValueType(befStr+os.linesep))

            xmlStr=xmlStr+self.checkValueType(befStr+os.linesep)

            xmlStrList=self.dictToXml(dictData,tag,1)
            for o in xmlStrList:
                newXmlList.append(self.checkValueType(o +os.linesep))
                xmlStr=xmlStr+self.checkValueType(o+os.linesep)
            #结尾
            lasStr=self.clLasTag("root",0)
            xmlStr=xmlStr+self.checkValueType(lasStr+os.linesep)
            newXmlList.append(self.checkValueType(lasStr+os.linesep))

            print xmlStr
            #保存到文本
            try:
                if outputPath!=None:
                    file2=open(outputPath,'w')
                    file2.write(xmlStr)
                    file2.close()
            except:
                CustomInfo="No permission to write the file, or the path error."
                logs.logs("Error",CustomInfo).getCustom_Log().error(CustomInfo)
                sys.exit(1)

        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)