from beets.library import Library
from unidecode import unidecode

def returnAlbums():
    song = "/home/arhelius/Dokumenty/music/database/library.db"
    lib=Library(song)
    items=lib.albums()
    tempalb=[]
    tempart=[]
    temppath=[]
    tempyear=[]
    alls=[]
    for item in items:
        tempalb.append(str(item['album']))
        tempart.append(str(item['albumartist']))
        temp2=unidecode(str(item['artpath']))
        if(temp2!='None'):
            temppath.append(temp2[2:-1])
        else:
            temppath.append('None')
        tempyear.append(item['year'])
        
    for i in range(len(tempalb)):
        alls.append([tempalb[i],tempart[i],temppath[i],tempyear[i]])
    return alls


def returnTitles():
    song = "/home/arhelius/Dokumenty/music/database/library.db"
    lib=Library(song)
    items=lib.items()
    temptitle=[]
    tempalbum=[]
    tempartist=[]
    tempyear=[]
    alls=[]
    for item in items:
        temptitle.append(item['title'])
        tempalbum.append(item['album'])
        tempartist.append(item['artist'])
        tempyear.append(item['year'])
    for i in range(len(temptitle)):
        alls.append([temptitle[i],tempartist[i],tempalbum[i],tempyear[i]])
    return alls
