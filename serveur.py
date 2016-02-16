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
	print 'commencer l\'apocalypse'
	for i in listSock:
		i.send('fin')
		i.close()
		i.shutdown(1)
	print 'fin des client'
	print th.enumerate()
	for i in th.enumerate():
		if i != th.currentThread():
			i.join()
	print 'fin des thread'
	socketPrincipal.shutdown(1)
	socketPrincipal.close()
	print 'fin de la socket principal'
####################################################################




Fin_boucle_client = True
####################################################################
def commence(newsocket):
	newsocket.send('commence')
	global Fin_boucle_client

	while Fin_boucle_client:
		data = newsocket.recv(2055)
		print data

		if data == 'fin':
			Fin_boucle_client = False
			print 'fin de la connexion client TCP'
			newsoc.remove(newsocket)

		if data[:2] == 'tb':
			verrou.acquire()
			for i in newsoc:
				if i != newsocket:
					i.send(data[3:])
			verrou.release()



####################################################################



threads = []
newsoc = []
##################################################################
try:
	# En attente que tous les joueurs se mettent en place
	while len(newsoc)<nbJoueur:
		news, addr = socketPrincipal.accept()
		print "connected from", addr
		news.send('connected\n')

		t = th.Thread(target=commence, args=(news,))
		threads.append(t)
		newsoc.append(news)
		t.start()





	# si un client se deconecte alors le serveur s'arrete
	while Fin_boucle_client:
		data = raw_input('>> ')
		if Fin_boucle_client==False:
			break

		for i in newsoc:
			print 'envoyer'
			i.send(data)

		if data == 'fin':
			break


except KeyboardInterrupt:
	for i in newsoc:
		i.send('fin serveur')
	print 'vous avez pressez ctrl+C'
	
except error:
	print 'error'

finally:
	finir(newsoc, threads, socketPrincipal)
	print 'fin de connexion'
	sys.exit(1)
#################################################################