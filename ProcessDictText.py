#!/usr/bin/env python
from elementtree import ElementTree as ET
import base64
import chardet
import os

wwwDir = '/home/bernard/storia_dictionary/forwww/'
dictDir = '/home/bernard/storia_dictionary/'


def getWords (txt):
    words = str(txt).split('\t')
    del words[0]
    return words

def processWordDef (lineIn):
    
    allwords = getWords (lineIn)
    encoding = chardet.detect(allwords[3])['encoding']
    root = ET.fromstring (allwords[3].decode(encoding, 'replace').encode('utf-8'))

    #add audio reference         
    bodyElem = root.find("body")
    
    pron_word = str('/dictionary/Pronunciation/' + 'pron_' + allwords[1] + '.mp3').encode('utf-8')
    print pron_word      
    audioElem=ET.Element ('audio', id = 'dicAudio')
    audioElem.set('src', pron_word)
    audioElem.set('autoplay', 'true')
    bodyElem.append(audioElem)
    scriptElem=ET.Element('script')
    
    if allwords[2] == "YD":
        bodyElem.set("onclick", "playsound()")
        soundscript = "function playsound(){document.getElementById('dicAudio').play();document.getElementById('readThru').play();}"
        scriptElem.text = soundscript
        #add readThrough
        readthru_file = str('/dictionary/ReadthroughAudio/' + 'fd_' + allwords[0] + '.mp3').encode('utf-8')
        print readthru_file      
        readThru_audioElem=ET.Element ('audio', id = 'readThru')
        readThru_audioElem.set('src', readthru_file)
        readThru_audioElem.set('controls', 'true')
        readThru_audioElem.set('autoplay', 'true')
        bodyElem.append(readThru_audioElem)
    else:
        addon_script = "document.querySelectorAll('img.pron-icon')[0].setAttribute ('onclick', 'playsound()');function playsound(){document.getElementById('dicAudio').play();}"
        scriptElem.text = addon_script
    
    bodyElem.append(scriptElem)
    
    #process images
    for imgElement in root.findall ('.//img'):
            imgSrc = imgElement.get('src')
            imgFile = dictDir + 'Images/' + imgSrc
            if (os.path.exists(imgFile)):
                newImgSrc = "data:image/jpg;base64," + base64.encodestring(open(imgFile,"rb").read())
            else:
                #miss image file 
                newImgSrc=imgSrc 
            #print newImgSrc
            imgElement.set('src', newImgSrc)
    
    #change cross reference        
    for xrefElement in root.findall ('.//span'):
        if xrefElement.get('class') == "xref":
            xlinkElem = xrefElement.find ('a')
            xlinkRef = xlinkElem.get('href')
    
            for entry in wordFormTable:
                if xlinkRef == entry[2]:
                    #assign the real word form
                    xlinkRef = entry[1] 
                
            newXlinkRef = '/dictionary/' + allwords[2] + '/' + xlinkRef + '.html'
            xlinkElem.set('href', newXlinkRef)
            
            
    tree = ET.ElementTree(root)

    tree.write (wwwDir+allwords[2]+'/'+ allwords[1] + '.html', encoding='utf-8')    

with open(dictDir+'WordFormTable.txt') as wordFormText:
    wordFormTable = [ getWords(line) for line in wordFormText ]

with open(dictDir+'EntryTable.txt') as dictText:
    for line in dictText:
        processWordDef (line)

