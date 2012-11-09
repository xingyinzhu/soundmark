# -*- coding: utf-8 -*-

import MySQLdb

#-------------------------------------------------------------------------------
dbhost = 'localhost'
dbuser = 'root'
dbpswd = '123456'
dbport = 3306
#-------------------------------------------------------------------------------

def connect():
    conn = MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpswd,port=dbport)
    return conn

#-------------------------------------------------------------------------------
def testinsertonerecord(conn,value):
    cur = conn.cursor()
    conn.select_db('dict')
    
    #print value
    
    sql = """INSERT INTO TEST_WORD(ID,\
       WORD, ENGLISHMARK, AMERICAMARK, MEANING,TYPE,SENSEGROUP) \
       VALUES ("%d", "%s", "%s", "%s", "%s", "%d", "%s" )""" % \
       (0,value[0], value[1], value[2], value[3], value[4],value[5])
    
    try:
        #print sql
        cur.execute(sql)
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        #print 'error!!!!!'
        conn.rollback()
#-------------------------------------------------------------------------------

def getrecord(conn):
    cur = conn.cursor()
    
    conn.select_db('dict')
    count=cur.execute('select * from word')
    
    print 'there has %s rows record' % count
    
    results =cur.fetchmany(2)
    for result in results:
        #print result
        print 'ID: %d WORD %s ENGLISHMARK %s AMERICAMARK %s MEANING %s TYPE %d' % result
    
#-------------------------------------------------------------------------------
def getresults(conn):
    cur = conn.cursor()
    
    conn.select_db('dict')
    cur.execute('select * from test_word')
    results =cur.fetchall()
    return results
#-------------------------------------------------------------------------------
def insertonerecord(conn,value):
    cur = conn.cursor()
    conn.select_db('dict')
        
    
    sql = """INSERT INTO WORD(ID,\
       WORD, ENGLISHMARK, AMERICAMARK, MEANING,TYPE,SENSEGROUP) \
       VALUES ("%d", "%s", "%s", "%s", "%s", "%d", "%s" )""" % \
       (0,value[0], value[1], value[2], value[3], value[4],value[5])
    
    #sql = MySQLdb.escape_string(sql)

    #cur.execute(sql,(0,value[0], value[1], value[2], value[3], value[4]))
    #cur.executemany('insert into word values(%d,%s,%s,%s,%s)',value)
    try:
        #print sql
        cur.execute(sql)
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        #print 'error!!!!!'
        conn.rollback()
#-------------------------------------------------------------------------------
def getYQrecords(conn):
    cur = conn.cursor()
    conn.select_db('dict')
    sql = """select * from word where sensegroup is not null"""
    cur.execute(sql)
    results =cur.fetchall()
    return results 
#-------------------------------------------------------------------------------
def getAdvrecords(conn):
    cur = conn.cursor()
    conn.select_db('dict')
    sql = """select * from word where TYPE=3"""
    cur.execute(sql)
    results =cur.fetchall()
    return results 
#-------------------------------------------------------------------------------
def getonerecordbyword(conn,value):
    cur = conn.cursor()
    conn.select_db('dict')
    #print """select * from word where WORD='%s'""" %(value)
    sql = """select * from word where WORD='%s'""" %(value)
    cur.execute(sql)
    results =cur.fetchall()
    return results 
#-------------------------------------------------------------------------------
#test
if __name__ == "__main__":
    conn = connect()
    #value=['want','[wɒnt]','[wɒnt]','haha',0]
    #insertonerecord(conn,value)
    getrecord(conn)
    #fetch("help")
    