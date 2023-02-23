# encoding:UTF-8
import os
import json
import logs
import traceback
import sys
import re

class queryCustom():
    def __init__(self,nodeKey=None,safeName=None,index=None,subNode=None):
        """
        相当于自定义的数据结构
        qType---->｛nodeKey:str,  index:x,   subNode:[qType,qType,qType,qType]｝
        :param nodeKey:  对象名
        :param index:
        :param subNode:
        :return:
        """
        self.nodeKey=nodeKey
        self.index=index
        self.subNode=[]
        self.safeName=safeName
        if subNode!=None:
            self.subNode.append(subNode)
        return
class clQuery():
    def __init__(self,query):
        #self.jsonStr=json.dumps(json.loads(jsonStr.strip()))
        self.query=query
        return

    def testPrintQC(self,object,n):
        print "          "*n,"节点名------>",object.nodeKey
        print "          "*n,"index------>",object.index
        print "          "*n,"safeName------>",object.safeName
        print "          "*n,"subNode------>"
        print "          "*n,"+++++++++++++++++++++++++++++"
        if object.subNode!=None:
            for o in object.subNode:
                self.testPrintQC(o,n+1)


    def getQuery(self):
        """
        返回数据类型如下：
        qType---->｛nodeKey:str, 节点名
                    safeName：name  安全别名
                    index:x,     节点名的index
                    subNode:[    节点名下的参数
                        qType,
                        qType
                        ]
                        ｝
        :return:
        """
        #将Query数据分解成两部分处理，以“.{”作为分割
        try:
            list1=self.query.split(".{")
            lsLen=len(list1)
            if len(list1)>2:
                CustomInfo="The Query data format is not correct.The correct format:A.B[*].{A,B,C[*].id}"
                logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
                sys.exit(1)
            if lsLen==2:
                befStr=list1[0]
                lastStr=list1[1][:len(list1[1])-1]
                #必须先计算后面的数据
                lasList=self.clLastQueryData(lastStr)
                befList=self.clBefQueryData(befStr)

                kQc=befList[len(befList)-1]
                for o in lasList:
                    kQc.subNode.append(o)
                qc=self.clListQc(befList)
                return qc
            elif lsLen==1:
                befStr=list1[0]
                befList=self.clBefQueryData(befStr)
                qc=self.clListQc(befList)
                return qc
            else:
                CustomInfo=""
                logs.logs(None,CustomInfo).getECSLogger()
                sys.exit(1)
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="The Query data format is not correct.The correct format:'Permissions[1].ABC[0].{AKF:Permission[0],BBC[0].id}'"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def clListQc(self,list1):
        """
        将列表里 qc类型的值生成一个qc值
        :param list1:
        :return:
        """
        qK=None
        for i in range(len(list1)-1,-1,-1):
            if qK!=None:
                list1[i].subNode.append(qK)
                qK=list1[i]
            else:
                qK=list1[i]
        return qK

    def clUnitQuery(self,unitQuery):
        """
        处理并生成单个节点
        :param unitQuery:
        :return:
        """
        intQ=unitQuery.find(".")
        if intQ==-1:
            intB=unitQuery.find("[")
            intL=unitQuery.find("]")
            if intB==-1:
                nodeKey=unitQuery
                qc=queryCustom(nodeKey,None,None,None)
                return qc
            else:
                indexN=unitQuery[intB+1:intL]
                nodeKey=unitQuery[:intB]
                qc=queryCustom(nodeKey,None,indexN,None)
                return qc
        else:
            list1=unitQuery.split(".")
            list2=[]
            for o in list1:
                qc1=self.clUnitQuery(o)
                list2.append(qc1)
            qc=self.clListQc(list2)
            return qc

    def clBefQueryData(self,befQuery):
        """
        处理并生成一个qc的列表，该列表顺序不可变
        :param befQuery:
        :return:
        """
        list1=befQuery.split(".")
        list2=[]
        for o in list1:
            qc=self.clUnitQuery(o)
            list2.append(qc)
        return list2

    def clLastQueryData(self,lasQuery):
        list1=lasQuery.split(",")
        list2=[]
        list5=[]
        for object in list1:
            m=object.find(":")
            if m!=-1:
                list3=object.split(":")
                safeName=list3[0]
                qc=self.clUnitQuery(list3[1])
                qc.safeName=safeName
            else:
                qc=self.clUnitQuery(object)
            list5.append(qc)
        return list5