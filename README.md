# api.hungr.dev

Endpoint           Methods  Rule
-----------------  -------  -----------------------
addGroceryList     POST     /groceryList
addItem            POST     /items
deleteGroceryList  DELETE   /groceryList
deleteItem         DELETE   /items
getGroceryLists    GET      /groceryList
getListItems       GET      /items
hello_world        GET      /
login              POST     /login
signUp             POST     /signup
static             GET      /static/<path:filename>
updateItem         PATCH    /items
