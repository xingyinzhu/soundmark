# -*- coding: utf-8 -*-

import MySQLdb
import sqlite3
import datetime
#from wordHtml import fetch
#-------------------------------------------------------------------------------
dbhost = 'localhost'
dbuser = 'root'
dbpswd = '123456'
dbport = 3306
#tmp
attribute_id = 4
#tmp
#-------------------------------------------------------------------------------
sqlitedb = 'd:/dict/dict.db'
#-------------------------------------------------------------------------------
def connectsqlite():
    conn = sqlite3.connect(sqlitedb) 
    return conn
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
def getresults(conn,tablename):
    cur = conn.cursor()
    
    print 'select * from '+ tablename
    cur.execute('select * from ' + tablename + " where id>=43")
    results =cur.fetchall()
    return results
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
def getdistinctwords(conn):
    cur = conn.cursor()
    conn.select_db('dict')
    sql = """select word from word group by word"""
    cur.execute(sql)
    results =cur.fetchall()
    return results 
#-------------------------------------------------------------------------------
def insertAttriToSqlite(conn,value):
    cursor = conn.cursor()
    #print value
    sql = """INSERT INTO ATTRIBUTE(WORD,TYPE,GROUPS)
                       VALUES ("%s","%d", "%s")""" % \
                        (value[0], value[1], value[2])
    
    try:
        cursor.execute(sql)
    except sqlite3.Error,e:
        print "SQL Error %s" % (e)
        conn.rollback()
#-------------------------------------------------------------------------------
def insertOneToSqlite(conn,value):
    cursor = conn.cursor()
    sql = """INSERT INTO WORDS(WORD, ENGLISHMARK, AMERICAMARK, MEANINGS)
                      VALUES ("%s", "%s", "%s", "%s")""" % \
                        (value[0], value[1], value[2], value[3])
                        
    #sql = """INSERT INTO TEST_WORDS(WORD, ENGLISHMARK, AMERICAMARK, MEANINGS)
    #                   VALUES ("%s", "%s", "%s", "%s")""" % \
    #                    (value[0], value[1], value[2], value[3])
                        
    try:
        cursor.execute(sql)
    except sqlite3.Error,e:
        print "SQL Error %s" % (e)
        conn.rollback()
    
#-------------------------------------------------------------------------------
def isWordInDB(conn, word):
    cursor = conn.cursor()
    sql = """SELECT * FROM WORDS WHERE WORD = '%s'""" % (word)
    #print sql
    
    cursor.execute(sql)
    results =cursor.fetchall()
    if len(results) == 0:
        return False
    
    return True

#-------------------------------------------------------------------------------
def trim(str):
    
    str = str.replace("\n", "")
    #str = str.replace("\r\n","")
    return str
    
#-------------------------------------------------------------------------------
#
def buildAttributeIndex(conn, results):
    
    global attribute_id
    
    lasttmp = results[0][3]
    for result in results:
        tmp = result[3]
        if cmp(lasttmp, tmp) != 0:
            lastid = result[0];
            attribute_id = attribute_id + 1
            print "%s %s" %(trim(tmp) , attribute_id);
            updateAndInsert(conn,trim(lasttmp),attribute_id,lastid);
            lasttmp = tmp
        if attribute_id % 60 == 0:
            conn.commit()
            
    conn.commit()
#-------------------------------------------------------------------------------
def updateAndInsert(conn, str, id,lastid):
    cursor = conn.cursor()
    likestr = "%" + str + "%"
    sql = """UPDATE attribute set groups = %d where groups like '%s' and id < %d""" % (id,likestr,lastid)
    #print sql;
    cursor.execute(sql)
    
    
    sql = """INSERT INTO attribute_id(attributeid, attributename)
                      VALUES (%d, "%s")""" % (id, str)
    #print sql;
    cursor.execute(sql)               
    
#-------------------------------------------------------------------------------
def updateWordsType(conn,str,value):
    cursor = conn.cursor()
    selectsql = """select * from word where WORD='%s'""" %(str)
    
    cursor.execute(selectsql)
    results =cursor.fetchall()
    if len(results) == 0:
        insertsql = """ INSERT INTO ATTRIBUTE(WORD,TYPE,GROUPS)
                       VALUES ("%s",%d, %d)""" % \
                        (str, value, 0)
                        
        #print insertsql;
        cursor.execute(insertsql)
    else:
        updatesql = """UPDATE attribute set type = %d where word = '%s'""" % (value, str)
        #print updatesql;
        cursor.execute(updatesql)

#-------------------------------------------------------------------------------
def insertNewValuesToProgress(conn,curvalue,goalvalue):
    cursor = conn.cursor()
    selectsql = """select word from WORDS""";
    cursor.execute(selectsql)
    results = cursor.fetchall();
    
    for result in results:
        word = result[0]
        now=datetime.datetime.now()
        #insertsql = """INSERT INTO progress(word, value, goal, updatetime)
                      #VALUES ("%s", %d, %d, ?)""" % (word, curvalue, goalvalue,now)
        #print insertsql
        cursor.execute("INSERT INTO progress VALUES (?, ?, ? , ?)" , (word, curvalue, goalvalue,now))
    
#-------------------------------------------------------------------------------
#test

#if __name__ == "__main__":
#    value = fetch('help',1,'group')
#    print value
#    conn = connectsqlite()
#    insertOneToSqlite(conn,value)
#    conn.commit()
    #testselectfromsqlite(conn)
    
if __name__ == "__main__":
    
    conn = connectsqlite()
    insertNewValuesToProgress(conn,0,50)
    conn.commit()
    #results = getresults(conn,'attribute')
    #buildAttributeIndex(conn,results)
        
        
        