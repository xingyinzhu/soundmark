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
    
    for result in results:
        print result[1].ljust(20), result[4]
        str = "%s %s\r\n" %(result[1].ljust(20),result[4])
        outfile.writelines(str)
        outfile.writelines("[" + result[3] + ']\r\n')
        #print result[1] + " " + result[3] + " " + result[4] + '\r\n'
        #print 'ID: %d WORD %s ENGLISHMARK %s AMERICAMARK %s MEANING %s TYPE %d' % result
    outfile.close()
    conn.close()    
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    writetodisk()


#-------------------------------------------------------------------------------


