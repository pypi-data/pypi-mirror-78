#All the modules needed
import jarvpy
import smtplib, ssl
import time
from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from time import strftime
import webbrowser
print("This AI (Pyvis) was created by Vihaan Pundir")
print("Copyright 2050 by Vihaan Pundir, All rights reserved.")
print("Please do not copy this work of coding, or you will have copyright issues.")
print("Pyvis is designed to listen and talk to its Users and never deny them.")
print("Pyvis will listen to you if you command it the right thing.")
print("Hello")
print("Pyvis (Ai) will give you output if you give him these commands:")
print("Email for emailing")
print("Tell the exact time for telling you the time")
print("Open Clock for opening a digital clock page")
print("Wolf. for searching wolframalpha")
print("Open websites for opening websites")
print("And...")
print("Link searcher for searching links")
print("Please do not search anything else")
print("Please report bugs to vihaan.pundir@ps517tccs.org")
print("___________________________________________________________________________________")
def AI():
    search = input("Please command pyvis: ")
    #1
    if search == 'Email':
        while True:
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender_email = input("what is your email address: ")  # Enter your address
            receiver_email = input("Who do you want to send to: ")  # Enter receiver address
            password = input("Type your password and press enter: ")
            message = input("Please enter message: ")

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
                    print("Message sent")

    if search == 'Tell the exact time':  
                now = datetime.now()
                print(now.strftime("%d/%m/%Y %H:%M:%S"))
                time.sleep(1)

    if search == 'Open Clock': 
                # creating tkinter window 
                root = Tk() 
                root.title('Clock') 

                # This function is used to 
                # display time on the label 
                def time(): 
                    string = strftime('%H:%M:%S %p') 
                    lbl.config(text = string) 
                    lbl.after(1000, time) 

                # Styling the label widget so that clock 
                # will look more attractive 
                lbl = Label(root, font = ('calibri', 40, 'bold'), background = 'purple', foreground = 'white') 

                # Placing clock at the centre 
                # of the tkinter window 
                lbl.pack(anchor = 'center') 
                time() 

                mainloop() 
                    
            #2
    if search == 'Open websites':
                while True: 
                    query = input("Please enter what you want to or open: ")
                    webbrowser.open(query)

            #3
    if search == 'Link searcher':
                try:
                    from googlesearch import search
                except ImportError: 
                    print("No module named 'google' found") 

                    # to search
                    while True:
                        query = input("Search links")
                        for j in search(query, tld="com", num=10, stop=10, pause=2):
                            print(j)
jarvpy.AI()
