class Letters(object):
    def __init__(self,letter,artist=[],path=[],ids=[]):
        self.letter=letter
        self.artist=artist
        self.path=path
        self.ids=ids
        
class tempClass(object):
     def __init__(self,art=None,path=[]):
        self.art=art
        self.path=path
        
def letters(items):
    letterslist=[]
    for i in range(len(items)):
        if(items[i][0]==''):
            letterslist.append('N')
        else:
            temp=items[i][0]
            letterslist.append(temp[:1])
    lett=sorted(list(set(letterslist)))
    return lett

def tempPath(items,art):
    artists=[]
    for i in range(len(art)):
        temppath=[]
        for j in range(len(items)):
            if(art[i][0]==items[j][0]):
                temppath.append(items[j][3])
        artists.append(tempClass(art[i][0],temppath))
    return artists
    
def onePath(j,artists):
    if(all(v is '' for v in artists[j].path)):
        return 'brak'
    else: 
        for q in range(len(artists[j].path)):
            if(artists[j].path[q]==''):
                    del(artists[j].path[q])
        return artists[j].path[0]
        
def sortArt(items,art):
    artists=tempPath(items,art)
    listletter=letters(items)
    arts=[]
    for i in range(len(listletter)):
        tempart=[]
        temppath=[]
        tempids=[]
        for j in range(len(artists)):
            tmp=artists[j].art
            if(listletter[i]==tmp[:1]):
                tempart.append(tmp)
                temppath.append(onePath(j,artists))
                tempids.append(items[j][4])
            elif(tmp=='' and listletter[i]=='N'):
                tempart.append(tmp)
                temppath.append(onePath(j,artists))
                tempids.append(items[j][4])
            
        arts.append(Letters(listletter[i],tempart,temppath,tempids))
    return arts
   
            
