class Years(object):
    def __init__(self,year=None,title=[],artist=[],album=None):
        self.year=year
        self.title=title
        self.artist=artist
        self.album=album
        
def func(items,years,albums):
    yearslist=[]
    for i in range(len(years)):
        tempart=[]
        temptitle=[]
        for j in range(len(items)):
            if(str(years[i])==str(items[j][3])):
                temptitle.append(items[j][0])
                tempart.append(items[j][1])
        yearslist.append(Years(years[i],temptitle,tempart,albums[i][0]))
    return yearslist
