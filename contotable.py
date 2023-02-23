# encoding:UTF-8
import os
import sys
import re
import logs
import traceback
import platform

class contotable():
    def __init__(self,varJson,filePath,fileName):
        self.varJson=varJson
        self.filePath=filePath
        self.fileName=fileName
        return

    #转为A:[]类型准备的函数
    def clListData2(self,key,listData,rowLevel):
        """
        接受一个字典参数
        返回值如下：
        tableRowList=｛
                        maxLen:lenNum 最大宽度的字符长度
                        maxCol:Num
                        rowLis[
                                {colNum:Num   本行有几列
                                rowLevel:Num  本行缩进几级
                                colValue:[value1,value2]   本行单元格中的值
                                }
                        ]
                    ｝
        """
        returnDict={}  #返回字典
        strLenList=[]     # 字符串长度列表
        colList=[]      #记录所有的列数
        maxLen=0       #最长的字符串长度
        maxCol=0       #最多的列数

        rowList=[]
        #下面几个参数相当----------》rowLis
        colNum=0      #当前行的列数
        rowRs1=[]     #单元格中的值-----》colValue
        rowRs2=[]     #单元格中的值-----》colValue

        rowDict={}  #表格单行的级别信息等-----------》rowList 下面的 ｛｝
        rowDict2={}  #表格单行的级别信息等-----------》rowList 下面的 ｛｝

        n=0
        try:
            list3=[]
            for obj in listData:
                newKey=key+"["+ str(n) +"]"
                strLenList.append(len(newKey))  # 字符串长度统计
                colList.append(1)      #---------------》colValue[]
                rowDict=self.createRowDict(1,rowLevel,[newKey])
                rowList.append(rowDict)
                if isinstance(obj,dict):
                    nodeRowDict=self.clData(obj,rowLevel+1)
                    for o in nodeRowDict["rowList"]:
                        rowList.append(o)
                    strLenList.append(nodeRowDict["maxLen"])
                    colList.append(nodeRowDict["maxCol"])
                elif isinstance(obj,list):
                    nodeRowDict=self.clListData2(key,obj,rowLevel+1)
                    list3.append(nodeRowDict)
                else:
                    rowList.append(obj)
                    pass
                n=n+1
            if len(list3)>0:
                for nodeRow in list3:
                    colList.append(n)
                    colList.append(nodeRowDict["maxCol"])
                    strLenList.append(nodeRowDict["maxLen"])
                    for dictObj in nodeRow["rowList"]:
                        rowList.append(dictObj)

            maxCol=max(colList) #获取最多的列表数
            maxLen=max(strLenList) #计算最大的字符串长度
            returnDict["maxCol"]=maxCol
            returnDict["maxLen"]=maxLen
            returnDict["rowList"]=rowList
            return returnDict
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)


    def createRowDict(self,colNum,rowLevel,colValue):
        """
        反回生成下列类型的字典
        {colNum:Num   本行有几列
        rowLevel:Num  本行缩进几级
        colValue:[value1,value2]   本行单元格中的值
         }
        :return:
        """
        return {"colNum":colNum,"rowLevel":rowLevel,"colValue":colValue}
        pass
    def createUnitRowInfo(self,rowLevel,cellList,cellType):
        rowDict={}
        rowDict["rowLevel"]=rowLevel
        rowDict["cellList"]=cellList
        rowDict["cellType"]=cellType
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

    def clDictData(self,csObject,rowLevel,parmKey=None):
        #保存一行中所有单元格的数据
        cellListKey=[]
        cellListValue=[]
        #临时存储下一级数据的列表信息
        lsList=[]
        #临时存储当前行数据的列表信息
        dqList=[]
        if isinstance(csObject,dict):
            keyList=self.px(csObject)
            rowDict1=None
            rowDict2=None
            for key in keyList:
                value=csObject[key]
                #编码格式转换
                key=self.checkValueType(key)
                value=self.checkValueType(value)
                if isinstance(value,dict):
                    #nexRowList=self.clDictData(value,int(rowLevel)+1,key)
                    nexRowList=self.clDictData(value,int(rowLevel),key)
                    clDict1=self.createUnitRowInfo(rowLevel,[key],'title')
                    lsList.append(clDict1)
                    lsList=lsList+nexRowList
                elif isinstance(value,list):
                    #nexRowList=self.clListData(value,int(rowLevel)+1,key)
                    nexRowList=self.clListData(value,int(rowLevel),key)
                    lsList=lsList+nexRowList
                else:
                    cellListKey.append(key)
                    cellListValue.append(value)
            #处理字典中键值为字符串的数据，将其存储为行,  当前循环中，字典对应的值是字符串时，将其追加到一个列表中生成一行数据
            if len(cellListKey)>0:
                rowDict1=self.createUnitRowInfo(rowLevel,cellListKey,'title')
                rowDict2=self.createUnitRowInfo(rowLevel,cellListValue,'value')
                dqList.append(rowDict1)
                dqList.append(rowDict2)
            if len(lsList)>0:
                dqList=dqList+lsList
            return dqList
        else:
            CustomInfo="The wrong data type is not Dict!"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)

    def clListData(self,csObject,rowLevel,parmKey=None):
        dqList=[]
        lsList=[]
        cellListKey=[]
        cellListValue=[]
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
                nodeKey=parmKey+"["+str(n)+"]"
                dictNodeKey=self.createUnitRowInfo(rowLevel,[nodeKey],'title')
                if isinstance(obj,dict):
                    nexRowList=self.clDictData(obj,int(rowLevel)+1,None)
                    lsList.append(dictNodeKey)
                    lsList=lsList+nexRowList
                elif isinstance(obj,list):
                    nexRowList=self.clListData(obj,int(rowLevel),nodeKey)
                    lsList=lsList+nexRowList
                else:
                    cellListKey.append(nodeKey)
                    cellListValue.append(obj)
                n=n+1
            if len(cellListKey)>0:
                rowDict1=self.createUnitRowInfo(rowLevel,cellListKey,'title')
                rowDict2=self.createUnitRowInfo(rowLevel,cellListValue,'value')
                dqList.append(rowDict1)
                dqList.append(rowDict2)
            if len(lsList)>0:
                dqList=dqList+lsList
            return dqList
        else:
            CustomInfo="The wrong data type is not List!"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)


    def clNewData(self,csObject,rowLevel,parmKey=None):
        """
        返回行的数据格式， rowList=[rowDict,rowDict,rowDict,rowDict]
        返回的列表元素值的格式rowDict:{
                                rowLevel:行级别
                                colValue:[单元格的值列表]
                            }
        :param csObject:
        :param rowLevel:
        :param parmKey:
        :return:
        """

        #每行数据存储到列表中
        rowList=[]
        #字典数据中，keyList 和value列表
        if isinstance(csObject,dict):
            rowList=self.clDictData(csObject,rowLevel,parmKey)
        elif isinstance(csObject,list):
            if parmKey==None:
                parmKey="Find_Data"
            rowList=self.clListData(csObject,rowLevel,parmKey)
        else:
            CustomInfo="The format of the data error, data must be dict or list"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)
        return rowList

    #根据输入数据设置中间单元格格式
    def getUnitCss(self,uWidth,obj):
        """
        计算每个单元格中值的前后空格数，原则上取整数，多余的宽度将会被算在最末尾的单元格上
        """
        intLen=0
        try:
            count=self.getCN_Count(obj)   #当前行为 字符串中有中文字符时，表格会变小
            if count>0:
                uWidth=uWidth+count
            obj=self.checkValueType(obj)
            if isinstance(obj,str):
                intLen=len(obj)
            elif obj=="":
                intLen=0
            intBef=(uWidth-intLen)/2
            intLas=uWidth-intLen-intBef
            return {"intBef":intBef,"intLas":intLas,"intLen":intLen}
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def getUnitCssCN(self,uWidth,obj):
        """
        计算每个单元格中值的前后空格数，原则上取整数，多余的宽度将会被算在最末尾的单元格上
        """
        intLen=0
        try:
            count=self.getCN_Count(obj)   #当前行为 字符串中有中文字符时，表格会变小
            if count>0:
                uWidth=uWidth+count
            obj=self.checkValueType(obj)
            if isinstance(obj,str):
                intLen=len(obj)
            elif obj=="":
                intLen=0
            intBef=(uWidth-intLen)/2
            if count>0:
                intLas=uWidth-intLen-intBef + (count/2)
            else:
                intLas=uWidth-intLen-intBef
            return {"intBef":intBef,"intLas":int(intLas),"intLen":intLen}
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #根据行数据列表打印出格式数据
    def setTableCss(self,maxCol,maxStrLen):
        """
        根据最大的字符串长度和最长的单元格数，计算出最合适的总体表格宽度和列数
        :param maxCol:
        :param maxStrLen:
        :return:tableWidth,unitWidth
        """
        try:
            unitWidth=maxStrLen +4 #给出单元格宽度
            tableWidth=unitWidth * maxCol
            return {"unitWidth":unitWidth,"tableWidth":tableWidth}
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
            else:
                value=object
            return value
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    def getCN_Count(self,object):
        try:
            str1=""
            iconvcontent=object
            if not isinstance(object,unicode):
                if not isinstance(object,int):
                    iconvcontent=iconvcontent.decode("utf-8")
                else:
                    return 0
            zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
            match = zhPattern.findall(iconvcontent)
            if len(match)>0:
                for obj in match:
                    obj=obj.encode("gbk")
                    str1=str1+obj
                return len(str1)/2
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def setRowFormat(self,rowDict,tableCss):
        """
        rowDict:{colNum:Num   本行有几列
                 rowLevel:Num  本行缩进几级
                 colValue:[value1,value2]   本行单元格中的值
                 }
        存在三种情况，1.该行只有一个单元格  不设置行的底部
                      2.该行有多个单元格    设置行的底部
        :return:
        """
        try:
            returnList={}
            returnListCN={}
            colNum=rowDict["colNum"]
            rowLevel=rowDict["rowLevel"]
            m=len(rowDict["colValue"])
            object=rowDict["colValue"]
            tableWidth=tableCss["tableWidth"] #单元格的总宽度
            if colNum==1:
                sideStr="|" * (rowLevel-1)+"|"
                leftTopStr="|" *(rowLevel-1) +"+"
                rightTopStr= "+" +"|" *(rowLevel-1)

                obj=self.checkValueType(object[0])
                unitCss=self.getUnitCss(tableWidth,str(obj)+sideStr+sideStr)
                rowStr=sideStr+ " " * unitCss["intBef"] +   str(obj) +" " * unitCss["intLas"] +sideStr

                unitCss=self.getUnitCss(tableWidth,leftTopStr+rightTopStr)
                topStr=leftTopStr + "-" *(unitCss["intBef"]+unitCss["intLas"])+rightTopStr
            else:
                #获取行中间部分的单元格内容

                uWidth=tableWidth/colNum    #确认改行单元格中前 colNum-1 个单元格的总体宽度
                leftStr="|" * (rowLevel-1) +"|"
                leftTopStr="+" *(rowLevel-1)
                leftTopStr="|"+leftTopStr
                #leftTopStr="|" *(rowLevel-1) +"+"

                obj=self.checkValueType(object[0])

                unitCss=self.getUnitCss(uWidth,str(obj)+leftStr)
                intBef=unitCss["intBef"]
                intLas=unitCss["intLas"]
                firstCellStr=leftStr+" " *intBef + str(obj) + " " * (intLas-1) +"|"
                firstCellTopStr=leftTopStr+"-" * (uWidth-1-len(leftTopStr)) +"+"
                midCellStr=""
                midCellTopStr=""
                for n in range(1,m-1):
                    unitCss=self.getUnitCss(uWidth,object[n])
                    intBef=unitCss["intBef"]
                    intLas=unitCss["intLas"]
                    obj=self.checkValueType(object[n])
                    midCellStr=midCellStr+" " * intBef + str(obj) + " " * (intLas-1) +"|"
                    midCellTopStr=midCellTopStr+"-" * (uWidth-1) +"+"
                rightStr="|"+ "|" *(rowLevel-1)

                rightTopStr= "+" *(rowLevel-1)
                rightTopStr= rightTopStr+"|"


                obj=self.checkValueType(object[m-1])

                unitCss=self.getUnitCss(tableWidth-uWidth*(colNum-1),str(obj)+rightStr)
                intBef=unitCss["intBef"]
                intLas=unitCss["intLas"]
                lastCellStr=" " *intBef + str(obj) + " " * intLas + rightStr

                lastCellTopStr="-" * (tableWidth-uWidth*(colNum-1)-len(rightTopStr)) + rightTopStr

                rowStr=firstCellStr+midCellStr+lastCellStr
                topStr=firstCellTopStr+midCellTopStr+lastCellTopStr
            returnList["rowStr"]=rowStr
            returnList["topStr"]=topStr
            return returnList
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def setRowFormatCN(self,rowDict,tableCss):
        """
        rowDict:{colNum:Num   本行有几列
                 rowLevel:Num  本行缩进几级
                 colValue:[value1,value2]   本行单元格中的值
                 }
        存在三种情况，1.该行只有一个单元格  不设置行的底部
                      2.该行有多个单元格    设置行的底部
        :return:
        """
        try:
            returnList={}
            returnListCN={}
            colNum=rowDict["colNum"]
            rowLevel=rowDict["rowLevel"]
            m=len(rowDict["colValue"])
            object=rowDict["colValue"]
            tableWidth=tableCss["tableWidth"] #单元格的总宽度
            if colNum==1:
                sideStr="|" * (rowLevel-1)+"|"
                leftTopStr="|" *(rowLevel-1) +"+"
                rightTopStr= "+" +"|" *(rowLevel-1)

                obj=self.checkValueType(object[0])
                unitCss=self.getUnitCssCN(tableWidth,str(obj)+sideStr+sideStr)
                rowStr=sideStr+ " " * unitCss["intBef"] +   str(obj) +" " * unitCss["intLas"] +sideStr

                unitCss=self.getUnitCssCN(tableWidth,leftTopStr+rightTopStr)
                topStr=leftTopStr + "-" *(unitCss["intBef"]+unitCss["intLas"])+rightTopStr
            else:
                #获取行中间部分的单元格内容

                uWidth=tableWidth/colNum    #确认改行单元格中前 colNum-1 个单元格的总体宽度
                leftStr="|" * (rowLevel-1) +"|"
                leftTopStr="+" *(rowLevel-1)
                leftTopStr="|"+leftTopStr
                #leftTopStr="|" *(rowLevel-1) +"+"

                obj=self.checkValueType(object[0])

                unitCss=self.getUnitCssCN(uWidth,str(obj)+leftStr)
                intBef=unitCss["intBef"]
                intLas=unitCss["intLas"]
                firstCellStr=leftStr+" " *intBef + str(obj) + " " * (intLas-1) +"|"
                firstCellTopStr=leftTopStr+"-" * (uWidth-1-len(leftTopStr)) +"+"
                midCellStr=""
                midCellTopStr=""
                for n in range(1,m-1):
                    unitCss=self.getUnitCssCN(uWidth,object[n])
                    intBef=unitCss["intBef"]
                    intLas=unitCss["intLas"]
                    obj=self.checkValueType(object[n])
                    midCellStr=midCellStr+" " * intBef + str(obj) + " " * (intLas-1) +"|"
                    midCellTopStr=midCellTopStr+"-" * (uWidth-1) +"+"
                rightStr="|"+ "|" *(rowLevel-1)

                rightTopStr= "+" *(rowLevel-1)
                rightTopStr= rightTopStr+"|"


                obj=self.checkValueType(object[m-1])

                unitCss=self.getUnitCssCN(tableWidth-uWidth*(colNum-1),str(obj)+rightStr)
                intBef=unitCss["intBef"]
                intLas=unitCss["intLas"]
                lastCellStr=" " *intBef + str(obj) + " " * intLas + rightStr

                lastCellTopStr="-" * (tableWidth-uWidth*(colNum-1)-len(rightTopStr)) + rightTopStr

                rowStr=firstCellStr+midCellStr+lastCellStr
                topStr=firstCellTopStr+midCellTopStr+lastCellTopStr
            returnList["rowStr"]=rowStr
            returnList["topStr"]=topStr
            return returnList
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def printTableData(self,tableRowList):
        """
        tableRowList=｛
                        maxLen:lenNum 最大宽度的字符长度
                        maxCol:Num
                        rowLis[
                                {colNum:Num   本行有几列
                                rowLevel:Num  本行缩进几级
                                colValue:[value1,value2]   本行单元格中的值
                                }
                        ]
                    ｝
        """
        try:
            setCss=self.setTableCss(tableRowList["maxCol"],tableRowList["maxLen"])
            unitWidth=setCss["unitWidth"] #单元格的宽度
            tableWidth=setCss["tableWidth"] #单元格的总宽度
            listList=[]
            topStr="+"+"-" * (tableWidth-2)+"+"
            listList.append(topStr+os.linesep)
            for rowDict in tableRowList["rowList"]:
                rowD=self.setRowFormat(rowDict,setCss)
                listList.append(rowD["rowStr"]+os.linesep)
                listList.append(rowD["topStr"]+os.linesep)
            return listList
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def printTableDataCN(self,tableRowList):
        """
        tableRowList=｛
                        maxLen:lenNum 最大宽度的字符长度
                        maxCol:Num
                        rowLis[
                                {colNum:Num   本行有几列
                                rowLevel:Num  本行缩进几级
                                colValue:[value1,value2]   本行单元格中的值
                                }
                        ]
                    ｝
        """
        try:
            setCss=self.setTableCss(tableRowList["maxCol"],tableRowList["maxLen"])
            unitWidth=setCss["unitWidth"] #单元格的宽度
            tableWidth=setCss["tableWidth"] #单元格的总宽度
            listList=[]
            topStr="+"+"-" * (tableWidth-2)+"+"
            listList.append(topStr+os.linesep)
            for rowDict in tableRowList["rowList"]:
                rowD=self.setRowFormatCN(rowDict,setCss)
                listList.append(rowD["rowStr"]+os.linesep)
                listList.append(rowD["topStr"]+os.linesep)
            return listList
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)



    def changeData(self,rowList):
        """
        反回生成下列类型的字典
        {colNum:Num   本行有几列
        rowLevel:Num  本行缩进几级
        colValue:[value1,value2]   本行单元格中的值
         }
        :return:
        """
        colNum=0
        rowLevel=0
        if isinstance(rowList,list):
            strLenList=[]
            colNumList=[]
            lsList=[]
            returnDict={}
            for dictObj in rowList:
                cellList=dictObj["cellList"]
                colNum=len(cellList)
                lsDict=self.createRowDict(colNum,dictObj["rowLevel"],cellList)
                lsList.append(lsDict)
                colNumList.append(colNum)
                for obj in cellList:
                    strLenList.append(len(obj))
            maxCol=max(colNumList) #获取最多的列表数
            maxLen=max(strLenList) #计算最大的字符串长度
            returnDict["maxCol"]=maxCol
            returnDict["maxLen"]=maxLen
            returnDict["rowList"]=lsList
            return returnDict
        else:
            CustomInfo="Data type error, given data is not list"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)
        #return {"colNum":colNum,"rowLevel":rowLevel,"colValue":colValue}
    def splitList(self,rowList,splitNum,isTV=True):
        #将一行数据分割成指定的列数
        lsList=[]
        newRowList=[]
        n=len(rowList)
        if n>splitNum:
            lsList=rowList[0:splitNum]
            lsList2=self.splitList(rowList[splitNum:],splitNum,isTV)
            newRowList.append(lsList)
            newRowList=newRowList+lsList2
        else:
            i=splitNum-len(rowList)
            if isTV:
                for x in range(0,i):
                    rowList.append(' ')
            newRowList.append(rowList)
        return newRowList

    def splitRowList(self,rowDict,splitNum,isTV=True):
        lsList=self.splitList(rowDict['cellList'],splitNum,isTV)
        newRowList=[]
        for o in lsList:
            lsDict=self.createUnitRowInfo(rowDict['rowLevel'],o,rowDict['cellType'])
            newRowList.append(lsDict)
        return newRowList

    def fgRow(self,rowListInfo,splitNum):
        newRowListInfo=[]
        colNumList=[]
        lsList=[]
        maxColNum=0
        maxLevel=0
        levelList=[]
        strLenList=[]
        newRowList=[]
        rowCount=len(rowListInfo)
        n=0
        for o in rowListInfo:
            lsList.append(len(o['cellList']))
        maxColNum=max(lsList)
        if splitNum>maxColNum:
            splitNum=maxColNum
        while n <rowCount:
            dict1=rowListInfo[n]
            if  n+1 < rowCount:
                dict2=rowListInfo[n+1]
                if dict2['cellType']=='value':
                    list1=self.splitRowList(dict1,splitNum,True)
                    list2=self.splitRowList(dict2,splitNum,True)
                    m=0
                    for m in range(0,len(list1)):
                        newRowList.append(list1[m])
                        newRowList.append(list2[m])
                    n=n+2
                else:
                    list1=self.splitRowList(dict1,splitNum,False)
                    newRowList=newRowList+list1
                    n=n+1
            else:
                list1=self.splitRowList(dict1,splitNum,False)
                newRowList=newRowList+list1
                n=n+1

        #newRowList=rowListInfo
        rowCount=len(newRowList)
        n=0

        pd=False
        while n<rowCount:
            dictObj1=newRowList[n]
            if n+1<rowCount:
                dictObj2=newRowList[n+1]
                if dictObj2['cellType']=='value':
                    pd=True
                else:
                    pd=False
            else:
                pd=False
            strLen=0
            lenTitle=0
            lenValue=0
            cellList1=dictObj1['cellList']
            colNumList.append(len(cellList1))
            levelList.append(dictObj1['rowLevel'])
            if pd:
                cellList2=dictObj2['cellList']
                for m in range(0,len(cellList1)):
                    title=cellList1[m]
                    value=cellList2[m]
                    lenTitle=lenTitle+len(title)
                    lenValue=lenValue+len(value)

                    if len(title)>len(value):
                        strLen=strLen+len(title)
                    else:
                        strLen=strLen+len(value)
                #计算标题与值行取双方对应列字符窜最长值计算
                strLenList.append(strLen)
                #记录各自行中字符串总长度
                dictObj1['Len']=lenTitle
                dictObj2['Len']=lenValue
                newRowListInfo.append(dictObj1)
                newRowListInfo.append(dictObj2)
                n=n+2
            else:
                for m in range(0,len(cellList1)):
                    strLen=strLen+len(cellList1[m])
                strLenList.append(strLen)
                dictObj1['Len']=strLen
                newRowListInfo.append(dictObj1)
                n=n+1
        maxLen=max(strLenList)
        maxColNum=max(colNumList)
        maxLevel=max(levelList)

        return (maxLen,maxColNum,maxLevel,newRowListInfo)


    def changeData2(self,rowList,maxWidth,maxLevel):

        """
        反回生成下列类型的字典
        {colNum:Num   本行有几列
        rowLevel:Num  本行缩进几级
        colValue:[
            valueK,
            valueK1]   本行单元格中的值
         }
         valueK的结构如下：
         valueK:{
            leftNum:0
            right:0
            value:0
         }

        :return:
        """
        if isinstance(rowList,list):
            rowInfoList=[]
            strLenList=[]
            colNumList=[]
            lsList=[]
            returnDict={}
            rowCount=len(rowList)
            n=0
            pd=False
            topStr="-"*(maxWidth+maxLevel+maxLevel)
            topStr="++" +topStr[:len(topStr)-5]+"++"
            rowInfoList.append(topStr)
            while n<rowCount:
                dictObj1=rowList[n]
                if n+1<rowCount:
                    dictObj2=rowList[n+1]
                    if dictObj2['cellType']=='value':
                        pd=True
                    else:
                        pd=False
                else:
                    pd=False
                if pd:
                    lsList=self.setRowInfo2(dictObj1,dictObj2,maxWidth,maxLevel)
                    rowInfoList=rowInfoList+lsList
                    n=n+2
                else:
                    lsList=self.setRowInfo(dictObj1,maxWidth,maxLevel)
                    rowInfoList=rowInfoList+lsList
                    n=n+1
            return rowInfoList
        else:
            CustomInfo="Data type error, given data is not list"
            logs.logs(None,CustomInfo).getCustom_Log().error(CustomInfo)
            sys.exit(1)
        #return {"colNum":colNum,"rowLevel":rowLevel,"colValue":colValue}

    def setRowInfo(self,rowDict,maxWidth,maxLevel):
        """
        :param cellList: 行中单元格数据集合
        :param strLen: 单元格中数据总长度
        :param Level: 行级别
        :param maxWidth: 行最大宽度
        :param maxLevel: 最大行级别
        :return:
        """
        lsList=[]
        rowLevel=rowDict['rowLevel']
        cellList=rowDict['cellList']
        cellCount=len(cellList)
        #可以控制的剩余空白长度
        num1=maxWidth-rowDict['Len']
        #平均每个值两边的空白长度
        unit=num1/(cellCount*2)
        #平分之后多余的空白长度
        syNum=num1%(cellCount*2)
        rowStr=""
        fgxStr=""
        for cell in cellList:
            lefStr=" "* unit
            rigStr=" "* (unit-1)

            lefStrF="-"* unit
            rigStrF="-"* (unit-1)

            cellValue=self.checkValueType(cell)
            count=self.getCN_Count(cellValue)   #当前行为 字符串中有中文字符时，表格会变小
            if count>0:
                rigStr=" "*count + rigStr
                rigStrF="-" * count +rigStrF
            modStr="-" * len(cellValue)

            rowStr=rowStr+lefStr+cellValue+rigStr+"|"
            fgxStr=fgxStr+lefStrF+modStr+rigStrF+"+"
        if syNum!=0:
            lsStr=" " * (syNum-1) +"|"
            rowStr=rowStr[:len(rowStr)-1] +" "+lsStr
            fgxStr=fgxStr[:len(fgxStr)-1] +"-"+ lsStr
        lsList.append(self.createLR(rowStr,rowLevel,maxLevel,False))
        lsList.append(self.createLR(fgxStr,rowLevel,maxLevel,True))
        return lsList

    #专门计算标题和值行
    def setRowInfo2(self,rowTitleDict,rowValueDict,maxWidth,maxLevel):
        """
        :param cellList: 行中单元格数据集合
        :param strLen: 单元格中数据总长度
        :param Level: 行级别
        :param maxWidth: 行最大宽度
        :param maxLevel: 最大行级别
        :return:
        """
        lsList=[]
        rowLevel=rowTitleDict['rowLevel']
        cellList=rowTitleDict['cellList']
        cellCount=len(cellList)

        cellList1=rowTitleDict['cellList']
        cellList2=rowValueDict['cellList']
        lsCellList=[]
        n=0
        strLen=0
        for n in range(0,cellCount):
            strCell1=self.checkValueType(cellList1[n])
            strCell2=self.checkValueType(cellList2[n])
            if len(strCell1)>len(strCell2):
                strLen=strLen+len(strCell1)
                lsCellList.append(strCell1)
            else:
                strLen=strLen+len(strCell2)
                lsCellList.append(strCell2)

        #可以控制的剩余空白长度
        num1=maxWidth-strLen
        #平均每个值两边的空白长度
        unit=num1/(cellCount*2)
        #平分之后多余的空白长度
        syNum=num1%(cellCount*2)
        lenList=[]
        for o in lsCellList:
            lenList.append(len(o)+unit+unit)
        rowStr=""
        fgxStr=""
        rowTitleInfo=""
        rowValueInfo=""
        for n in range(0,cellCount):
            strCell1=self.checkValueType(cellList1[n])
            strCell2=self.checkValueType(cellList2[n])
            cellStr=self.setUnitCell(strCell1,lenList[n])
            rowTitleInfo=rowTitleInfo + self.setUnitCell(strCell1,lenList[n])
            rowValueInfo=rowValueInfo + self.setUnitCell(strCell2,lenList[n])
            lsStr="-" * (len(cellStr)-1) +"+"
            fgxStr=fgxStr+lsStr
        if syNum!=0:
            syStr1=" " *(syNum-1) +"|"
            syStr2="-" *(syNum-1) +"+"
            rowTitleInfo=rowTitleInfo[:len(rowTitleInfo)-1] +" "+syStr1
            rowValueInfo=rowValueInfo[:len(rowValueInfo)-1] +" "+syStr1
            fgxStr=fgxStr[:len(fgxStr)-1] +"-"+syStr2
        lsList.append(self.createLR(rowTitleInfo,rowLevel,maxLevel,False))
        lsList.append(self.createLR(fgxStr,rowLevel,maxLevel,True))
        lsList.append(self.createLR(rowValueInfo,rowLevel,maxLevel,False))
        lsList.append(self.createLR(fgxStr,rowLevel,maxLevel,True))
        return lsList

    def setUnitCell(self,cellValue,unitWidth):
        cellValue=self.checkValueType(cellValue)
        count=self.getCN_Count(cellValue)   #当前行为 字符串中有中文字符时，表格会变小
        if count>0:
            unitWidth=unitWidth+count
        num1=unitWidth-len(cellValue)
        num2=num1/2
        syNum=num1%2
        leftStr=" " * num2
        if syNum==0:
            rightStr=" " * (num2-1) +"|"
        else:
            lsStr=" " * (syNum-1) + "|"
            rightStr=" " * num2 +lsStr
        strValue=leftStr + cellValue + rightStr
        return strValue

    def createLR(self,rowStr,rowLevel,maxLevel,isFGX=False):
        if isFGX:
            #如果是分割线
            str1="-" *(maxLevel-rowLevel)
            leftStr="+" * (rowLevel-1) +str1
            leftStr="|" + leftStr

            str2="-" *(maxLevel-rowLevel)
            rightStr="+" *(rowLevel-1) +"|"
            rightStr=str2+rightStr
        else:
            str1=" " *(maxLevel-rowLevel)
            leftStr="|" * (rowLevel-1) +str1
            leftStr="|" + leftStr

            str2=" " *(maxLevel-rowLevel)
            rightStr="|" *(rowLevel-1) +"|"
            rightStr=str2+rightStr
        return  leftStr+rowStr[:len(rowStr)-1]+rightStr

    def getTableData(self,ColWidth):
        try:
            listKK=self.clNewData(self.varJson,2,None)
            if ColWidth==None:
                ColWidth=4
            else:
                ColWidth=int(ColWidth)
            (maxLen,maxColNum,maxLevel,RowListInfo)=self.fgRow(listKK,ColWidth)
            #此处流出多余空间
            maxLen=maxLen+maxColNum+20
            rowListInfo=self.changeData(RowListInfo)
            rowList=self.printTableData(rowListInfo)
            rowListCN=self.printTableDataCN(rowListInfo)
            if platform.system()=="Windows":
                for o in rowList:
                    print o.decode("utf-8").encode("gbk")
            else:
                for o in rowList:
                    print o.decode("utf-8")

            #如果当前用户设置了 outputfile 路径值，则表示同时将信息保存到该地址
            if self.fileName!=None and self.fileName!="":
                file1=file(self.fileName,'w')
                if platform.system()=="Windows" or platform.system()=="Linux":
                    file1.writelines(rowList)
                else:
                    file1.writelines(rowListCN)
                file1.close()
        except IOError:
            info = traceback.format_exc()
            CustomInfo="No permission to write to the file"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

