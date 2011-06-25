#!/usr/bin/python3.1
# -*- coding: utf-8 -*-
# getContent
import sys # Für grundlegende Systemfunktionen
import cgi # Für die CGI-Funktion
import cgitb; cgitb.enable() # Debugfunktionen
import sqlite3

# DB Connection
conn = sqlite3.connect("tkhelp.db")
db = conn.cursor()

print("Content-Type: text/html")
print()

form = cgi.FieldStorage()

contentid = form.getvalue("page")

if contentid == None: # Überprüfen, ob contentid überhaupt eine ID enthält
	print("Kein entsprechender Artikel gefunden!")
	print("<br />Suchen sie doch:")
	print(''' 
	<form method="get" action="search.py">
	<input type="text" name="searchquery" />
	<input type="submit" value="Suchen" />
	</form>
	''')
	sys.exit(0)

if contentid.rfind("<") != -1: # Gibt es '<' in der Contentid?
	contentid = contentid.replace("<", "&lsaquo;")

if contentid.rfind(">") != -1: # Gibt es '>' in der Contentid?
	contentid = contentid.replace(">", "&rsaquo;")

if contentid.rfind("'") != -1: # Gibt es >'< in der Contentid?
	contentid = contentid.replace("'", "&#x92;")
	
if contentid != None:
	sql = "SELECT * FROM webdocu WHERE name='%(contentid)s'" % { "contentid" : contentid }
	#db.execute(sql)
	result = db.execute(sql)
	for row in result:
		print(row[2])


