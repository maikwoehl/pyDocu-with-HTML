''' This file controls the Keywords in the Database. Add a new line with the module-name and fill in the keywords with following syntax: key1 key2 key3 keyN'''
tkinter = "tkinter interface tcl import lightweight system performance tk gui bindings python graphical user interface"
button = "tcl tk widget button"
entry = "tcl tk widget entry"

def getKeywords(keyname):
	if keyname == None:
		return "The entered Keyword is incorrect"
		
	elif keyname == "tkinter_html":
		return tkinter
	elif keyname == "button_html":
		return button
	elif keyname == "entry_html":
		return entry
