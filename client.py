from socket import *
import select
from time import time, ctime
import sys
from signal import *
import threading
from Chatbox import *
from Tkinter import *

host = gethostname()
port = 8000



Continue_boucle = True

# appli = True

##########################################################
def recevoir():
	global Continue_boucle
	while Continue_boucle:
		data_recv = s.recv(2055)
		print data_recv, 'client'
	

		if data_recv == 'fin':
			Continue_boucle = False

		if data_recv[:3] == 'tb ':
			appli.retrive(data_recv[2:])
##########################################################


##########################################################
def chat():
	global appli
	root = Tk()
	appli = Application(root, s)






###########################################################
try:

	s = socket(AF_INET, SOCK_STREAM)
	s.connect((host, port))


	FinBoucle = False

	while not FinBoucle:
		data = s.recv(2055)
		print data

		if len(data) != 0:
			FinBoucle = True



	t = threading.Thread(target=recevoir)
	# t_chat = threading.Thread(target=chat)
	
	

	t.start()
	# t_chat.start()

	while Continue_boucle:
		data = raw_input('>> ')
		s.send('tb ' + data)

		if data == 'fin':
			break

	t.join()
	# t_chat.join()



###########################################################
except KeyboardInterrupt:
	s.send('fin')
	# t_chat.join()
	t.join()
	print 'Vous avez pressez ctrl+C'
	s.shutdown(1)
	s.close()
	sys.exit(1)


except error:
	s.close()
	# t_chat.join()
	t.join()
	print 'error'
	s.shutdown(1)
	s.close()
	sys.exit(1)

###########################################################
finally:
	# fermeture de la connexion
	print "finally ..."
	s.shutdown(1)
	s.close()

print "fin du client TCP"

