#API PYTHON CRUD

The main objective of this project is to learn and understand how to work with FastApi a modern framework to develop API's fast and asynchronous, also using uvicorn a ASGI server compatible with python.
The CRUD using the class db_alumnes.py is also to understand the pattern CRUD in applications and how they are developed to interact with the page and a database.

#Begin the server 

Be sure that you are in the directory api where the module main.py exists and then run the next command:

uvicorn main:app --reload

#Use Cases

GET /alumnes/list
Optional uses:

    ![AlumnesList](projectScreenshots\alumnesLlist.png)

    When there is no optional items find in the order returns all the list of alumnes without any information about the aula except for DescAula 

    ![AlumnesListASC](projectScreenshots\AlumneListAsc.png)

    Returns all the list of alumnes but ordered alphabetically by the name of the alumne

    ![AlumnesListDESC](projectScreenshots\AlumnesListDesc.png)

    Returns all the list of alumnes but ordered descending alphabetically by the name of the alumne

    ![AlumnesListLIKE](projectScreenshots\AlumneListLike.png)

    Returns all the alumnes whose names matches with the letters found in the order

    ![AlumnesListLIMIT](projectScreenshots\AlumneListLimit.png)

    Returns the list of alumnes but can skip as much alumnes as the integer in skip is, the same with limit but it does not skip, it allows just the number of alumnes you input in limit with an integer.

GET  /alumne/show/numericId

    ![AlumnesReadId](projectScreenshots\AlumneReadId.png)

    Returns 1 alumne using the id to find it

GET  /alumne/listAll

    ![AlumnesListALL](projectScreenshots\AlumneListAll.png)

    Returns the alumne with their respective aula data which gives an entire alumne with aula information.

POST /alumne/add

    ![AlumnesAdd](projectScreenshots\AlumneAdd.png)

    Returns the new alumne created

POST /alumne/loadAlumnes

    ![AlumnesAddCSV](projectScreenshots\AlumneReadCSV.png)

    Decided to return de ids created to follow the trace, kind of more effective way to know the flow of the errors and data.

PUT  /alumne/update/numericId

    ![AlumnePut](projectScreenshots\AlumnePut.png)

    Returns the alumne who has been replaced in order to know what have you changed and be free to create a new one with this data in case of user error

DELETE /alumne/delete/numericId

    ![AlumneDelete](projectScreenshots\AlumneDelete.png)

    Returns the alumne who has been deleted in order to know what have you deleted and avoid the user error in case of incorrect alumne deleted

#View in page

    ![LlistaInWeb](projectScreenshots\LlistaInWeb.png)

    Here we have a view of the representation of the data found in database alumne using javascript to fetch and locate every row in the correspondent place of the table