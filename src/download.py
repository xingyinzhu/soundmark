# -*- coding: utf-8 -*-
import re
import os.path
from os.path import basename
from urlparse import urlsplit
import urllib2
from wordHtml import readHtmlContent

##http://dict.baidu.com/s?wd=help
prefix_url=["http://dict.baidu.com/s?wd="]

#mp3path
p1 = re.compile(r'<span>[^"<>]*<b lang="EN-US" xml:lang="EN-US">(?P<value>[^"<>]*)</b>\s*<a href="#" url="(?P<mp3path>[^"<>]*)"')

downloadroot = "D:/dictmp3/"
#-------------------------------------------------------------------------------
def url2name(url):
    return basename(urlsplit(url)[2])

#-------------------------------------------------------------------------------

def download(url, localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url:
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileName:
        # we can force to save the file as specified name
        localName = localFileName + localName
    print localName
    
    f = open(localName, 'wb')
    f.write(r.read())
    f.close()

#-------------------------------------------------------------------------------
def downmp3(word):
    print prefix_url[0]+word
    content = readHtmlContent(prefix_url[0]+word)
    #print content
    
    if content != None:
        miter = p1.finditer(content)
    
    cnt = 0
    for match in miter:
        mp3path = match.group('mp3path')
        if cnt == 0:
            downloadpath = downloadroot + word + "/0/"
        else:
            downloadpath = downloadroot + word + "/1/"
        if not os.path.isdir(downloadpath):
            os.makedirs(downloadpath) 
        download(mp3path,downloadpath)
        
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    downmp3('help')