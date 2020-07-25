#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-28 16:28:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys

import json
# import timetool
import shutil
import random

from PIL import Image

if sys.version_info > (3,0):
    def cmp(a,b):
        import operator
        return operator.eq(a,b)


#获取脚本路径
def cur_file_dir():
    pathx = sys.argv[0]
    tmppath,_file = os.path.split(pathx)
    if cmp(tmppath,'') == 0:
        tmppath = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(tmppath):
        return tmppath
    elif os.path.isfile(tmppath):
        return os.path.dirname(tmppath)
    
#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#for python3
def cmp(a,b):
    return ((a>b)-(a<b))

#获取目录下的所有类型文件
def getAllExtFile(pth,fromatx = ".erl"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
            elif fromatx == ".*" :
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist


#获取一个目录下的所有子目录路径
def getAllDirs(spth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    for d in files:
        if d[1] != '/' and (not d[1] in makedirstmp): #创建未创建的目录层级
            tmpdir = d[1][1:]
            tmpleves = tmpdir.split('/')
            alldirs = getAllLevelDirs(tmpleves)
            for dtmp in alldirs:
                if not dtmp in makedirstmp:
                    makedirstmp.append(dtmp)
    return makedirstmp
#获取目录下的所有文件路径
def getAllFiles(spth,fromatx = '.*'):
    files = getAllExtFile(spth,fromatx)
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    for d in files:
        makedirstmp.append(d[0])
    return makedirstmp


def isFile(filename):
    try:
        with open(filename) as f:
            return True
    except IOError:
        return False

def finddir(arg,dirname,filenames):
    name,text = os.path.split(dirname)
    dirnametmp = str(dirname)
    if text and text[0] == '.':
        print(dirname)
        print(filenames)
        os.system('rm -r %s'%(dirname))
        return
    elif filenames:
        for f in filenames:
            if f[0] == '.' and isFile(dirname + f):
                fpthtmp = dirname + f
                if f.find(' '):
                    nf = f.replace(' ','\ ')
                    fpthtmp = dirname + nf
                print(dirname + f)
                os.system('rm  %s'%(fpthtmp))

#删除所有pth目录下的所有"."开头的文件名和目录名
def removeProjectAllHideDir(pth):
    alldirs = getAllDirs(pth)
    if not ('/' in alldirs):
        alldirs.append('/')
    for d in alldirs:
        tmpth = pth + d
        os.path.walk(tmpth, finddir, 0)


#获取一个路径中所包含的所有目录及子目录
def getAllLevelDirs(dirpths):
    dirleves = []
    dirtmp = ''
    for d in dirpths:
        dirtmp += '/' + d
        dirleves.append(dirtmp)
    return dirleves

#在outpth目录下创建ndir路径中的所有目录，是否使用决对路径
def makeDir(outpth,ndir):
    tmpdir = ''
    if ndir[0] == '/':
        tmpdir = outpth + ndir
    else:
        tmpdir = outpth + '/' + ndir
    print(tmpdir)
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)

# 创建一个目录下的所有子目录到另一个目录
def createDirs(spth,tpth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    tmpfpth = fpth
    for d in files:
        if d[1] != '/' and (not d[1] in makedirstmp): #创建未创建的目录层级
            tmpdir = d[1][1:]
            tmpleves = tmpdir.split('/')
            alldirs = getAllLevelDirs(tmpleves)
            for dtmp in alldirs:
                if not dtmp in makedirstmp:
                    makeDir(tpth,dtmp)
                    makedirstmp.append(dtmp)

# 替换文件名
def replaceFileName(path,sname,replaceStr,tostr):
    a = sname
    tmpname = a.replace(replaceStr, tostr)
    outpath = path + tmpname
    oldpath = path + sname
    cmd = "mv %s %s"%(oldpath,outpath)
    print(cmd)
    os.system("mv %s %s"%(oldpath,outpath))

# 替换目录下的文件名中某个字符串为其他字符串
def renameDir(sdir,replacestr,tostr,exittype):
    files = getAllExtFile(sdir,fromatx = exittype)
    allfilepath = []
    for f in files:
        tmppath = sdir + f[1]
        filename = f[2] + exittype
        allfilepath.append([tmppath,filename])
    for p in allfilepath:
        replaceFileName(p[0], p[1], replacestr, tostr)


def getFileNameFromPath(fpth):
    tmp = fpth.split('/')[-1]
    fname = tmp.split('.')[0]
    return fname

labelpath = 'txt'
imagepath = 'images'
xmlpath = 'annotations'

trainNum = 0.8
valNum = 0.2

trainpth = 'train.txt'
valpth = 'val.txt'

def createDataFile(indir,imgfmart = '.png',typefmart = '.xml'):
    imgstmp = getAllFiles(indir,imgfmart)
    xmlstmp = getAllFiles(indir,typefmart)
    return imgstmp,xmlstmp

def copyfile(spth,tpth):
    f = open(spth,'rb')
    dat = f.read()
    f.close()
    f = open(tpth,'wb')
    f.write(dat)
    f.close()

def deleOldfile(imgpth,xmlpth):
    if os.path.exists(imagepath):
        shutil.rmtree(imagepath)
    os.mkdir(imagepath)
    if os.path.exists(xmlpath):
        shutil.rmtree(xmlpath)
    os.mkdir(xmlpath)

def randomList(plist):
    dats = list(range(len(plist)))
    dtmp = 0
    outnames = []
    while len(dats) > 0:
        dtmp = random.randint(0,len(dats)-1)
        print(dtmp,len(dats))
        outnames.append(dats[dtmp])
        dats.pop(dtmp)
        
    outlist = []

    for i,v in enumerate(outnames):
        outlist.append(plist[v])
    return outlist

def getFileNames(fs):
    outnames = []
    for i,v in enumerate(fs):
        tmp = getFileNameFromPath(v)
        outnames.append(tmp)
    return outnames

def createTrainAndValFile(odir,names):
    tcount = int(len(names)*trainNum)
    vcount = len(names) - tcount
    trainstr = ''
    valstr = ''
    for i,v in enumerate(names):
        if i < tcount:
            trainstr += v + '\n'
        else:
            valstr += v + '\n'
    trainstr = trainstr[:-1]
    valstr = valstr[:-1]
    f = open(odir + os.sep + 'train.txt','w')
    f.write(trainstr)
    f.close()

    f = open(odir + os.sep + 'val.txt','w')
    f.write(valstr)
    f.close()

def conventPNG2JPEG(spth,tpth):
    im = Image.open(spth)
    rgb_im=im.convert('RGB')
    rgb_im.save(tpth)

import xml2txt
def conventXML2TXT(spth,tpth,classes,isHeaveClas):
    xml2txt.convert_annotation(spth, tpth,classes,isHeaveClas)
def conventTXT2XML(spth,tpth):
    pass

clsname = 'classes.txt'

def getClassesWithFIle(fpth):
    f = open(fpth,'r')
    lines = f.readlines()
    f.close()
    outclses = []
    for i,v in enumerate(lines):
        tmpv = v.replace('\n','').replace('\r','')
        outclses.append(tmpv)
    return tmpv

def saveClassesToFile(fpth,plist):
    outstr = ''
    for i,v in enumerate(plist):
        outstr += v + '\n'
    f = open(fpth,'w')
    f.write(outstr)
    f.close()

def createData(indir,outdir,imgfmart,labfmart):
    classes = []
    idir = indir
    odir = outdir
    if not idir:
        idir = os.getcwd()
    if not odir:
        odir = idir + os.sep + 'out'
    vocimgpth = odir + os.sep + imagepath
    vocxmlpth = odir + os.sep + xmlpath
    txtpth = odir + os.sep + labelpath
    if os.path.exists(odir):
        shutil.rmtree(odir)
    os.mkdir(odir)
    os.mkdir(vocimgpth)
    os.mkdir(vocxmlpth)
    os.mkdir(txtpth)
    clspth = idir + os.sep + clsname
    oclspth = odir + os.sep + clsname
    isHeaveClas = False
    if os.path.exists(clspth):
        classes = getClassesWithFIle(clspth)
        shutil.copyfile(clspth, oclspth)
        isHeaveClas = True
    else:
        print('the classes is empty,and will create it to outdir:\n%s'%(oclspth))
    imgs,xmls=createDataFile(indir,imgfmart,labfmart)
    for i,v in enumerate(imgs):
        print(v)
        spth = indir + v
        tmps = v.split('.')
        jpegpth = ''
        if not os.path.exists(spth):
            print('imagefile not exists:%s'%(spth))
            return False
        if len(tmps) == 2:
            jpegpth = tmps[0]+'.jpg'
            tpth = vocimgpth + jpegpth
            conventPNG2JPEG(spth,tpth)
        else:
            print('file path erro')
            print(v)
            return False
    print(len(imgs))
    for i,v in enumerate(xmls):
        print(v)
        spth = indir + v
        tpth = vocxmlpth + v
        tmps = v.split('.')
        tmptxtpth = txtpth + tmps[0] + '.txt'
        copyfile(spth,tpth)
        cs = conventXML2TXT(spth, tmptxtpth,classes,isHeaveClas)
        print(cs)
    print(len(xmls))
    rimgs = randomList(imgs)
    print(rimgs)
    print(len(rimgs))
    names = getFileNames(rimgs)
    print(names)
    print(clspth)
    if not isHeaveClas:
        print(oclspth)
        saveClassesToFile(oclspth, classes)
    createTrainAndValFile(odir,names)
    
    return True
def main(args):
    indir = None
    outdir = None
    imgfmart = '.png'
    labfmart = '.xml'
    if len(args) == 2:
        indir = args[1]
        outdir = args[1] + os.sep +'out'
    elif len(args) == 3:
        indir = args[1]
        outdir = args[2]
    elif len(args) == 4:
        indir = args[1]
        outdir = args[2]
        imgfmart = '.' + args[3]
    elif len(args) == 5:
        indir = args[1]
        outdir = args[2]
        imgfmart = '.' + args[3]
        labfmart = '.' + args[4]
    else:
        print('use pwd dir')
    # main(indir,outdir,imgfmart,labfmart)
    isOK = createData(indir,outdir,imgfmart,labfmart)
    print(isOK)

# def test():
#     pass
def test():
    ls = list(range(10))
    print(ls)
    print(type(ls))
    print(list(ls))
    print(ls.pop())
#程序对labelImg标注的数据文件夹下的内容进行处理,生成out目录
#在out目录下生成一个xml和txt,以及一个jpg的文件夹,
#xml下放置所有voc的标注数据,txt下放所有yolo标注的数据,jpg下入所有图片的jpg图片
#如果原始的labelImg标注的是yolo数据,程序会自动把yolo同样转成一份xml数据放在xml目录下
#如果原始的labelImg标注的是voc数据,程序会自动把voc的xml数据转成一份txt的数据放在txt目录下
#如果原始图片是png格式,程序会把png格式数据自动转成jpg格式保存到jpg下,
#在voc目录下会生成用于tensorflow使用的数据集
if __name__ == '__main__':
    # test()
    main(sys.argv)
    
