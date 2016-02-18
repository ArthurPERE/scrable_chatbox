from Tkinter import *
from socket import *
import threading


text = ''


class Application:

    def hello(self):
        msg = messagebox.askquestion('title','question')

    def __init__(self, form, sock):
        self.sock = sock
        self.nb_col = 1

        self.frame = form

        self.frame.resizable(0,0)
        self.frame.minsize(200, 200)
        self.frame.title('Top Level')

        # Global Padding pady and padx
        pad_x = 5
        pad_y = 5

        # create a toplevel menu
        menubar = Menu(self.frame)
        #command= parameter missing.
        menubar.add_command(label="quit", command=self.frame.quit)
        #command= parameter missing.
        menubar.add_command(label="Menu2")
        #command= parameter missing.
        menubar.add_command(label="Menu3")

        # display the menu
        self.frame.config(menu=menubar)

        # Create controls

        label1 = Label(self.frame, text="Label1")
        self.txt = StringVar()
        textbox1 = Entry(self.frame, textvariable=self.txt)
        #command= parameter missing.
        button1 = Button(self.frame, text='add text', command=self.addchat)

        scrollbar1 = Scrollbar(self.frame)
        textarea1 = Text(self.frame, width=20, height=10)

        textarea1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=textarea1.yview)

        textarea1.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)
        scrollbar1.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky=W)
        textbox1.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)
        button1.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky=W)
        self.textbox = textbox1
    	self.textarea = textarea1 # see above
    	self.frame.bind("<Return>", lambda x: self.addchat())
        # this is the magic that makes your enter key do something



    def addchat(self):
    	txt = self.textbox.get()
    	# gets everything in your textbox
    	self.textarea.insert(END,"\n"+txt)
    	# tosses txt into textarea on a new line after the end
    	self.textbox.delete(0,END) # deletes your textbox text

        self.sock.send('tb '+txt)
        self.nb_col += 1






    def retrive(self, text):
        if text[:2] == 'tb':

            print txt, 'chat'

            self.textarea.insert(END, "\n"+text[3:])
            self.nb_col += 1

            # for justify the receinved text at right
            # self.textarea.tag_add('tager', '%d.0'%self.nb_col, 'end')
            # self.textarea.tag_config('tager' ,justify='right')



    def begin(self):
        # self.frame.after(0, self.retrive)
        self.frame.mainloop()


    def quit(self):
        self.frame.destroy()

    def update(self, txt):
        global text
        text = txt




if "__main__"=="__name__":
    Application(Tk(), 0)


