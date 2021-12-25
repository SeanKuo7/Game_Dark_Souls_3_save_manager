import pathlib
from datetime import datetime
from zipfile import ZipFile
import os
import os.path

print("Working directory: ", pathlib.Path().resolve())

def readPathesFromConfig():
    inputPath = ""
    outputPath = ""
    try:
        print("entered")
        f = open("config.ini", "r")
        #print(f.read())
        dirListRaw = f.readlines()
        #print(dirList)
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
    print(inputPath)
    print(outputPath)
    now = datetime.now()
    currentTimeStr = now.strftime("_%Y.%m.%d_%H%M%S")
    #print("Current Time =", currentTimeStr)
    outputBackupFilePath = outputPath+"\\DarkSoulsIII"+currentTimeStr+".zip"
    inputPath = "D:\Desktop\eggsdir"
    print(outputBackupFilePath)
    with ZipFile(outputBackupFilePath, 'w') as backupZip:
        #backupZip.write()
        for folderName, subfolders, filenames in os.walk(inputPath):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                print(filePath)
                # Add file to zip
                parrentDirname = folderName.split("\\")[-1]
                basename = os.path.basename(filePath)
                
                print(parrentDirname, basename)
                backupZip.write(filePath, parrentDirname+"\\"+basename)
    return



if __name__ == "__main__":
    dirList = readPathesFromConfig()
    backupSave(dirList[0], dirList[1])


