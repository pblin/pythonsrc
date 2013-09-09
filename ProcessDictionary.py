#!/usr/bin/env python
from elementtree import ElementTree as ET
import urllib2

def downloadfile(sourceUrl, destDir):
	u = urllib2.urlopen(sourceUrl)
	words = sourceUrl.split('/')
	localFile = open(destDir+words[-1], 'w')
	localFile.write(u.read())
	localFile.close()

downloadfile('http://bits.blioreader.com/partners/Scholastic/SLInstall/QAStandard/UpdateManifest.xml?uniqueRequest=634971476181326349_6069547', '/home/bernard/storia_dictionary')

tree = ET.parse ('/home/bernard/storia_dictionary/manifest.xml')
root = tree.getroot()

forUpdate= ['DictionaryText', 'DictionaryPron', 'DictionaryImage', 'DictionaryAudio']

for updateElement in root.findall('UpdateComponent'):
	updateName = updateElement.get('Name')
	#print updateName
	if updateName in forUpdate:
		for updateEntry in updateElement.findall('UpdateEntry'):
			version=updateEntry.get('EndVersion')
			fileUrl=updateEntry.get('href') 
			if fileUrl and ".exe" not in fileUrl:
				print fileUrl
				downloadfile(fileUrl,'/home/bernard/storia_dictionary/')
		





