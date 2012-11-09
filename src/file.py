# -*- coding: utf-8 -*-
from wordHtml import *
from db import *
from word import *
#-------------------------------------------------------------------------------
path = "D:\\jc.txt"
pahtyq = "d:\\yq.txt"
#-------------------------------------------------------------------------------
def readWord():
    file = open(path)
    value = []
    conn = connect()
    cnt = 0
    while 1:
        lines = file.readlines(1000)
        if not lines:
            break
        for line in lines:
            cnt = cnt + 1
            line = line.strip(' ')
            value = fetch(line)
            value.append("")
            insertonerecord(conn,value)
            if cnt % 20 == 0:
                conn.commit()
        conn.commit()
    conn.close()
    file.close()    
#-------------------------------------------------------------------------------

def writetodisk():
    outfile = open('D:\\jcout.txt','w')
    conn = connect()
    results = getresults(conn)
    
    cnt = 1
    for result in results:
        #print result[1].ljust(20), result[4]
        string = "%s%s%s\n" %(str(cnt).ljust(5),result[1].ljust(20),result[4])
        outfile.writelines(string)
        outfile.writelines("     [" + result[3] + ']\n')
        #print result[1] + " " + result[3] + " " + result[4] + '\r\n'
        #print 'ID: %d WORD %s ENGLISHMARK %s AMERICAMARK %s MEANING %s TYPE %d' % result
        cnt = cnt + 1
    outfile.close()
    conn.close()    
#-------------------------------------------------------------------------------


def readWordYQ():
    file = open(pahtyq)
    
    conn = connect()
    chinese = "";
    
    cnt = 1
    total = 0;
    while 1:
        lines = file.readlines(1000)
        if not lines:
            break
        for line in lines:
            
            #Blank line
            if line == "\n":
                continue 
            #Chinese
            if is_cn_line(line):
                cnt = 0
                chinese = line
            #English Word
            if is_cn_line(line)==False and line != "\n":
                line = line.strip(' ')
                value = fetch(line.lower())
                value.append(chinese)
                insertonerecord(conn,value)
                cnt = cnt + 1 
                total = total + 1
            if total % 20 == 0:
                conn.commit()
        conn.commit()
    conn.close()
    file.close()
#-------------------------------------------------------------------------------
def writeYQtodisk():
    file = open(pahtyq)
    outfile = open('D:\\yqout.txt','w')
    conn = connect()
    chinese = "";
    
    YQ = {}
    
    results = getYQrecords(conn)
    print 'haha'
    for result in results:
        w = Word(result[1],result[3],result[4])
        #print result[1]
        YQ[result[1]] = w
    conn.close()    
    print 'lala'
    cnt = 1
    while 1:
        lines = file.readlines(1000)
        if not lines:
            break
        for line in lines:
            #Blank line
            if line == "\n":
                outfile.writelines(line) 
            #Chinese
            if is_cn_line(line):
                #print "%d : %s" %(cnt,line)
                cnt = 1
                outfile.writelines(line)
                #print chinese
            #English Word
            if is_cn_line(line)==False and line != "\n":
                line = line.strip(' ')
                #line = fetch(line.lower())
                line = line.lower()
                line = dealstring(line)
                
                tmp = YQ[line]
                string = "%s%s%s\n" %(str(cnt).ljust(5),tmp.word.ljust(20),tmp.meanings)
                outfile.writelines(string)
                outfile.writelines("     [" + tmp.soundmark + ']\n')
                cnt = cnt + 1
                 
    file.close()
    outfile.close()
    
    
#-------------------------------------------------------------------------------
def is_cn_line(line): 
    len1 = len(line)
    len2 = len(unicode(line,'utf8'))
    return len1 != len2
                
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    #writetodisk()
    #readWordYQ()
    writeYQtodisk()
#-------------------------------------------------------------------------------


