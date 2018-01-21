from subprocess import PIPE, Popen, check_output


class Repo:

	def __init__(self, path='.', logs = 0):
		self.path = path
		self.logs = logs
		self.remotes = []
		self.get_remotes()	


	"""
	Wywołuje git remote w lokalizacji self.path aby pobrać listę zdalnych repozytoriów.
	"""
	def get_remotes(self):		
		p = Popen(['git', 'remote'], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		for remote in p.stdout:
			remoteStr = remote.decode('UTF-8')[:-1]
			if remoteStr not in self.remotes:
				self.remotes.append(remoteStr)
		return self.remotes

	"""
	Wywołanie git init <ścieżka>
	0-repo initialized, 0-repo reinitialized, 1-fail
	"""
	def init(self):									
		cmdAnswer = check_output(['git','init', self.path]).decode('UTF-8')
		if cmdAnswer[:32] == 'Initialized empty Git repository':
			if self.logs == 1: print('Repository initialized')
			return 0
		elif cmdAnswer[:37] == 'Reinitialized existing Git repository':
			if self.logs == 1: print('Repository reinitialized')
			return 0
		else:
			if self.logs == 1: print('Initialization failed') 
			return 1

	"""
	Wywołanie git annex init <ścieżka>
	0-repo initialized, 1-fail
	"""
	def annex_init(self):
		p = Popen(['git', 'annex', 'init', self.path], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		cmdAnswer = p.stdout.readline().decode('UTF-8')
		if cmdAnswer[:-1] == 'init ' + self.path + ' ok':			
			if self.logs == 1: print('Annex repository initialized')
			return 0
		else:
			if self.logs == 1: print('Annex initialization failed') 
			return 1
	
	"""
	Dodanie nowego repozytorium. 
	Funkcja wywołuje git remote add <name> <path> w lokalizacji, w której znajduje się repozytorium self.
	0 - success. 1 - fail
	"""
	def remote_add(self, name, object):
		self.remotes.append(name)
		p = Popen(['git','remote', 'add', name, object.path], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		cmdErr = p.stderr.readline().decode('UTF-8')
		cmdAnswer = p.stdout.readline().decode('UTF-8')
		if (cmdAnswer[:-1] == '') & (cmdErr == ''):
			if self.logs == 1: print('Remote '+ name + ' successfuly added')
			return 0
		else:
			if self.logs == 1: print(cmdErr) 
			return 1

	"""
	Dwustronne łączenie repozytoriów.
	remoteName - nazwa repozytorium zdalnego w repozytorium lokalnym (self)
	localName - nazwa repozytorium lokalnego w repozytorium zdalnym
	0 - succes, 1 - fail
	"""
	def connect_remotes(self, object, remoteName, localName):
		if (self.remote_add(remoteName, object)) | (object.remote_add(localName, self)):
			if self.logs == 1: print('connecting failed')
			return 1
		else:
			return 0
	
 	
	#Wywołanie git annex add <path> w lokalizacji self.path.
	#Zwraca listę dodanych plików
	#@TODO dodawanie kilku plikow naraz
	
	def annex_add(self, path='.'):
		addedFiles = []
		p = Popen(['git','annex', 'add', path], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		for line in p.stdout:
			cmdAnswer = line.decode('UTF-8')[:-1]
			print(cmdAnswer)
			if cmdAnswer == '(recording state in git...)':
				if self.logs == 1: print(len(addedFiles),'files added')
				break
			else:
				addedFiles.append(cmdAnswer[4:-3])
		return addedFiles


	def commit(self, message='adding files', path='.'):
		p = Popen(['git','commit', path, '-m', message], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		if p.stderr.readline().decode('UTF-8')[:-1] =='ok':
			if self.logs == 1: print('commiting: '+p.stdout.readline().decode('UTF-8')[:-1])
			return 0
		else:
			if self.logs == 1: print('commiting failed')
			return 1



	"""
	#Wywołuje git annex whereis <path>, czyli
	#szuka repozytoriów, w których występuje plik <path>
	#zwraca liste repozytoriow, lub 0 gdy nie znaleziono pliku
	##sciezka skracana jest o sciezke repozytorium
	"""
	def annex_whereis(self, path):
		remotes = []
		containsPath = path.find(self.path)
		if containsPath>=0:
			path = path[len(self.path)+1:]
		
		p = Popen(['git','annex', 'whereis', path], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		p.stdout.readline()		
		for cmdAnswer in p.stdout:
			cmdAnswer = cmdAnswer.decode('UTF-8')[:-1]
			index = cmdAnswer.rfind('[')
			index2 = cmdAnswer.rfind(']')
			if index>0 and index2>0:
				remotes.append(cmdAnswer[index+1:index2])
		
		if remotes == []: return 0
		return remotes
		
	"""
	#Wywołuje git annex sync w self.path
	#0 - no errors, 1 - error
	"""
	def annex_sync(self):
		p = Popen(['git','annex', 'sync'], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		cmdAnswer = p.stderr.readline().decode('UTF-8')
		if cmdAnswer == '':
			return 0
		else:
			if self.logs == 1: print(cmdAnswer)			
			return 1

	"""
	Wywołuje git annex get w celu pobrania plikow ktore nie znajduja sie w repozytorium
	#1 - brak bledu, lub 0 - blad
	#@TODO zwracanie listy plikow
	"""
	def annex_get(self):
		files = []
		p = Popen(['git','annex', 'get'], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		cmdAnswer = p.stderr.readline().decode('UTF-8')
		if cmdAnswer != '': 
			if self.logs==1: print(cmdAnswer)
			return 1
		for cmdAnswer in p.stdout.readline():
			print(cmdAnswer)
		return 0

	"""
	#return w przypadku ponizszych 3 funkcji zostanie dopisany w razie potrzeby
	"""

	def annex_unlock(self):
		p = Popen(['git','annex', 'unlock'], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
		
	def annex_direct(self):
		p = Popen(['git','annex', 'direct'], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)

	def annex_indirect(self):
		p = Popen(['git','annex', 'indirect'], cwd=self.path, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)


	
