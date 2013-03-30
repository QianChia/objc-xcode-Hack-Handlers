#! /usr/local/bin/python3
# -*- coding:utf-8 -*-

#Created by:yanghua_kobe
#Date:2013-03-29
#Function:
'''
    when you use Xcode's build-in "source control" function to 
    manage your project ,such as, [svn].You rename files or delete
    files through Xcode,it will gets a missing file warning 
    even though you have committed or check out. 
    The warning will never disappear, 
    it always tips you missing the file.
    (It is considerd as a bug of Xcode since version 4.3 ).

    More details:
    [http://blog.csdn.net/theonezh/article/details/7692804]

    the handler is useful for you to handle this problem.
    it run the 'svn status' cmd and find all warning files,
    then use 'svn rm xxx' to remove those files from svn control.
'''

import os, sys, re, fnmatch, os.path, subprocess


#TODO: change the path to your xcode project path
GLOBAL_PROJECT_PATH     = '/Users/yanghua/Desktop/weiboDemo'

#TODO: change the path to the dir where you stone the log file
GLOBAL_LOGFILE_PATH     = '/Users/yanghua/Desktop/tmp.txt'

#TODO: the flag identify if you want to keep the logfile
#default is True ,if False the logfile will be delete after running
GLOBAL_KEEP_LOGFILE     = True

#remark:
#the regex pattern used to match:
#^\?    :start with character "?" (the '?' means collision in svn)
#(?!.*?\.xcodeproj)     : is a part group, splited:
#       ?!              : means 'not is'
#       .*?             : any character
#       \.xcodeproj     : string '.xcodeproj'
#-------------------------------------------
#all of these make a pattern:
#match : start with '?' and not contain with '.xcodeproj' 
#-------------------------------------------
GLOBAL_COLLISION_IDENTIFIER_PATTERN = '^\?(?!.*?\.xcodeproj)'

#file mode option
MODE_WRITE                  = "w"
MODE_APPEND                 = "a"
MODE_READ                   = "r"

def HandleWarningFiles():
    '''
        desc        : main-handler 
    '''
    warningFileList=findAllWarningFiles()
    deleteAllWarningFiles(warningFileList)
    afterWarningHandled()

def deleteAllWarningFiles(warningFileList):
    '''
        desc        : delete all warning files
        args        : list of warning files
        return      : None
    '''
    if warningFileList is None or len(warningFileList)==0:
        return False

    for filePath in warningFileList:
        cmdStr='svn rm {0}'.format(filePath)
        with open(GLOBAL_LOGFILE_PATH, encoding='utf-8', mode=MODE_APPEND) \
        as tmp_logfile:
            tmp_logfile.write(cmdStr)
            process=subprocess.Popen(cmdStr, shell=True, \
                universal_newlines=True, stdout=tmp_logfile)
            process.wait()

def findAllWarningFiles():
    '''
        desc        : find all collision files
        args        : None
        return      : warning file list
    '''
    global GLOBAL_PROJECT_PATH,GLOBAL_COLLISION_IDENTIFIER_PATTERN
    cmdStr = 'svn status {0}'.format(GLOBAL_PROJECT_PATH)
    with open(GLOBAL_LOGFILE_PATH, encoding='utf-8', mode=MODE_WRITE) \
    as tmp_logfile:
        process=subprocess.Popen(cmdStr, shell=True, \
            universal_newlines=True, stdout=tmp_logfile)
        process.wait()
        tmp_logfile.write('\n\n\n')

    #reopen
    warningFileList=[]
    with open(GLOBAL_LOGFILE_PATH, encoding='utf-8', mode=MODE_READ) \
    as tmp_logfile:
        [warningFileList.append(line) for line in tmp_logfile \
        if re.match(GLOBAL_COLLISION_IDENTIFIER_PATTERN,line)]
        
    #handle file name (left trim backspace and '?' and right trim '\n')
    result=[fileName[1:].lstrip()[0:-1] for fileName in warningFileList]
    print(result)

    return result

def afterWarningHandled():
    '''
        desc        : delete the log file
        args        : None
        return      : None
    '''
    global GLOBAL_KEEP_LOGFILE,GLOBAL_LOGFILE_PATH
    if not GLOBAL_KEEP_LOGFILE:
        os.remove(GLOBAL_LOGFILE_PATH)
    else:
        print('log file path:{0}'.format(GLOBAL_LOGFILE_PATH))


if __name__ == '__main__':
    HandleWarningFiles()
