class Artists(object):
    def __init__(self,artist=None,album=[],path=[]):
        self.artist=artist
        self.album=album
        self.path=path
        
class Years(object):
    def __init__(self,year=None,album=[],path=[]):
        self.year=year
        self.album=album
        self.path=path

class Alfabets(object):
    def __init__(self,letter=None,album=[],path=[]):
        self.letter=letter
        self.album=album
        self.path=path
        
def sortArt(art,items):
    artists=[]
    art=sorted(art)
    for i in range(len(art)):
        tempalb=[]
        temppath=[]
        for j in range(len(items)):
            if(art[i][0]==items[j][0]):
                tempalb.append(items[j][2])
                if(items[j][3]==''):
                    temppath.append('brak')
                else:
                    temppath.append(items[j][3])
        artists.append(Artists(art[i][0],tempalb,temppath))
    for i in range(len(artists)):
        print(artists[i].artist)
    return artists

def sortYear(year,items):
    years=[]
    year=sorted(year)
    for i in range(len(year)):
        tempalb=[]
        temppath=[]
        for j in range(len(items)):
            if(year[i][0]==items[j][1]):
                tempalb.append(items[j][2])
                if(items[j][3]==''):
                    temppath.append('brak')
                else:
                    temppath.append(items[j][3])
        years.append(Years(year[i][0],tempalb,temppath))
    return years

def listLetters(items):
    letters=[]
    for i in range(len(items)):
        if(items[i][2]==''):
            letters.append('N')
        else:
            temp=items[i][2]
            letters.append(temp[:1])
    lett=sorted(list(set(letters)))
    return lett

def sortAlfabets(items):
    letters=listLetters(items)
    alfabet=[]
    for i in range(len(letters)):
        tempalb=[]
        temppath=[]
        for j in range(len(items)):
            tempsort=items[j][2]
            if(tempsort[:1]==letters[i]):
                tempalb.append(items[j][2])
                if(items[j][3]==''):
                    temppath.append('brak')
                else:
                    temppath.append(items[j][3])
            elif(items[j][2]=='' and letters[i]=='N'):
                tempalb.append('Nieznany album');
                if(items[j][3]==''):
                    temppath.append('brak')
                else:
                    temppath.append(items[j][3])
        alfabet.append(Alfabets(letters[i],tempalb,temppath))
    return alfabet
