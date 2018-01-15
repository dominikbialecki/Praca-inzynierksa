#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
import inspect, os, shutil

path=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dbfile=path+"/yamo.db"
print(dbfile)

def create_connection():
    try:
        conn = sqlite3.connect(dbfile)
        print(sqlite3.version)
        conn.close()
        return 2
    except Error as e:
        print(e)
        return -1
        
def create_table():
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS images(artist TEXT, album TEXT,year TEXT, pathfile TEXT, shortpath TEXT)")
        db.commit()
        db.close()
        return 2
    except Exception as e:
        raise e
        return -1
        
def checkTable():
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        query="select artist,album from `images`"
        cursor.execute(query)
        result=cursor.fetchall() 
        db.close()
        return result
    except Exception as e:
        raise e
    
def returnAllTable():
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        query="select artist,year,album,shortpath from `images`"
        cursor.execute(query)
        result=cursor.fetchall() 
        db.close()
        return result
    except Exception as e:
        raise e
    
def returnAlbumPath():
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        query="select album,shortpath from `images`"
        cursor.execute(query)
        result=cursor.fetchall() 
        db.close()
        return result
    except Exception as e:
        raise e
    
def returnArtist():
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        query="select distinct artist from `images`"
        cursor.execute(query)
        result=cursor.fetchall() 
        db.close()
        return result
    except Exception as e:
        raise e
    
def returnYear():
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        query="select distinct year from `images`"
        cursor.execute(query)
        result=cursor.fetchall() 
        db.close()
        return result
    except Exception as e:
        raise e
    
def deleteAllTask():
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        query="select pathfile from `images`"
        cursor.execute(query)
        for pathFile, in cursor:
            if(pathFile!=""):
                os.remove(pathFile)
        cursor.execute("DELETE FROM `images`")
        db.commit()
        db.close()
        return 2
    except Exception as e:
        raise e
        return -1
    
def insertToTable(albums,path):
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        query = ("INSERT INTO images(artist, album, year, pathfile, shortpath) VALUES(?,?,?,?,?)")
        
        for i in range(len(albums)):
            if(albums[i][2]!='None'):
                temp="/static/images/cover"+str(i)+".jpg"
                allpath=path+temp
                shortpath=".."+temp
                data_employee = (albums[i][1],albums[i][0],albums[i][3],allpath ,shortpath)
                new=albums[i][2]
                result=cursor.execute(query, data_employee)
                shutil.copy2(albums[i][2],allpath)
            else:
                data_employee = (albums[i][1],albums[i][0],albums[i][3],"" ,"")
                result=cursor.execute(query, data_employee)
        db.commit()
        db.close()   
        return 2
    except Exception as e:
        raise e
        return -1
   
    
        
