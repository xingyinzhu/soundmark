# -*- coding: utf-8 -*-
from wordHtml import *
from db import *
#-------------------------------------------------------------------------------
path = "D:\\jc.txt"
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
        outfile.writelines("     [" + result[2] + ']\n')
        #print result[1] + " " + result[3] + " " + result[4] + '\r\n'
        #print 'ID: %d WORD %s ENGLISHMARK %s AMERICAMARK %s MEANING %s TYPE %d' % result
        cnt = cnt + 1
    outfile.close()
    conn.close()    
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    writetodisk()


#-------------------------------------------------------------------------------


