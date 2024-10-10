# TrainStation
This app is a train schedule management and ticketing system that integrates with Neo4j and MongoDB databases. It provides a graphical user interface (GUI) built using Kivy to manage trains, search for connections, purchase tickets, and view them.

Purchase train tickets:

Users can input train details (train number, departure date and time) and their personal information (name, last name) to purchase tickets.
The purchased tickets are saved in MongoDB for future reference.


![image](https://github.com/user-attachments/assets/2185d869-0526-4987-86a4-291b10863477)
Manage train schedules:

Add new trains with details like departure and arrival stations, departure time, date, and track numbers.
Delete trains or specific connections using various criteria (train number, station, date, and time).
Search for train connections:

![image](https://github.com/user-attachments/assets/89ebdd5a-f8b3-40e8-99c1-0b68921880ac)


Passengers can search for available train connections between two cities on a given date.
The app retrieves and displays connections from the Neo4j database.


![image](https://github.com/user-attachments/assets/6a9f7cb2-bbac-445e-9a53-fb5e14a525e7)
