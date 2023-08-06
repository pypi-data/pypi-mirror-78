#####################################################################
#Programm author: Carmelo Sammarco
#####################################################################

#< TkLogin - A python Tkinter Login system >
#Copyright (C) <2020>  <Carmelo Sammarco - sammarcocarmelo@gmail.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################################################################

#########################
# IMPORT MODULES NEEDED #
#########################
import pkg_resources

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


import os
import json

def main(args=None):
    
    window = Tk()
    window.title("TkLogin")

    sideFrame = Frame(window)
    rightFrame = Frame(window)
    sideFrame.pack(side=LEFT)
    rightFrame.pack(side=RIGHT)

    #window.geometry('500x600')


    def log():

        ###########
        #LOGIN
        ###########
        filejason =  pkg_resources.resource_filename('TkLogin', 'Data/Users_Database.json')
        Database = {}
        with open (filejason, "r") as logfile:
            Database = json.load(logfile)
            Utenti = list(Database.keys())
            for Utenti in Database.keys():  
                listdic = Database.get(Utenti) 
                Usr = listdic[0] 
                Pass = listdic[1]
                if Usr == User.get() and Pass == Pwd.get():
                    messagebox.showinfo('TkLogin', 'Login successful! credentials found in the database')
                    print ("Login successful! credentials found in the database")
                    break
                else:
                    messagebox.showinfo('TkLogin', 'Login failed! credentials not found in the database')
                    print("Login failed! credentials not found in the database")
                    break

    #######################
    #GUI interface
    #######################
   
    Username = Label(sideFrame, text="Username")
    Password = Label(sideFrame, text="Password")
    txtlogin = Label(sideFrame, text="Login")

    Username.pack()
    Password.pack()
    txtlogin.pack()


    User = Entry(rightFrame, width=13)
    Pwd = Entry(rightFrame, width=13, show="*")
    btnlogin = Button(rightFrame, text="Enter", bg="red", command=log)

    User.pack()
    Pwd.pack()
    btnlogin.pack()
    
    #################################################################

    window.mainloop()

