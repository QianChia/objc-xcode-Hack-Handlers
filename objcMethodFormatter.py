#! /usr/local/bin/python3
# -*- coding:utf-8 -*-

#Created by:yanghua_kobe
#Date:2013-03-13
#Function:
'''
    change the method format:

    -(CGFloat) getHeightWithText:(NSString*)text fontSize:(CGFloat)fontSize constraint:(CGSize)cSize minHeight:(CGFloat)mHeight;

    to:

    -(CGFloat) getHeightWithText:(NSString*)text
                        fontSize:(CGFloat)fontSize
                      constraint:(CGSize)cSize
                       minHeight:(CGFloat)mHeight;
'''

import os, sys, re, fnmatch, os.path

#TODO: change the path to your xcode project path
GLOBAL_PROJECT_PATH     = '/Users/yanghua/Desktop/testOBJCFormatter/FastEasyBlog'


#match method pattern
#\s                 :space
#\s*                :0 or n space
#([\d\w]*)          :0 or n number or char such as (void) / ( CGFloat)
#(([\d\w]*)\s*\**\s*):  such as: (NSString* ) / ( UITableViewController *)
#\(                 :match left '('
#\)                 :match right ')'
GLOBAL_METHOD_PATTERN   = '^\s*(-|\+)\s*\(\s*(([\d\w]*)\s*\**\s*)\s*\)\s*'

#match notation and postil
GLOBAL_UNUSED_PATTERN   = '^\s*(//|//*)\s*'

#match arg delimiter
GLOBAL_ARG_DELIMITER_PARTTEN = '[a-zA-Z0-9_]\s+[a-zA-Z0-9_]'

GLOBAL_FILEPATH_LIST    = []

#want to match 
GLOBAL_INCLUDE = ['*.h', '*.m']
#want to exclude               
GLOBAL_EXCLUDE = ['*Global.h','*Global.m'] 

GLOBAL_INCLUDE = r'|'.join([fnmatch.translate(x) for x in GLOBAL_INCLUDE])
GLOBAL_EXCLUDE = r'|'.join([fnmatch.translate(x) for x in GLOBAL_EXCLUDE]) or r'$.'



def methodTypesettingHandle(projectPath):
    '''
        desc    : typesetting method name
        args    : projectPath - the path of the project
        return  : None
    '''
    global GLOBAL_FILEPATH_LIST
    collectFilePathInProject(projectPath)
    [handler(item) for item in GLOBAL_FILEPATH_LIST]
    # print(GLOBAL_FILEPATH_LIST)


def collectFilePathInProject(filePath):
    '''
        desc    : get all files of the project
        args    : filePath - the file's full path
        return  : collected all file path in project
    '''
    for root, dirs, files in os.walk(filePath):
        files = [os.path.join(root, f) for f in files]
        files = [f for f in files if not re.match(GLOBAL_EXCLUDE, f)]
        files = [f for f in files if re.match(GLOBAL_INCLUDE, f)]

        GLOBAL_FILEPATH_LIST.extend(files)


def handler(filePath):
    '''
        desc    : single file handle 
        args    : filePath - the objc file
        return  : None
    '''
    print('handling file > %s' % filePath)
    fileLines=[]
    if filePath is not None and len(filePath)!=0:
        #read and handle
        with open(filePath, encoding='utf-8', mode='r') as handlingFile:
            for singleLine in handlingFile:
                #the line is a method name and not be noted
                if re.search(GLOBAL_UNUSED_PATTERN,singleLine) is None and re.search(GLOBAL_METHOD_PATTERN,singleLine) is not None:
                    formattedMethod=methodFormatter(singleLine)
                    if formattedMethod is not None:
                        fileLines.extend(formattedMethod)
                    else:
                        fileLines.append(singleLine)
                else:
                    fileLines.append(singleLine)
                

        #write
        with open(filePath, encoding='utf-8', mode='w') as writingFile:
            for singleLine in fileLines:
                writingFile.write(singleLine)


def methodFormatter(matchedMethodLine):
    '''
        desc    : format the matched method line
        args    : matchedMethodLine - the method line str matched
        return  : List
    '''
    result=[]
    pattern=re.compile(GLOBAL_ARG_DELIMITER_PARTTEN)
    splitedList=pattern.split(matchedMethodLine)
    methodPartList=handleSplitedMethodPart(splitedList,matchedMethodLine)
    if methodPartList is None or len(methodPartList)<2:
        result=None
    else:
        result=methodPartFormatter(methodPartList)

    return result

def handleSplitedMethodPart(splitedList,matchedMethodLine):
    '''
        desc    : because of the reg_partten, the item of the splitedList
                  missed some character
        args    : splitedList - splited list based on the regex pattern
                  matchedMethodLine - source method str
        return  : handled method part list
    '''
    if splitedList is None or len(splitedList)==0:
        return splitedList

    result=[]
    for splitedItem in splitedList:
        findedStartIndex=matchedMethodLine.find(splitedItem)
        if findedStartIndex==-1:
            continue
        c_startIndex=findedStartIndex-1
        c_endIndex=findedStartIndex+len(splitedItem)

        #judge first character from source str
        if c_startIndex>=0:
            c_startStr=matchedMethodLine[c_startIndex:c_startIndex+1]
            if c_startStr!=' ':
                splitedItem='{0}{1}'.format(c_startStr,splitedItem)

        #judge last character from source str
        if c_endIndex<=len(matchedMethodLine)-1:
            c_endStr=matchedMethodLine[c_endIndex:c_endIndex+1]
            if c_endStr!=' ':
                splitedItem='{0}{1}'.format(splitedItem,c_endStr)

        result.append(splitedItem)

    return result
            

def methodPartFormatter(methodPartList):
    '''
        desc    : typesetting all method parts use "backspace"
        args    : methodPartList - the list of methodPart 
        return  : formatted methodPart list
    '''
    if methodPartList is None or len(methodPartList)<2:
        return None

    if methodPartList[0].find(':')==-1:
        return None

    colonCharIndex=methodPartList[0].index(':')
    for x in range(1,len(methodPartList)):
        tmpSplitedMethodPart=methodPartList[x].split(':')
        if tmpSplitedMethodPart is not None and len(tmpSplitedMethodPart)==2:
            partOneCharCount=len(tmpSplitedMethodPart[0])
            #the first colon's index that link with method name larger than 
            #the second arg's colon
            fillingSpaceNum=colonCharIndex-partOneCharCount
            if fillingSpaceNum>0:
                methodPartList[x]=argPartGenerator(fillingSpaceNum,methodPartList[x])
            else:
                return None
        else:
            return None

    return methodPartList


def argPartGenerator(fillingSpaceNum,argPart):
    '''
        desc    : generate space for the argPart 
        args    : fillingSpaceNum - filling space num 
                  argPart - the formating source code
        return  : formatted argParts
    '''
    tmpStr=''
    for x in range(fillingSpaceNum):
        tmpStr+=' '
    result='\n{0}{1}'.format(tmpStr,argPart)

    return result

if __name__ == '__main__':
    if GLOBAL_PROJECT_PATH is None or not os.path.exists(GLOBAL_PROJECT_PATH):
        print('the project path is not available! please check it again!')
        exit(0)
    os.chdir(GLOBAL_PROJECT_PATH)
    methodTypesettingHandle(GLOBAL_PROJECT_PATH)