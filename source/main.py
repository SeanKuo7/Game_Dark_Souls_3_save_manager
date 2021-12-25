import pathlib
print("Working directory: ", pathlib.Path().resolve())


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
    print(dirList)
except:
    print("reading config.ini failed!!")

