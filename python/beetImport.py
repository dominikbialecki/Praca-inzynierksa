from subprocess import PIPE, Popen


def startImporting(path='.', logs=1):
	tracksId = [] 						#lista id nowo dodanych albumow
	p = Popen(['beet','import', path, '-A'], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
	if logs == 1: print('wykonano import\nsciezki zaimportowanych plikow:')
	albumPath = []	
	for line in p.stderr:					#zapisywanie ścieżek albumów do listy. ścieżki typu byte
		albumPath.append(line.decode('UTF-8')[:-1])
		if logs == 1: print(line.decode('UTF-8')[:-1])
	
	for album in albumPath:
		a = Popen(['beet', 'list', album, '-a', '-f', '$id'], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1) #wyświetlenie id albumu
		for id in a.stdout:
			tracksId.append(id.decode('UTF-8')[:-1])
	if logs == 1: print(tracksId)
	return tracksId
