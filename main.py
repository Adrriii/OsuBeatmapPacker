import glob, os
from glob import glob
from os.path import basename
import zipfile

errors = []

src = ""
while(not os.path.isdir(src)):
    src = input("Source Folder : ")

dst = ""
while(not os.path.isdir(dst)):
    dst = input("Destination Folder : ")

mode = "any"
while(not mode.isdigit() and mode != ""):
    mode = input("Mode (nothing if ignored) : ")

keys = 0
if(mode == ""):
    mode = -1
else:
    mode = int(mode)
    if (3 == mode):
        keys = "any"
        while(not keys.isdigit() and keys != ""):
            keys = input("Keys (nothing if ignored) : ")
        if(keys == ""):
            keys = 0

def addAll(set,list):
    for element in list:
        set.add(element)

def getInfo(lines, keyword):
    for line in lines:
        if(line.startswith(keyword+":")):
            return line.split(":")[1]

def getMode(lines):
    try:
        return int(getInfo(lines,"Mode"))
    except:
        return -1

def getCS(lines):
    try:
        return int(getInfo(lines,"CircleSize"))
    except:
        return -1

def getAudio(lines):
    return getInfo(lines,"AudioFilename")

def getDesignAssets(lines):
    assetsMode = False
    assets = []
    for line in lines:
        if(line.startswith("//Break Periods")):
            assetsMode = False
        if assetsMode:
            assets.append(line.split("\"")[1])
        if(line.startswith("//Background and Video events")):
            assetsMode = True
    return assets

def packAssets(dest,assets,baseDir):
    zipf = zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED)
    for file in assets:
        os.chdir(baseDir)
        if(os.path.isfile(file.rstrip().strip())):
            zipf.write(file.rstrip().strip())
    zipf.close()
    
def packMap(dest,folder,mode=-1,keys=0):
    os.chdir(folder)
    assets = set()
    for file in glob("*.osu"):
        try:
            f = open(folder+file,'r', encoding="utf-8")
            lines = f.readlines()
            f.close()
            if(-1 == mode or getMode(lines) == mode):
                checks = True
                if(3 == mode and 0 != keys and keys!= getCS(lines)):
                    checks = False
                
                if checks:
                    assets.add(getAudio(lines))
                    assets.add(file)
                    addAll(assets,getDesignAssets(lines))
                    packAssets(dest,assets,folder)
        except Exception as e:
            errors.append("Error while reading \""+folder+file+"\" ("+str(e)+")")

folders = glob(src+"/*/")
total = len(folders)
i = 0
for dir in folders:
    i+=1
    print(str(i)+"/"+str(total))
    packMap(os.path.join(dst,basename(dir[:-1])+".osz"),dir,3,4)

if(len(errors) > 0):
    c = input("Scan ended with "+str(len(errors))+" errors, display them ? (y/n)")
    if(c == "y" or c == "Y"):
        for error in errors:
            print(error)