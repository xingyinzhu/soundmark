# -*- coding: utf-8 -*-
from db import *
from word import *
from wordHtml import fetch,dealstring
from download import downloadmp3
#-------------------------------------------------------------------------------
pathjc = "D:\\jc.txt"
pahtyq = "D:\\yq.txt"
pathadv = "D:\\adv.txt"
pathall = "D:\\all.txt"
pathyl = "D:\\yl.txt"
#-------------------------------------------------------------------------------
def dealWithString(line):
    line = line.strip(' ')
    line = line.lower()
    line = line.replace("\r\n","")
    line = line.replace("\n", "")
    return line
#-------------------------------------------------------------------------------
def getJCWords(path=pathjc):
    filename = open(path)
    value = []
    conn = connectsqlite()
    cnt = 0
    while 1:
        lines = filename.readlines(1000)
        if not lines:
            break
        for line in lines:
            cnt = cnt + 1
            line = dealWithString(line)
            value = fetch(line)
            insertOneToSqlite(conn,value)
            if cnt % 20 == 0:
                conn.commit()
        conn.commit()
    conn.close()
    filename.close()
#-------------------------------------------------------------------------------
def getYQandADVWords(path=pahtyq,wordtype=2):
   
    filename = open(path)
    conn = connectsqlite()
    chinese = "";
    
    cnt = 0
    
    attri = [];
    while 1:
        lines = filename.readlines(1000)
        if not lines:
            break
        for line in lines:
            
            #Blank line
            if line == "\n":
                continue 
            #Chinese
            if is_cn_line(line):
                chinese = line
            #English Word
            if is_cn_line(line)==False and line != "\n":
                line = dealWithString(line)
                value = fetch(line)
                attri = [];
                attri.append(line),attri.append(wordtype),attri.append(chinese)
                insertAttriToSqlite(conn,attri)
                insertOneToSqlite(conn,value)
                cnt = cnt + 1 
            if cnt % 20 == 0:
                conn.commit()
        conn.commit()
    conn.close()
    filename.close()
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
def writeYQtodisk():
    filename = open(pathadv)
    outfile = open('D:\\advout.txt','w')
    conn = connect()
        
    YQ = {}
    
    #results = getYQrecords(conn)
    results = getAdvrecords(conn)
    #print 'haha'
    for result in results:
        w = Word(result[1],result[3],result[4])
        print result[1]
        YQ[result[1]] = w
    conn.close()    
    print 'lala'
    cnt = 1
    while 1:
        lines = filename.readlines(1000)
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
def judgeWordInDB():
    filename = open(pathall)
    conn = connectsqlite()
    
    while 1:
        lines = filename.readlines(1000)
        if not lines:
            break
        for line in lines:
            line = dealWithString(line)
            result = isWordInDB(conn,line)
            if result == False:
                print line
            
    conn.close()
    filename.close()
    
#-------------------------------------------------------------------------------
def is_cn_line(line): 
    len1 = len(line)
    len2 = len(unicode(line,'utf8'))
    return len1 != len2
                
#-------------------------------------------------------------------------------

def fetchWordMp3():
    conn = connect()
    results = getdistinctwords(conn)
    for result in results:
        #print result[0]
        downloadmp3(result[0])
                
#-------------------------------------------------------------------------------
def updateJCWordsType(path=pathjc):
    filename = open(path)
    value = []
    conn = connectsqlite()
    cnt = 0
    while 1:
        lines = filename.readlines(1000)
        if not lines:
            break
        for line in lines:
            cnt = cnt + 1
            line = dealWithString(line)
            #value = fetch(line)
            #insertOneToSqlite(conn,value)
            updateWordsType(conn,line,1)
            if cnt % 20 == 0:
                conn.commit()
        conn.commit()
    conn.close()
    filename.close()
        
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    #fetchWordMp3()
    
    #getJCWords()
    #getYQandADVWords()
    #getYQandADVWords(pathadv,3)
    #judgeWordInDB()
    
    updateJCWordsType()
#-------------------------------------------------------------------------------


