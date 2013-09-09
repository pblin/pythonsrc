#!/usr/bin/env python

import zipfile
import os


def unzip(zipFilePath, destDir):
    zfile = zipfile.ZipFile(zipFilePath)
    for name in zfile.namelist():
        (dirName, fileName) = os.path.split(name)
        if fileName == '':
            # directory
            newDir = destDir + '/' + dirName
            if not os.path.exists(newDir):
                os.mkdir(newDir)
        else:
            # file
            fd = open(destDir + '/' + name, 'wb')
            fd.write(zfile.read(name))
            fd.close()
    zfile.close()

zipdir = '/home/bernard/storia_dictionary/'
for filename in os.listdir(zipdir):
    if '.zip' in filename:
        unzip (zipdir+filename, '/home/bernard/storia_dictionary')

