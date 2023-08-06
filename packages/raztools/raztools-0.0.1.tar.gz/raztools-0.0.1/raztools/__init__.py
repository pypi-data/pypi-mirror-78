import os 
import sys 
import time

def MakeLogin(usern,psp) :  #protect your app with username and password
	login = input('Enter your username: ')  
	while login != usern:  
		print('--------------------------\nUsername does not exist.\n')
		login = input('Enter your username: ')   
	if login == usern: 
		loginpswd = input('Enter the password: ')     
		while loginpswd != psp:  
		    print('--------------------------\nWrong password.\n')
		    loginpswd = input('Enter the password: ') 
		if loginpswd==psp : 
			print('You are logged in. ') 


def cleart():  #clear the terminal | linux&windows stable
	time.sleep(1)
	os.system('cls' if os.name=='nt' else 'clear') 


def surefile(pathtofile) : #terms file
	run = open(pathtofile, "r")  
	if run.read()=='RUN=YES': 
		print('You accepted the terms.Everything is good.') 
	else:   
		print('You dont accepted the terms in the '+pathtofile+' file.' )
		time.sleep(6) 
		sys.exit()  

def wait(tims): #shortcut
	time.sleep(tims)

def close(): #shortcut 
	sys.exit()
