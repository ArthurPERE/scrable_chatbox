from socket import *
import select
from time import time, ctime
import sys
import signal
#from Serveur_Scrabble import *
from threading import *

host = gethostname()
port = 8000

socketPrincipal = socket(AF_INET, SOCK_STREAM)

socketPrincipal.bind((host, port))

socketPrincipal.listen(4)
print 'en ecoute'

nbJoueur = int(raw_input('nombre de Joueur ? '))





#####################################################################
# pour la fin de la boucle
def finir(listSock, listTread, socketPrincipal):
	for i in listSock:
		i.send('fin')
		i.close()

	for i in listTread:
		i.join()

	socketPrincipal.shutdown(1)
	socketPrincipal.close()
####################################################################





Fin_boucle_client = True
####################################################################
def commence(newsocket):
	newsocket.send('commence')

	while True:
		data = newsocket.recv(255)
		print data

		if data == 'fin':
			global Fin_boucle_client
			Fin_boucle_client = False
			print 'fin de la connexion client TCP'
			break

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

		t = Thread(target=commence, args=(news,))
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
	print 'vous avez pressez ctrl+C'
	
except error:
	print 'error'

finally:
	finir(newsoc, threads, socketPrincipal)
	print 'fin de connexion'
#################################################################