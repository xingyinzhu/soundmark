# -*- coding: utf-8 -*-
import urllib2
import re
import chardet
from urllib2 import HTTPError,URLError

#-------------------------------------------------------------------------------
path = ""
prefix_url=["http://dict.youdao.com/search?q="]
postfix_url = ["&keyfrom=dict.index"]

#p0 = re.compile(r'<li><span class="date">(?P<date>[^"<>]*)</span>\s*<a href="(?P<url>http://[^<>]*)"\s*target=[^<>]*>(?P<title>[^"<>]*)</a>\s*</li>')
p1 = re.compile(r'<span class="pronounce">(?P<country>[^"<>]*)<span class="phonetic">(?P<value>[^"<>]*)</span>')
p2 = re.compile(r'<div class="trans-container">\s*<ul>(?P<meaning>[^"]*)</ul>')
#p2 = re.compile(r'<div class="trans-container">\s*<ul>(?P<meaning>[^"]*)</ul>\s*<p class="additional">(?P<addition>[^"<>]*)</p>')

#p3 = re.compile(r'<p class="additional">(?P<addition>[^"<>]*)</p>')
#p3 = re.compile(r'')
#-------------------------------------------------------------------------------
def readHtmlContent(url):
    try:
        content = urllib2.urlopen(url).read()
    except HTTPError,e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        content = None
    except URLError,e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        content = None
    #else:
        #content = None
    return content


#-------------------------------------------------------------------------------
def smartcode(stream):
    ustring = stream
    codedetect = chardet.detect(ustring)["encoding"]
    try:
        ustring = unicode(ustring,codedetect)
        #type = sys.getfilesystemencoding()
        type = 'utf8'
        return "%s" %(ustring.encode(type))
        #return "%s" %(ustring.encode('utf8')) 
    except:
        return u"bad unicode encode try!"
#------------------------------------------------------------------------------- 
def dealstring(string):
    string = string.replace("\r\n","")
    string = string.replace("\n", "")
    string = string.strip(' ')
    string = string.replace("</li>","")
    string = string.replace("<li>","")
    string = string.replace("[","")
    string = string.replace("]","")
    return string
#-------------------------------------------------------------------------------
def fetch(word,type,group=None):
    value = []
    word = dealstring(word)
    value.append(word)
    #print prefix_url[0]+word
    print 'now fetch word : %s' %(word) 
    content = readHtmlContent(prefix_url[0]+word)
    
    if content != None:
        miter = p1.finditer(content)
        miter2 = p2.finditer(content)
        
        #phonetic
        cnt = 0
        for match in miter:
                        
            #country = smartcode(match.group('country'))
            #print country
            
            #phonetic = smartcode(match.group('value'))
            phonetic = match.group('value')
            #print 'haha' + phonetic
            phonetic = dealstring(phonetic)
            #print match.group('country')
            #print phonetic
            value.append(phonetic)
            cnt = cnt + 1
        if cnt == 1 :
            value.append(phonetic)
        #meanings
        for match in miter2:
            meanings = match.group('meaning')
            #meanings = smartcode(match.group('meaning'))
            
            meanings = dealstring(meanings)
            #print meanings
            value.append(meanings)
            #additions = smartcode(match.group('addition'))
            
        #for match in miter3:
    #print value
    value.append(group)
    value.append(type)
    return value
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
if __name__ == "__main__":
    print 'haha'