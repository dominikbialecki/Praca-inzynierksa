from beets.library import Library
from unidecode import unidecode
from subprocess import PIPE, Popen
import os

def getLibPath():
	"""	
	#ponieważ config.yaml na różnych systemach znajduje sie w różnych miejscach, 
	#lepiej wywolac beet config niz bezposrednio otwierac plik open('/home/dominik/.config/beets/config.yaml', 'r')
	"""
	p = Popen(['beet','config'], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
	for line in p.stdout:
		line = line.decode('UTF-8')[:-1]
		if "library: " in line:
			line = line[9:]
			if not os.path.exists(line):			#w przypadku gdy ścieżka podana jest z użyciem '~/'
				line = os.path.expanduser(line)
			return line



def beetImport(path='.', logs=0):
	#lista id nowo dodanych albumow
	albumsId = [] 						
	p = Popen(['beet','import', path, '-A'], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
	if logs == 1: print('wykonano import\nsciezki zaimportowanych plikow:')
	albumPath = []	
	for line in p.stderr:					
		#zapisywanie ścieżek albumów do listy. ścieżki typu byte
		albumPath.append(line.decode('UTF-8')[:-1])
		if logs == 1: print(line.decode('UTF-8')[:-1])
	
	for album in albumPath:
		#wyświetla id albumu
		a = Popen(['beet', 'list', album, '-a', '-f', '$id'], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1) 
		for id in a.stdout:
			albumsId.append(id.decode('UTF-8')[:-1])
	if logs == 1: print(albumsId)
	return albumsId




def returnAlbums():
    song = getLibPath()
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

def toTime(length):
    i=0;
    l=int(length)
    while l>60:
        l-=60
        i+=1
    if(l<10):
        return str(i)+":0"+str(l)
    else:
        return str(i)+":"+str(l)
    
def returnTitles():
    song = getLibPath()
    lib=Library(song)
    items=lib.items()
    temptitle=[]
    tempalbum=[]
    tempartist=[]
    tempyear=[]
    tempgenre=[]
    temptime=[]
    alls=[]
    for item in items:
        temptitle.append(item['title'])
        tempalbum.append(item['album'])
        tempartist.append(item['artist'])
        tempyear.append(item['year'])
        tempgenre.append(item['genre'])
        temptime.append(toTime(item['length']))
    for i in range(len(temptitle)):
        alls.append([temptitle[i],tempartist[i],tempalbum[i],tempgenre[i],tempyear[i],temptime[i]])
    return alls

