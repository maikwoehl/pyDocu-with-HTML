#!/usr/bin/python3.1
import os
import sys
import sqlite3

import tkhelp_elements as src
import keywordsconf as keyconf

dirList = os.listdir("../pages")
dirList.sort()

conn = sqlite3.connect("../tkhelp.db")
db = conn.cursor()

def write(filename, keywords):
	
	with open("../pages/"+filename, "r") as handler:
		html = handler.read()
	
	inFileHTML = html % { "site_title" : src.site_title, "site_meta" : src.site_meta, "site_css" : src.site_css, "site_js" : src.site_js }
	inFileHTML = inFileHTML.replace("'", "&#x92;")
	inFileHTML = inFileHTML.replace("\n", "")
	try:
		db.execute("INSERT INTO webdocu VALUES ('%(filename)s', '%(keywords)s', '%(inFileHTML)s')" %  { "filename" : filename.replace(".html", ""), "keywords" : keywords, "inFileHTML" : inFileHTML })
		conn.commit()
		return True
	
	except sqlite3.IntegrityError:
		return False
		
		
def backup(filename):
	
	with open("../pages/"+filename, "r") as handler:
		html = handler.read()

	inFileHTML = html % { "site_title" : src.site_title, "site_meta" : src.site_meta, "site_css" : src.site_css, "site_js" : src.site_js }
	inFileHTML = inFileHTML.replace("'", "&#x92;")
	inFileHTML = inFileHTML.replace("\n", "")
	try:
		db.execute("INSERT INTO tkhelp VALUES ('%(filename)s', '%(inFileHTML)s')" %  { "filename" : filename, "inFileHTML" : inFileHTML })
		conn.commit()
		return True
	
	except sqlite3.IntegrityError:
		return False

def checkIn(type):
	
	if type == "normal":
		for sFile in dirList:
			keyname = sFile.replace(".", "_")
			keywords = keyconf.getKeywords(keyname)
			writeHandler = write(sFile, keywords)
			if writeHandler:
				print(sFile, "wurde erfolgreich in Datenbank geladen!")
			else:
				print("Datensatz %(filename)s existiert!" % { "filename": sFile })
	
	elif type == "delete":
		db.execute("DELETE FROM webdocu")
		conn.commit()
		checkIn("normal")
		
	elif type == "backup":
		db.execute("DELETE FROM tkhelp")
		for sFile in dirList:
			keyname = sFile.replace(".", "_")
			keywords = keyconf.getKeywords(keyname)
			writeHandler = backup(sFile)
			if writeHandler:
				print("Datensatz '",sFile,"' wurde gesichert!")
				
		print("Sie koennen die SQL Daten aus der tkhelp-Tabelle exportieren(Fremdtools benoetigt)")

try: 			
	if sys.argv[1]:
		if sys.argv[1] == "update":
			checkIn("delete")
			sys.exit(0)
		
		elif sys.argv[1] == "backup":
			checkIn("backup")
			sys.exit(0)
			
		else:
			print("Unknown parameter, program execute...")
	else:
		pass
		
except IndexError:
	pass
			


checkIn("normal")
