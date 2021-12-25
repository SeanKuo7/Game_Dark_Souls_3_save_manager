import pathlib
from datetime import datetime
from zipfile import ZipFile
import os
import os.path
import time
import hashlib
import sys
import traceback

print("Working directory: ", pathlib.Path().resolve())

def readPathesFromConfig():
    inputPath = ""
    outputPath = ""
    try:
        with open("config.ini", "r") as f: 
            #print(f.read())
            dirListRaw = f.readlines()
            dirList = []
            for dir in dirListRaw[:-1]:
                dirTrimmed = dir[0:len(dir)-1]
                dirList.append(dirTrimmed)
            dirList.append(dirListRaw[-1])
        return(dirList)
    except:
        print("reading config.ini failed!!")
    return

def backupSave(inputPath, outputPath):
    # print(inputPath)
    # print(outputPath)
    now = datetime.now()
    currentTimeStr = now.strftime("_%Y.%m.%d_%H%M%S")
    #print("Current Time =", currentTimeStr)
    outputBackupFilePath = outputPath+"\\DarkSoulsIII"+currentTimeStr+".zip"
    # inputPath = "D:\Desktop\eggsdir"
    print(outputBackupFilePath)
    with ZipFile(outputBackupFilePath, 'w') as backupZip:
        #backupZip.write()
        for folderName, subfolders, filenames in os.walk(inputPath):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                print(folderName, subfolders, filePath)
                if not subfolders:
                    parrentDirname = folderName.split("\\")[-2] + "\\" +  folderName.split("\\")[-1]
                else:
                    parrentDirname = folderName.split("\\")[-1]
                # Add file to zip
                basename = os.path.basename(filePath)
                dirInZipFile = parrentDirname+"\\"+basename
                # print(parrentDirname, basename)
                backupZip.write(filePath, dirInZipFile)
    return

def getCheckSums(path):
    hashFunction = hashlib.md5()
    returnList = []
    for folderName, subfolders, filenames in os.walk(path):
        for filename in filenames:
            filePath = os.path.join(folderName, filename)
            # lastModifiedTime = os.path.getmtime(filePath)
            with open(filePath, "rb") as file_to_check:
                # read contents of the file
                # data = file_to_check.read()
                # pipe contents of the file through
                for chunk in iter(lambda: file_to_check.read(4096), b""):
                    hashFunction.update(chunk)
                md5_returned = hashFunction.hexdigest()
            returnList.append(md5_returned)
    return returnList

def fileMonitor(path2Watch, outputPath):
    before = getCheckSums(path2Watch)
    while 1:
        time.sleep (5)
        after = getCheckSums(path2Watch)
        print(before,after)
        if before != after:
            print("modified!!!")
            now = datetime.now()
            currentTimeStr = now.strftime("_%Y.%m.%d_%H%M%S")
            # print(currentTimeStr)
            before = after
            backupSave(path2Watch, outputPath)
    return

def showExceptionNWait(exc_type, exc_value, tb):
    try:
        traceback.print_exception(exc_type, exc_value, tb)
        input("Press any key to exit.")
        sys.exit(-1)
    except:
        sys.exit(-1)

def main():
    dirList = readPathesFromConfig()
    if not dirList:
        errorMsg = f'config.ini pathes error, got {dirList}'
        print(errorMsg)
        raise Exception(errorMsg)
    
    if len (dirList)<3:
        errorMsg = f'config.ini pathes error, got {dirList}'
        print(errorMsg)
        raise Exception(errorMsg)
    fileMonitor(dirList[0], dirList[1])
    return

sys.excepthook = showExceptionNWait
if __name__ == "__main__":
    
    main()


