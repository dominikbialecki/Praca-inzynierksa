class Artists(object):
    def __init__(self,artist=None,title=[],album=[],year=[]):
        self.artist=artist
        self.title=title
        self.album=album
        self.year=year
        
def func(items,albums):
    artistslist=[]
    for i in range(len(albums)):
        tempalb=[]
        tempyear=[]
        temptitle=[]
        for j in range(len(items)):
            if(albums[i][1]==items[j][1]):
                tempalb.append(items[j][2])
                temptitle.append(items[j][0])
                tempyear.append(items[j][3])
        artistslist.append(Artists(albums[i][1],temptitle,tempalb,tempyear))
    return artistslist
