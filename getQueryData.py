#encoding:UTF-8
import os
import json
import logs
import traceback
import sys
import re
import queryResult


class getQueryData():
    def __init__(self,strContent,strType,query):
        self.dictinfo=json.loads(strContent)
        self.strType=strType
        self.query=query
        return

    def getClData(self,list1):
        if isinstance(list1,list):
            a=len(list1)
            if a==1:
                return self.getClData(list1[0])
            else:
                return list1
        else:
            return list1

    def getQueryData(self):
        try:
            x=queryResult.clQuery(self.query)
            queryObj=x.getQuery()
            #dictObj=self.clStrContent(self.dictinfo,queryObj)
            #先查找根节点，获取根节点下的值

            list1=self.findNodeKey(self.dictinfo,queryObj)
            list1=self.getClData(list1)

            index=queryObj.index
            listObj=[]
            dictObj2={}
            nName=queryObj.nodeKey
            safeName=queryObj.safeName
            if queryObj.safeName!=None:
                nName=safeName
            #显示查询结果的总条数
            queryTotalCount=0
            #如果有子节点，则从根节点下获取子节点的值
            if isinstance(list1,list):
                queryTotalCount=len(list1)
                for i in range(0,len(list1)):
                    nName="Find_Data_"+str(i+1)
                    dictObj2[nName]=self.findSubNode(list1[i],queryObj)
            else:
                queryTotalCount=1
                nName="Find_Data"
                dictObj2[nName]=self.findSubNode(list1,queryObj)
            #dictObj2=self.findSubNode(dictObj,queryObj)

            """
            if isinstance(list1,list):
                for i in range(0,len(list1)):
                    dictObj2[nName]=self.findSubNode(list1[i],queryObj)
            else:
                dictObj2[nName]=self.findSubNode(list1,queryObj)
            """
            if "PageNumber" in self.dictinfo.keys():
                dictObj2['PageNumber']=self.dictinfo['PageNumber']
            if "RequestId" in self.dictinfo.keys():
                dictObj2['RequestId']=self.dictinfo['RequestId']
            if "TotalCount" in self.dictinfo.keys():
                dictObj2['TotalCount']=self.dictinfo['TotalCount']
            dictObj2['queryTotalCount']=str(queryTotalCount)+" "
            return dictObj2
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)




    def clUnit(self,nodeKey,value,subNode=[],safeName=None):
        """
        没有 索引的状态下进行检索
        :param nodeKey:
        :param value:
        :param safeName:
        :param queryObj:
        :return:
        """
        #判断是否存在 安全名称 safeName，如果存在，则其关键词将更改为安全名称 并生成dict数据
        lsDict1={}
        lsDict2={}
        lsDict3={}
        if safeName==None:
            lsDict1[nodeKey]=value
        else:
            lsDict1[safeName]=value
        #根据 subNode 判断是否需要向下一级取值，subNode列表长度为0 则表示不需要向下一级取值，负责继续向下一级取值
        if len(subNode)==0:
            return lsDict1
        else:
            #当前nodeKey存在下一级，需要向下一级取值
            lsDict={}
            for qObj in subNode:
                lsDict2=self.clStrContent(value,qObj)
                for key in lsDict2.keys():
                    #将下一级的每个键值对都存储到当前nodeKey这一级别
                    lsDict3[key]=lsDict2[key]
            return lsDict3

    def getSubUnit(self,object,queryObjList,nName):
        """
        处理单个Value下的 子节点列表
        :param object: 传进来的被查询数据
        :param queryObjList: 子节点列表
        :param nName: 父节点名
        :return: 返回父节点对应的数据
        """
        clDict1={}
        clDict2={}
        clDict3={}
        listData=[]
        lenSubQ=len(queryObjList)

        if lenSubQ>0:
            lsVal=None
            for Queryobj in queryObjList:
                subKey=Queryobj.nodeKey
                if Queryobj.safeName!=None:
                    subKey=Queryobj.safeName
                if subKey in clDict2.keys():
                    info = "Do not allow the safety duplicate name: '"+ subKey +"'"
                    CustomInfo=info
                    logs.logs(info,CustomInfo).getECSLogger()
                    sys.exit(1)
                lsDict=self.findSubNode(object,Queryobj)
                if isinstance(lsDict,list):
                    clDict2[subKey]=lsDict
                else:
                    clDict2[subKey]=lsDict[subKey]
            clDict3[nName]=clDict2
            return clDict3
        else:
            clDict3[nName]=object
            return clDict3

    #提供判断并返回列表数据
    def clListData(self,object,indexN,nodeKey):
        if not isinstance(object,list):
            return False
        if indexN!="*" and indexN!=None:
            cLen=len(object)
            if int(indexN)>=cLen or int(indexN)<0:
                info="The Query parameter '"+nodeKey+"["+str(indexN)+"]"+"' index value is out of range!"
                logs.logs(None,info).getCustom_Log().error(info)
                return "error"
        return True

    def findSubNode(self,object,queryObj):
        try:
            safeName=queryObj.safeName
            nodeKey=queryObj.nodeKey
            indexN=queryObj.index
            subQueryObj=queryObj.subNode
            #子节点的数量
            lenSubQ=len(subQueryObj)
            clDict1={}
            clDict2={}
            if safeName==None:
                nName=nodeKey
            else:
                nName=safeName
            #nodeKey=self.checkValueType(nodeKey)
            #被查询对象为字典、列表、其他类型（子串，int,bool等）
            if isinstance(object,dict):
                if nodeKey in object.keys():
                    #此处无论用户有没有输入 index的值，都不对index进行判断，忽略用户输入的Query的index
                    value=object[nodeKey]

                    #对数据做List判断，如果数据格式和indexN都符合，则继续，否则报错
                    if self.clListData(value,indexN,nodeKey)=="error":
                        sys.exit(1)

                    if isinstance(value,list):
                        list1=[]
                        stopNum=len(value)
                        startNum=0
                        #当下面这个判断为True时，则表示取列表的单个元素，否则只取对应值
                        if indexN!="*" and indexN!=None:
                            startNum=int(indexN)
                            stopNum=startNum+1
                        if lenSubQ>0:
                            for i in range(startNum,stopNum):
                                clDict=self.getSubUnit(value[i],subQueryObj,nName)
                                list1.append(clDict[nName])
                            clDict1[nName]=list1
                        else:
                            for i in range(startNum,stopNum):
                                list1.append(value[i])
                            clDict1[nName]=list1
                        return clDict1
                    elif isinstance(value,dict):
                        if lenSubQ>0:
                            clDict=self.getSubUnit(value,subQueryObj,nName)
                            clDict1[nName]=clDict[nName]
                        else:
                            clDict1[nName]=[value]
                        return clDict1
                    else:
                        clDict=self.getSubUnit(value,subQueryObj,nName)
                        return clDict
                        info="Data error, data is not List or Dict"
                        logs.logs(None,info).getCustom_Log().error(info)
                        sys.exit(1)
                else:
                    #nodeKey不存在于当前 dict 的keys中,则对字典的values值进行遍历寻找
                    info="Key '"+nodeKey+"' does not exist in the dictionary data error"
                    logs.logs(None,info).getCustom_Log().error(info)
                    sys.exit(1)
            elif isinstance(object,list):
                list1=[]
                stopNum=len(object)
                pd=True
                startNum=0
                if indexN==None or indexN=="*":
                    pd=True
                else:
                    if int(indexN)>=stopNum or int(indexN)<0:
                        info="The Query parameter '"+nodeKey+"["+str(indexN)+"]"+"' index value is out of range!"
                        logs.logs(None,info).getCustom_Log().error(info)
                        sys.exit(1)
                    else:
                        pd=False
                        startNum=int(indexN)
                        stopNum=int(indexN)+1
                #对object列表中的每个对象进行queryObj查询，
                for i in range(startNum,stopNum):
                    obj=object[i]
                    clDict=self.findSubNode(obj,queryObj)
                    if isinstance(clDict,list):
                        list1.append(clDict)
                    else:
                        list1.append(clDict[nName])
                clDict1[nName]=list1
                return clDict1
            else:
                #"被查询的数据只能是字典或者列表！
                info="Data query is only a dictionary or list!"
                logs.logs(None,info).getCustom_Log().error(info)
                sys.exit(1)

        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def findNodeKey(self,object,queryObj):
        """
        寻找根节点，至查找跟节点，并将根节点与其值组成字典返回
        """
        try:
            safeName=queryObj.safeName
            nodeKey=queryObj.nodeKey
            indexN=queryObj.index
            subQueryObj=queryObj.subNode
            clDict1={}
            DataList=[]
            nName=nodeKey
            if safeName!=None:
                nName=safeName
            if isinstance(object,dict):
                #nodeKey在当前 dict 的keys中
                if nodeKey in object.keys():
                    #nodeKey在当前 dict 的keys中

                    if indexN==None:
                        #没有索引时直接取值
                        clDict1[nName]=object[nodeKey]
                        return clDict1
                        #DataList.append(clDict1)
                        #return DataList
                    else:
                        #nodeKey有索引，则先对nodekey对应的值进行判断，判断是否为列表，如果不是列表，则反回错误，否则反悔其索引对应的值
                        value=object[nodeKey]
                        if not isinstance(value,list):
                            #数据字典中 nodeKey对应的值不是列表类型,程序不取用户输入的索引
                            #info="The data of '"+nodeKey+"' values is not of type list!"
                            #logs.logs(None,None).getCustom_Log().error(info)
                            clDict1[nName]=value
                            return clDict1
                            """
                            #数据字典中 nodeKey对应的值不是列表类型
                            info="The data of '"+nodeKey+"' values is not of type list!"
                            logs.logs(None,None).getCustom_Log().error(info)
                            sys.exit(1)
                            """
                        clDict1[nName]=object[nodeKey]
                        return clDict1
                        #DataList.append(clDict1)
                        #return DataList

                else:
                    #nodeKey不存在于当前 dict 的keys中,则对字典的values值进行遍历寻找
                    for unitDict in object.values():
                        dictValue=self.findNodeKey(unitDict,queryObj)
                        if dictValue!=None and len(dictValue)>0:
                            #如果字典不为空，且字典里面有内容，则反回字典
                            #return dictValue
                            DataList.append(dictValue)
                    DataList=self.getClData(DataList)
                    return DataList
            elif isinstance(object,list):
                #如果是列表，则对列表中的每个值进行遍历
                for obj in object:
                    clDict1=self.findNodeKey(obj,queryObj)
                    if clDict1!=None and len(clDict1)>0:
                        #return clDict1
                        DataList.append(clDict1)
                DataList=self.getClData(DataList)
                return DataList
                #数据中没有找到键值 Key
                info="Key '"+nodeKey+"' was not found in the data."
                logs.logs(None,info).getCustom_Log().error(info)
                sys.exit(1)

            else:
                #如果输入参数中 第一个参数不是dict/list 则反回None
                return None
                #"数据错误，被查询对象必须是字典或列表
                info="Data error, by the object must be a dictionary or list query"
                logs.logs(None,info).getCustom_Log().error(info)
                sys.exit(1)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def checkValueType(self,object):
        value=None
        try:
            if isinstance(object,unicode):
                value=object.encode('utf-8')
            elif isinstance(object,bool):
                if object==True:
                    value="true"
                else:
                    value="false"
            elif isinstance(object,int):
                value=str(object)
            elif isinstance(object,str):
                value=object.decode('utf-8')
            else:
                value=object
            return value
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def clStrContent(self,clDictData,queryObj):
        try:
            safeName=queryObj.safeName
            nodeKey=queryObj.nodeKey
            indexN=queryObj.index
            subQueryObj=queryObj.subNode

            if isinstance(clDictData,dict):
                #nodeKey在当前 dict 的keys中
                if nodeKey in clDictData.keys():
                    #nodeKey在当前 dict 的keys中
                    pass
                else:
                    #nodeKey不存在于当前 dict 的keys中
                    pass
            elif isinstance(clDictData,list):
                pass
            else:
                pass

            #节点名是否存在于 clDictData的第一级keys()中
            if nodeKey in clDictData.keys():
                value=clDictData[nodeKey]
                #判断是否存在 索引，如果存在索引，则根据索引值判断是否需要在字典外层套上list
                if indexN==None:
                    return self.clUnit(nodeKey,value,subQueryObj,safeName)
                elif indexN=="*":
                    if isinstance(value,list):
                        #创建列表，预存储值
                        listDict=[]
                        clDict={}
                        for i in range(0,len(value)):
                            #判断是否存在 安全名称 safeName，如果存在，则其关键词将更改为安全名称 并生成dict数据
                            UnitValue=value[i]
                            unitDict=self.clUnit(nodeKey,UnitValue,subQueryObj,safeName)
                            listDict.append(unitDict)
                        clDict[nodeKey]=listDict
                        return clDict
                    else:
                        #数据格式错误，参数 nodeKey对应的值不是列表！
                        info="Data format error, parameter '"+nodeKey+"' values not list!"
                        logs.logs(None,info).getCustom_Log().error(info)
                        sys.exit(1)
                else:
                    #nodeKey有索引，且索引只有一个值
                    #此处需要加判断，判断索引是否超出范围 ?????
                    value=value[int(indexN)]
                    #判断是否存在 安全名称 safeName，如果存在，则其关键词将更改为安全名称 并生成dict数据
                    return self.clUnit(nodeKey,value,subQueryObj,safeName)
            else:
                #如果 nodeKey 不在clDictData的keys中，则对clDictData的values进行判断
                pass
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def printGetQData(self,divDict):
        for key in divDict.keys():
            value=divDict[key]
            print key,"---------->",value
        dictinfo=json.dumps(divDict)
        print dictinfo.encode("utf-8")