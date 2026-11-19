mailFlood.py

#start of code
#import smtp functions, date functions, and Tkinter
from smtplib import SMTP
import datetime
from tkinter import *


class mf22:

   def __init__(self):

       #make the GUI
       self.window1 = Tk()

	#frames to section the GUI and improve layout
       self.frameTop = Frame((self.window1))
       self.frameTop.pack(side=TOP)
       self.frameBot = Frame((self.window1))
       self.frameBot.pack(side=BOTTOM)
       self.frame1 = Frame((self.frameTop))
       self.frame1.pack(side=LEFT)
       self.frame2 = Frame((self.frameTop))
       self.frame2.pack(side=RIGHT)
       self.frame3 = Frame((self.frameBot))
       self.frame3.pack()
	
	#Put in the labels and texfields and the button
       self.numLbl = Label((self.frame1), text="Number of Emails:")
       self.numLbl.pack()
       self.numTxt = Entry((self.frame2), text="")
       self.numTxt.pack()

       self.fromLbl = Label((self.frame1), text="From:")
       self.fromLbl.pack()
       self.fromTxt = Entry((self.frame2), text="")
       self.fromTxt.pack()

       self.toLbl = Label((self.frame1), text="To:")
       self.toLbl.pack()
       self.toTxt = Entry((self.frame2), text="")
       self.toTxt.pack()

       self.subLbl = Label((self.frame3), text="Subject:")
       self.subLbl.pack()
       self.subTxt = Entry((self.frame3), text="")
       self.subTxt.pack()

       self.msgLbl = Label((self.frame3), text="Message:")
       self.msgLbl.pack()
       self.msgTxt = Entry((self.frame3), text="")
       self.msgTxt.pack()

       self.sendButton = Button((self.frame3), text="Send",
           command=(self.onClicked)) #button activates the event onClicked
       self.sendButton.pack()

       self.doneLabel = Label(self.frame3,
           text="All fields will clear when done")
       self.doneLabel.pack()

       #start the main loop
       self.window1.mainloop()

   def onClicked(self):
	
	#pull data from the entries
       self.num = int(self.numTxt.get())
       self.fromAdd = str(self.fromTxt.get())
       self.toAdd = str(self.toTxt.get())
       self.subj = str(self.subTxt.get())
       self.body = str(self.msgTxt.get())

       #get the time and date
	self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

	#format the message
       self.msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" \
       % ((self.fromAdd), (self.toAdd), (self.subj), (self.date),
(self.body))

	#start the counter and be ready to connect to the mail server
       smtp = SMTP()
       n = 0
       l = self.num

       while n < l:
       	smtp.connect('127.0.0.1', 25)
               smtp.helo('localhost')
               smtp.sendmail((self.fromAdd), (self.toAdd), (self.msg))
               smtp.quit()
               n = n + 1

	#clear all fields once done
       self.numTxt.delete(0, END)
       self.fromTxt.delete(0, END)
       self.toTxt.delete(0, END)
       self.subTxt.delete(0, END)
       self.msgTxt.delete(0, END)

#run the class
if __name__ == "__main__":
   main = mf22()
#end of code

