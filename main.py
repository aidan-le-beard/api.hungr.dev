from flask import Flask, request
import json
import sqlite3

app = Flask(__name__) # http://api.hungr.dev:5000/

app.debug = True

# home page
@app.route("/")
def hello_world(): 
    return "<p>welcome to hungr</p>"


# GET REQUEST groceryList
@app.route("/groceryList", methods = ['GET'])
def getGroceryLists(): 
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    data = []

    results = cursor.execute("select * from groceryList")
    for groceryList in results: 
        data.append(dict(
         name=groceryList[0]
         ))
    
    return json.dumps(data)
    
# GET REQUEST items
@app.route("/items", methods = ['GET'])
def getListItems():
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    data = []

    results = cursor.execute("select * from item where groceryList = '%s'" %  request.args.get('groceryList')).fetchall()
    print (results)
    for item in results: 
        data.append(dict(
            id=item[0], 
            name=item[1], 
            count=item[2], 
            note=item[3], 
            groceryList=item[4]))
            
    return json.dumps(data)
    
#POST REQUEST signup
@app.route("/signup", methods = ['POST'])
def signUp():
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    cursor.execute("insert into user (username, password) values ('%s', '%s')" % (request.args.get('username'), request.args.get('password')))
    connection.commit()
    return "success"
    
#POST REQUEST login
@app.route("/login", methods = ['POST'])
def login():
    if checkPassword(username=request.args.get('username'), password=request.args.get('password')):
        return "User Logged in"
    else: 
        print(request.args.get('username'), request.args.get('password'))
        return "No User or Incorrect Password", 401
            
#POST REQUEST groceryList
@app.route("/groceryList", methods = ['POST'])
def addGroceryList():
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    cursor.execute("insert into groceryList (name) values ('%s')" % request.args.get('name'))
    print ("Successfully added the Grocery List %s" % request.args.get('name'))
    connection.commit()
    return "success"

#POST REQUEST items
@app.route("/items", methods = ['POST'])
def addItem():
    name = request.args.get('name')
    count = int(request.args.get('count'))
    note = request.args.get('note')
    groceryList = request.args.get('groceryList')
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
    return ("Added the item %s to the grocery list %s" % (name, groceryList))
		
	
    
    

#UPDATE
@app.route("/items", methods = ['PATCH'])
def updateItem():
    id = int(request.args.get('id'))
    name = request.args.get('name') 
    count = int(request.args.get('count') )
    note = request.args.get('note')
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    if note:
        cursor.execute("update item set name = '%s', count = %i, note = '%s' where id = %i" % (name, count, note, id))
        print ("update item set name = '%s', count = %i, note = '%s' where id = %i" % (name, count, note, id))
        return ("update item set name = '%s', count = %i, note = '%s' where id = %i" % (name, count, note, id))
    else:
        cursor.execute("update item set name = '%s', count = %i where id = %i" % (name, count, id))
        print ("update item set name = '%s', count = %i where id = %i" % (name, count, id))
        return ("update item set name = '%s', count = %i where id = %i" % (name, count, id))
    connection.commit()
    
# DELETE items
@app.route("/items", methods = ['DELETE'])
def deleteItem(): 
    connection = sqlite3.connect("dev.db")


# DELETE grocery lists
@app.route("/groceryList", methods = ['DELETE'])
def deleteGroceryList(): 
    connection = sqlite3.connect("dev.db")
    name = request.args.get('name')
    cursor = connection.cursor()
    cursor.execute("delete from groceryList where name = '%s'" % name )
    print("delete from groceryList where name = '%s'" % name )
    connection.commit()
    return("delete from groceryList where name = '%s'" % name )

# Helper Functions
def checkPassword(username: str, password: str) -> bool: 
    print ("Given: ",username, password)
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
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