import sqlite3
import json

connection = sqlite3.connect("dev.db")
cursor = connection.cursor()

def checkPassword(username: str, password: str) -> bool: 
	realPassword = cursor.execute("select password from user where username = '%s'" % (username)).fetchone()
	if realPassword is None:
		print ("No user")
		return False
	if realPassword[0] != password: 
		print ("Incorrect Password")
		return False
	if realPassword[0] == password:
		print("Successful Login")
		return True
		
	
def getGroceryLists(): 
	connection = sqlite3.connect("dev.db")
	cursor = connection.cursor()
	data = []
	results = cursor.execute("select * from groceryList")
	for groceryList in results: 
		data.append(dict(
			name=groceryList[0]
		))
		
	print(json.dumps(data))
	return json.dumps(data)
	
	
def getListItems(groceryList: str):
	connection = sqlite3.connect("dev.db")
	data = []
	cursor = connection.cursor()
	results = cursor.execute("select * from item where groceryList = '%s'" %  groceryList).fetchall()
	for item in results: 
		data.append(dict(
			id=item[0], 
			name=item[1], 
			count=item[2], 
			note=item[3], 
			groceryList=item[4]))
			
	return json.dumps(data)
	
def addUser(username: str, password: str):
	connection = sqlite3.connect("dev.db")
	cursor = connection.cursor()
	cursor.execute("insert into user (username, password) values ('%s', '%s')" % (username, password))
	connection.commit()

def addGroceryList(name: str):
	connection = sqlite3.connect("dev.db")
	cursor = connection.cursor()
	cursor.execute("insert into groceryList (name) values ('%s')" % (name))
	print ("Successfully added the Grocery List %s" % name)
	connection.commit()
	connection.close()
	
def addItem(name: str, count: int, note: str, groceryList: str):
	connection = sqlite3.connect("dev.db")
	cursor = connection.cursor()
	if note:
		cursor.execute("insert into item (name, count, note, groceryList) values ('%s', %i, '%s', '%s')" % (name, count, note, groceryList))
		print ("with note")
	else:
		cursor.execute("insert into item (name, count, groceryList) values ('%s', %i, '%s')" % (name, count, groceryList))
		print ("without note")
	connection.commit()
	
	print ("Added the item %s to the grocery list %s" % (name, groceryList))
		
def deleteItem( id: int ): 
	connection = sqlite3.connect("dev.db")
	cursor = connection.cursor()
	cursor.execute("delete from item where id = %i" % id )
	print("delete item where id = %i" % id)
	
def deleteGroceryList( name: str ): 
	connection = sqlite3.connect("dev.db")
	cursor = connection.cursor()
	cursor.execute("delete from groceryList where name = '%s'" % name )
	print("delete groceryList where name = %s" % name )
	return("delete from groceryList where name = %s" % name )

def updateItem(id: int, name: str, count: int, note: str):
	connection = sqlite3.connect("dev.db")
	cursor = connection.cursor()
	if note:
		cursor.execute("update item set name = '%s', count = %i, note = '%s' where id = %i" % (name, count, note, id))
		print ("update item set name = '%s', count = %i, note = '%s' where id = %i" % (name, count, note, id))
	else:
		cursor.execute("update item set name = '%s', count = %i where id = %i" % (name, count, id))
		print ("update item set name = '%s', count = %i where id = %i" % (name, count, id))
	connection.commit()
	
checkPassword(username = "a", password = "b")
# addGroceryList("demoList")
# addItem(name = "testitem", count = 1, note = "", groceryList = "Senior Project")

print(getListItems("Senior Project"))

getGroceryLists()
updateItem(id = 7, name = "test 2", count = 5, note = "test 2" )