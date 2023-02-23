# encoding:UTF-8
import os
import sys
import re
import contotable
import logs
import traceback
import platform

class contoText():
    def __init__(self,varJson,filePath,fileName):
        self.varJson=varJson
        self.filePath=filePath
        self.fileName=fileName
        return


    def checkValueType(self,object):
        value=None
        if isinstance(object,unicode):
            value=object.encode('utf-8')
        elif isinstance(object,bool):
            if object==True:
                value="true"
            else:
                value="false"
        elif isinstance(object,int):
            value=str(object)
        else:
            value=object
        return value

    def createUnitRowInfo(self,rowLevel,rowValue):
        rowDict={}
        rowDict["rowLevel"]=rowLevel
        rowDict["rowValue"]=rowValue
        return rowDict

    def px(self,dictObject):
        """
        排序字典
        :param dictObject:
        :return:
        """
        keyList=dictObject.keys()
        strList=[]
        dictList=[]
        lsList=[]
        a=[]
        for key in dictObject.keys():
            value=dictObject[key]
            if isinstance(value,dict):
                dictList.append(key)
            elif isinstance(value,list):
                lsList.append(key)
            else:
                strList.append(key)
        strList.sort()
        dictList.sort()
        lsList.sort()
        if len(dictList)>0:
            strList=strList+dictList
        if len(lsList)>0:
            strList=strList+lsList
        return strList

    def clDictData(self,csObject,parmKey=None,Level=1):
        #保存一行中所有单元格的数据
        cellListKey=[]
        cellListValue=[]
        #临时存储下一级数据的列表信息
        lsList=[]
        #临时存储当前行数据的列表信息
        dqList=[]
        if isinstance(csObject,dict):
            keyList=self.px(csObject)
            for key in keyList:
                value=csObject[key]
                #编码格式转换
                key=self.checkValueType(key)
                value=self.checkValueType(value)
                if isinstance(value,dict):
                    nexRowList=self.clDictData(value,key,Level+1)
                    lsList.append(self.createUnitRowInfo(Level,key))
                    lsList=lsList+nexRowList
                elif isinstance(value,list):
                    nexRowList=self.clListData(value,key,Level+1)
                    lsList.append(self.createUnitRowInfo(Level,key))
                    lsList=lsList+nexRowList
                else:
                    if value=="": value='""'
                    dqList.append(self.createUnitRowInfo(Level,key+":"+value))
            #处理字典中键值为字符串的数据，将其存储为行,  当前循环中，字典对应的值是字符串时，将其追加到一个列表中生成一行数据
            if len(lsList)>0:
                dqList=dqList+lsList
            return dqList
        else:
            CustomInfo="The wrong data type is not Dict!"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)

    def clListData(self,csObject,parmKey=None,Level=1):
        dqList=[]
        lsList=[]
        if isinstance(csObject,list):
            csObject.sort(None,None,True)
            if parmKey==None:
                CustomInfo="Argument is of type list data, need the parent node name"
                logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
                sys.exit(1)
            n=0
            for obj in csObject:
                #编码格式转换
                obj=self.checkValueType(obj)
                n=n+1
                nodeKey=parmKey+"["+str(n)+"]"
                if isinstance(obj,dict):
                    nexRowList=self.clDictData(obj,None,Level+1)
                    lsList.append(self.createUnitRowInfo(Level,nodeKey))
                    lsList=lsList+nexRowList
                elif isinstance(obj,list):
                    nexRowList=self.clListData(obj,nodeKey,Level+1)
                    lsList.append(self.createUnitRowInfo(Level,nodeKey))
                    lsList=lsList+nexRowList
                else:
                    if obj=="": obj='""'
                    dqList.append(self.createUnitRowInfo(Level,nodeKey+":"+obj))
            if len(lsList)>0:
                dqList=dqList+lsList
            return dqList
        else:
            CustomInfo="The wrong data type is not List!"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)


    def clNewData(self,csObject,parmKey=None,Level=1):
        if isinstance(csObject,dict):
            rowList=self.clDictData(csObject,parmKey,Level)
        elif isinstance(csObject,list):
            rowList=self.clListData(csObject,parmKey,Level)
        else:
            CustomInfo="The format of the data error, data must be dict or list"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)
        return rowList

    def getPrintData_gbk(self,object):
        """
        对数据中的编码问题进行解决
        :param object:
        :return:
        """
        value=None
        try:
            if isinstance(object,unicode):
                if platform.system=="Windows":
                    value=object.encode('gbk')
            elif isinstance(object,bool) or isinstance(object,int):
                value=object
            elif isinstance(object,str):
                if platform.system=="Windows":
                    value=object.decode('utf-8').encode('gbk')
                else:
                    value=object.decode('utf-8')
            return value
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def getTextData(self):
        try:
            rowListInfo=self.clNewData(self.varJson,None,1)
            rowList=[]
            rowStr=""
            for obj in rowListInfo:
                value1=self.getPrintData_gbk(obj['rowValue'])
                rowInfo=self.getPrintData_gbk("    " * int(obj['rowLevel']-1) + obj['rowValue'])
                print rowInfo
                rowStr=rowStr+rowInfo+os.linesep
            if self.fileName!=None:
                file1=file(self.fileName,'w')
                if platform.system=="Windows":
                    file1.writelines(rowStr.encode('gbk'))
                else:
                    file1.writelines(rowStr.encode('utf-8'))
                file1.close()

        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
