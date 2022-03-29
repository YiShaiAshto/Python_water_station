# Python_water_station

**The project made out of the the following four files:**

1.server.py - represents the server.
2.data.sqlite - SQLite 3 database used by the server to store data on the client (will be located in
the same directory as the server)  data.sqlite, it can be generated by server.py.
3.client.py - Represents a single client. meant to be copied to different folders and executed on
each.
4.status.txt - represents the data of the client, each status.txt is meant to be copied to the same
folder as client.py and is meant to have different data inside (at least a different ID).

**Explanation for the Client Code:**

The client runs in a loop in which it reads data from its status.txt, connects to the server,
and sends the data to the server, he doing this once every 60 seconds.
status.txt will contain the data of a single water station using the following 3 lines
● the first line represents the station ID (some integer)
● the second line represent the state of Alarm1 (0 for OFF; 1 for ON)
● the second line represent the state of Alarm2 (0 for OFF; 1 for ON)

For example if the file contains the following lines:
123
0
1

Then it represents station ID 123, its first alarm is OFF and its second Alarm is ON.

**Explanation for the Server:**

As one of the first actions of the server, it will open data.sqlite (this action will create the file if it
didn't exist before) and then the server will create a table for the station data if it doesn't exist
yet.

The database will contain a single table called station_status. and will contain the following columns:
station_id - for the station ID (will act as a primary key, meaning we only store a single line per
station ID)
last_date - text representing the last date the station contacted the server
alarm1 - 0 or 1 representing if the alarm was on or off
alarm2 - 0 or 1 representing if the alarm was on or off

When receiving data from a station ID that doesn't exist yet in the database a new line will be
inserted, when receiving data from a station ID that already exists its fields will be updated.

