from socket import *
import select
from time import time, ctime
import sys
import signal
#from Serveur_Scrabble import *
import threading as th

host = gethostname()
port = 8000

socketPrincipal = socket(AF_INET, SOCK_STREAM)
socketPrincipal.bind((host, port))
socketPrincipal.listen(4)
print 'en ecoute'



nbJoueur = int(raw_input('nombre de Joueur ? '))


verrou=th.Lock()


#####################################################################
# pour la fin de la boucle
def finir(listSock, listThread, socketPrincipal):
	global continue_boucle_client
	print 'commencer l\'apocalypse'


	for i in listSock:
		i.send('fin')
		# i.close()
		# i.shutdown(1)
	print 'fin des client'
	continue_boucle_client = False



	for i in th.enumerate():
		if i != th.currentThread():
			i.join()
	print 'fin des thread'

	socketPrincipal.shutdown(1)
	socketPrincipal.close()
	print 'fin de la socket principal'
####################################################################




continue_boucle_client = True
####################################################################
def commence(newsocket):
	# newsocket.send('commence serveur')
	global continue_boucle_client

	while continue_boucle_client:
		data = newsocket.recv(2055)
		print data


		# si un client c'est arreter
		if data == 'fin':
			verrou.acquire()
			continue_boucle_client = False
			print 'fin de la connexion client TCP'
			newsoc.remove(newsocket)
			verrou.release()


		# distribuer les informations aux autres
		if data[:2] == 'tb':
			verrou.acquire()
			for i in newsoc:
				if i != newsocket:
					i.send(data)
			verrou.release()



####################################################################



threads = [] # liste des threads
newsoc = [] # liste des sockets
##################################################################
try:
	# En attente que tous les joueurs se mettent en place
	while len(newsoc)<nbJoueur:
		news, addr = socketPrincipal.accept()
		print "connected from", addr

		# liste des thread et des sockets
		t = th.Thread(target=commence, args=(news,))
		threads.append(t)
		newsoc.append(news)

		news.send('joueur %d'%len(newsoc))

		t.start()






	# si un client se deconecte alors le serveur s'arrete
	while continue_boucle_client:
		if continue_boucle_client==False:
			break


# si on appuie sur ctrl-C
except KeyboardInterrupt:
	print 'vous avez pressez ctrl+C'
	
except error:
	print 'error'


# pour finir
finally:
	finir(newsoc, threads, socketPrincipal)
	print 'fin de connexion'
	sys.exit(1)
#################################################################