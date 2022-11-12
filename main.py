from flask import Flask, request
import json
import sqlite3

app = Flask(__name__) # http://api.hungr.dev:5000/ --> (now http://api.hungr.dev/)

app.debug = True
#app.run(debug=True) # changed above line, supposedly this auto-refreshes?
# Narrator: looks like it did not. Changed back to the above...

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
    name = request.args.get('name')
    if name is not None:
        results = cursor.execute("select * from groceryList WHERE name = '%s'" % (name))
    else:
        results = cursor.execute("select * from groceryList")

    for groceryList in results: 
        data.append(dict(
         name=groceryList[0],
         purchases=groceryList[1]
         ))
    
    return json.dumps(data)
    
# GET REQUEST items
@app.route("/items", methods = ['GET'])
def getListItems():
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    data = []
    desc = request.args.get('desc')
    if desc is not None:
        results = cursor.execute("SELECT * from item WHERE groceryList = '%s' ORDER BY frequency DESC" % request.args.get('groceryList')).fetchall()
    else:
        results = cursor.execute("select * from item where groceryList = '%s'" %  request.args.get('groceryList')).fetchall()
    print (results)
    for item in results: 
        data.append(dict(
            id=item[0], 
            name=item[1], 
            count=item[2], 
            note=item[3], 
            groceryList=item[4],
            frequency=item[5],
            username=item[6],
            visible=item[7]))
            
    return json.dumps(data)
    
#POST REQUEST signup
@app.route("/signup", methods = ['POST'])
def signUp():
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    username = request.args.get('username')
    if cursor.execute("SELECT COUNT(*) FROM user WHERE username = '%s'" % (username)).fetchone()[0] != 0:
        return "Username Taken"
    cursor.execute("insert into user (username, password) values ('%s', '%s')" % (username, request.args.get('password')))
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
    name = request.args.get('name')
    if cursor.execute("SELECT COUNT(*) FROM groceryList WHERE name = '%s'" % (name)).fetchone()[0] != 0:
        return "Group Already Added"
    cursor.execute("insert into groceryList (name) values ('%s')" % (name))
    print ("Successfully added the Grocery List '%s'" % (name))
    connection.commit()
    return ("success")

#POST REQUEST items
@app.route("/items", methods = ['POST'])
def addItem():
    input = request.args.get('name')
    nameParameters = input.split(',')
    count = int(request.args.get('count'))
    note = request.args.get('note')
    groceryList = request.args.get('groceryList')
    username = request.args.get('username')
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    for name in nameParameters:     
        if note:
            cursor.execute("insert into item (name, count, note, groceryList, frequency, username, visible) values ('%s', %i, '%s', '%s', %i, '%s', %i)" % (name, count, note, groceryList, 0, username, 1))
            print ("with note")
        else:
            cursor.execute("insert into item (name, count, groceryList, frequency, username, visible) values ('%s', %i, '%s', %i, '%s', %i)" % (name, count, groceryList, 0, username, 1))
            print ("without note")
        connection.commit()

    print ("Added the item %s to the grocery list %s" % (input, groceryList))
    return ("Added the item %s to the grocery list %s" % (input, groceryList))

#UPDATE -- patch groceryList
# increments purchases for the submitted groceryList
@app.route("/groceryList", methods = ['PATCH'])
def updateGroceryList():
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()
    name = request.args.get('name')
    cursor.execute("UPDATE groceryList SET purchases = purchases + %i WHERE name = '%s'" % (1, name))
    connection.commit()
    print("UPDATE groceryList SET purchases = purchases + %i WHERE name = '%s'" % (1, name))
    return("UPDATE groceryList SET purchases = purchases + %i WHERE name = '%s'" % (1, name))
    
#UPDATE -- patch items
@app.route("/items", methods = ['PATCH'])
def updateItem():
    input = request.args.get('id')
    if input is not None:
        parameters = input.split(',')

    name = request.args.get('name') 

    names = request.args.get('names')
    groceryList = request.args.get('groceryList')

    # only convert to int if given, else we get an error converting null to int
    count = request.args.get('count')
    if count is not None:
        count = int(count)

    note = request.args.get('note')

    # only convert to int if frequency is given, else we get an error converting null to int
    visible = request.args.get('visible')
    if visible is not None:
        visible = int(visible)

    username = request.args.get('username')
    connection = sqlite3.connect("dev.db")
    cursor = connection.cursor()

    # patch matching list of id=a,b,c with matching list of frequency=1,2,3
    if names is not None:
        cursor.execute("UPDATE item SET frequency = frequency + 1 WHERE name IN (%s) AND groceryList = '%s'" % (names, groceryList))
        print ("UPDATE item SET frequency = frequency + 1 WHERE name IN (%s) AND groceryList = '%s'" % (names, groceryList))
        connection.commit()
        return ("UPDATE item SET frequency = frequency + 1 WHERE name IN (%s) AND groceryList = '%s'" % (names, groceryList))

    # patch changing username and visibility based on id
    elif username and visible is not None:
        for item in parameters:
            id = int(item)
            cursor.execute("UPDATE item SET username = '%s', visible = %i where id = %i" % (username, visible, id))
            print ("UPDATE item SET username = '%s', visible = %i where id = %i" % (username, visible, id))
            connection.commit()
        return ("UPDATE item SET username = '%s', visible = %i where id = '%s'" % (username, visible, input))

    # patch username to some IDs
    elif username:
        for item in parameters:
            id = int(item)
            cursor.execute("UPDATE item SET username = '%s' where id = %i" % (username, id))
            print ("update item set username = '%s' where id = %i" % (username, id))
            connection.commit()
        return ("update item set username = '%s' where id = '%s'" % (username, input))

    # patch a group of IDs to either all have visible column of 0 or all of 1
    elif visible is not None:
        for item in parameters:
            id = int(item)
            cursor.execute("UPDATE item SET visible = %i where id = %i" % (visible, id))
            print("UPDATE item SET visible = %i where id = %i" % (visible, id))
            connection.commit()
        return("UPDATE item SET visible = %i where id = '%s'" % (visible, input))
        
    elif note:
        for item in parameters:
            id = int(item)
            cursor.execute("update item set name = '%s', count = %i, note = '%s' where id = %i" % (name, count, note, id))
            print ("update item set name = '%s', count = %i, note = '%s' where id = %i" % (name, count, note, id))
            connection.commit()
        return ("update item set name = '%s', count = %i, note = '%s' where id = '%s'" % (name, count, note, input))
    else:
        for item in parameters:
            id = int(item)
            cursor.execute("update item set name = '%s', count = %i where id = %i" % (name, count, id))
            print ("update item set name = '%s', count = %i where id = %i" % (name, count, id))
            connection.commit()
        return ("update item set name = '%s', count = %i where id = '%s'" % (name, count, input))
        

# DELETE items
# Aidan edited to allow ex: id=1,2,3,4 so we can do this in 1 call instead of 100
@app.route("/items", methods = ['DELETE'])
def deleteItem(): 
    connection = sqlite3.connect("dev.db")
    input = request.args.get('id')
    parameters = input.split(',')
    cursor = connection.cursor()
    for item in parameters: 
        id = int(item)
        cursor.execute("delete from item where id = %i;" % id )
        print("delete from item where id = %i" % id)
        connection.commit()
    return("delete from item where id = %s" % input)

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