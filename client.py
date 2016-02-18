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

verrou = threading.Lock()

text = ''

##########################################################
def recevoir():
	global Continue_boucle
	global text
	while Continue_boucle:
		data_recv = s.recv(2055)
		print data_recv, 'client'


		if data_recv[:2] == 'tb':
			text = data_recv[3:]

		if 'fin' in data_recv:
			Continue_boucle = False
			appli.quit()

##########################################################




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
	t_chat = threading.Thread(target=chat)
	
	t_chat.start()
	t.start()

	print 'aaa'

	while Continue_boucle:
		if Continue_boucle == False:
			break




###########################################################
except KeyboardInterrupt:
	s.send('fin')
	print 'Vous avez pressez ctrl+C'


except error:
	print 'error'

###########################################################
finally:
	# fermeture de la connexion
	print "finally ..."
	Continue_boucle=False
	t.join()
	print 'fini'
	t_chat.join()
	s.shutdown(1)
	s.close()
	sys.exit(1)

print "fin du client TCP"











#############################################################
def Application():
	global frame
	global nb_col
	global textbox
	global textarea

	nb_col = 1

	frame = Tk()

	frame.resizable(0,0)
	frame.minsize(200, 200)
	frame.title('Top Level')

	# Global Padding pady and padx
	pad_x = 5
	pad_y = 5

	# create a toplevel menu
	menubar = Menu(frame)
	#command= parameter missing.
	menubar.add_command(label="quit", command=frame.quit)
	#command= parameter missing.
	menubar.add_command(label="Menu2")
	#command= parameter missing.
	menubar.add_command(label="Menu3")

	# display the menu
	frame.config(menu=menubar)

	# Create controls

	label1 = Label(frame, text="Label1")
	txt = StringVar()
	textbox1 = Entry(frame, textvariable=txt)
	#command= parameter missing.
	button1 = Button(frame, text='add text', command=addchat)

	scrollbar1 = Scrollbar(frame)
	textarea1 = Text(frame, width=20, height=10)

	textarea1.config(yscrollcommand=scrollbar1.set)
	scrollbar1.config(command=textarea1.yview)

	textarea1.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)
	scrollbar1.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky=W)
	textbox1.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)
	button1.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky=W)
	textbox = textbox1
	textarea = textarea1 # see above
	frame.bind("<Return>", lambda x: addchat())
	# this is the magic that makes your enter key do something


def addchat():
	global nb_col
	global textbox
	global textarea

	txt = textbox.get()
	# gets everything in your textbox
	textarea.insert(END,"\n"+txt)
	# tosses txt into textarea on a new line after the end
	textbox.delete(0,END) # deletes your textbox text

	s.send('tb '+txt)
	nb_col += 1




##########################################################
def chat():
	global frame

	Application()

	update()
	frame.mainloop()

def update():
	global nb_col
	global textarea
	global text

	if text != '':
		textarea.insert(END, '\n'+text)

		nb_col += 1

		frame.after(100, update)
