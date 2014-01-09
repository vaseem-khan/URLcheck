from Tkinter import *
import tkMessageBox
import trainer as tr
import pandas
import main

root = Tk()
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

L1 = Label(frame, text="Enter the URL: ")
L1.pack( side = LEFT)
E1 = Entry(frame,bd =5, width=150)
E1.pack(side = RIGHT)

def submitCallBack():
	url=E1.get()
	main.process_test_url(url,'test_features.csv')
	return_ans = tr.gui_caller('url_features.csv','test_features.csv')
	a=str(return_ans).split()
	if int(a[1])==0:
		tkMessageBox.showinfo( "URL Checker Result","The URL "+url+" is Benign")
	elif int(a[1])==1:
		tkMessageBox.showinfo( "URL Checker Result","The URL "+url+" is Malicious")
	else:
		tkMessageBox.showinfo( "URL Checker Result","The URL "+url+" is Malware")
   		   
B1 = Button(bottomframe, text ="Submit", command = submitCallBack)

B1.pack()

root.mainloop()