# api.hungr.dev

|Endpoint         |  Methods | Rule|
|-----------------| -------| -----------------------|
addGroceryList    | POST   |  /groceryList
addItem           | POST   |  /items
getGroceryLists   | GET    |  /groceryList
getListItems      | GET    |  /items
hello_world       | GET    |  /
static            | GET    |  /static/<path:filename>
updateItem        | PATCH  |  /items

### Sample Backend View:
#### Groups that have been created and their number of purchases:
![image](https://user-images.githubusercontent.com/33675444/206811568-6851c0fe-d1da-4c52-aa87-40306af34a76.png)

#### Items that have been added, their associated group, number of purchases, user ID from firebase that added it, etc.
![image](https://user-images.githubusercontent.com/33675444/206811714-86ff865b-4364-4728-adea-8619ffcf01ae.png)
