from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sys
import inspect, os
path=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, path)
import python.beetsCommands as bc, python.beetsCombination as bk, python.beetsYears as by
import database.database as db
app = Flask(__name__)
db.create_table()

def organisationBeets():
    albums=bc.returnAlbums()
    print(albums)
    if(len(db.checkTable())==0):
        if(db.insertToTable(albums,path)>0):
            print("dodano dane")
        else:
            print("Blad operacji")
    elif(len(db.checkTable())!=len(albums) and len(db.checkTable())>0):
        if(db.deleteAllTask()>0):  
            print("usunieto dane")
            db.insertToTable(albums,path)
            print("dodano dane")
        else:
            print("Blad operacji")
    elif(len(db.checkTable())==len(bc.returnAlbums())):
        count=0
        res=db.checkTable()
        for i in range(len(res)):
            if(res[i][0]==albums[i][1] and res[i][1]==albums[i][0]):
                count+=0
            else:
                cout+=1
        if(count!=0):
            if(db.deleteAllTask()>0):  
                print("usunieto dane")
                db.insertToTable(albums,path)
                print("dodano dane")
            else:
                print("Blad operacji")
    else:
        print("Blad operacji")
        
    #db.deleteAllTask()
    
@app.route("/")
def albumy():
    result=db.returnAlbumPath()  
    print(result)
    return render_template('albums.html',result=result)

@app.route("/artists")
def artysci():
    result=db.returnArtistPath() 
    return render_template('artists.html',result=result)

@app.route("/songs")
def muzyka():
    allfunc=bk.func(bc.returnTitles(),bc.returnAlbums())
    return render_template('songs.html',allfunc=allfunc)

@app.route("/years")
def rok():
    years=by.func(bc.returnTitles(),bc.returnOnlyYear(),bc.returnAlbums())
    return render_template('years.html',years=years)

@app.route("/files_editions")
def edycjaP():
    return render_template('files_editions.html')

if __name__ == "__main__":
    organisationBeets()
    app.run(debug=True, use_reloader=True)
