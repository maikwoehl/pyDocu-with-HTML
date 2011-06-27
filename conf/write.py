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
		
		
def backup():
	try:
		sql = "SELECT * FROM webdocu"
		backup_sql = db.execute(sql)
		for row in backup_sql:
			sql_save = "INSERT INTO backup VALUES ('%(filename)s', '%(keywords)s', '%(inFileHTML)s')" %  { "filename" : row[0], "inFileHTML" : row[2], "keywords" : row[1] }
			print(sql_save)
			db.execute(sql_save)
			print(row[0]+"saved!")
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
		backup()
		print("If you can't view the sql file with an sql viewer or sql admin tool, you should use the backup2save command!")
				

try: 			
	if sys.argv[1]:
		if sys.argv[1] == "update":
			checkIn("delete")
			sys.exit(0)
		
		elif sys.argv[1] == "backup":
			checkIn("backup")
			sys.exit(0)
			
		elif sys.argv[1] == "dumpSQL":
			print("Please specify a dump-Filename!")
			dumpfile = input("Exit with X! \nfilename: ")
				
			if dumpfile != "X":
				with open(dumpfile, 'w') as f:
					for line in conn.iterdump():
						f.write('%s\n' % line)
				print("Written to "+dumpfile+"!")	
				sys.exit(0)	
			else:
				sys.exit(0)
				
		elif sys.argv[1] == "dump2DB":
			print("Save another DUMP file to restoredump.sql")
			with open("restoredump.sql", 'w') as f:
					for line in conn.iterdump():
						f.write('%s\n' % line)
						
			print("Choose one of this files:")
			print(os.system("dir"))
			print()
			print("Please specify your Dump-File!")
			dumpfile = input("Exit with X! \nfilename:")
			
			if dumpfile == "X":
				pass
			elif dumpfile == "x":
				pass
			else:
				try:
					db.execute("DROP TABLE webdocu")
					db.execute("DROP TABLE backup")
					conn.commit()
				except sqlite3.OperationalError:
					pass
				
				with open(dumpfile, "r") as f:
					dump = f.read()
					
				db.executescript(dump)
				conn.commit()
				print("Restore from "+dumpfile+"!")
				sys.exit(0)
			
			
		else:
			print("Unknown parameter, program execute...")
	else:
		pass
		
except IndexError:
	pass
			


checkIn("normal")
