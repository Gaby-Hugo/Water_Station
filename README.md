# Water_Station
My Python end-of-course project
project:
Create a water station and a database server that talks to the water stations

The server will allow new water stations to connect to it.
For each water station connected to it, every minute the server sends a "keep alive" request
Each water station when it receives keep alive it sends back information that includes:
1) The ID of the water station
2) Current date and time
3) Alarm status
4) Water detector status

The status of the water station will be determined by a text file that will contain information about the water status and the alarm status (0 or 1 for each mode)

When the server receives an update from the water station it updates its database accordingly.

The database server will be represented by the server.py file and will write its information to the data.db database file
 To be of type sqlite3.
 
 A water station will be represented by the client.py file and will read its information from the status.txt file. The file will be updated
 Manually (e.g. by gedit)

The database will contain the statio_status table according to the following query:
 CREATE TABLE IF NOT EXISTS station_status (
station_id INT,
last_date TEXT,
alarm1 INT,
alarm2 INT,
PRIMARY KEY (station_id));

Where station_id is the ID number of the reported station,
And last_date is the last reporting date according to the format "YYYY-MM-DD HH: mm". It can be obtained by the command in Python:
import datetime

datetime.datetime.now (). strftime ('% Y-% M-% d% H:% m')

And alarm1 is alarm mode 1 (its value should be 1 if the alarm is on or 0 if it is not)
And alarm1 is alarm mode 2 (its value should be 1 if the alarm is on or 0 if it is not)
 
The status.txt text file will contain three lines. The first line will contain the station_id (some int number)
The second line will contain alarm mode 1 (text 0 or text 1).
And the third line will contain alarm mode 2 (text 0 or text 1)
For example for the values:
1. 2. 3
0
1

This is station number 123, alarm 1 is off (0) and alarm 2 is on (1)
You can edit the text file with gedit for example and save it, and when client.py opens and reads the file it will use it
To send the information to the server.
  
The information to the server can be sent in the style of the following string:
"ID DATE TIME ALARM1 ALARM2"
for example:
example:
123 123-08-01 20:15 1 0
If we split this text on the server side with a split we get 5 strings in the list
0 -> The id
id = x [0]
1 together with 2 -> the date and time
last_date = x [1] + "" + x [2]
3 -> Alarm 1
alarm1 = x [3]
4-> Alarm 2
alarm2 = x [4]
Each water station will be represented in the database as only one line to be updated by server.py.
To update the database rows you can use insert or replace:
q = "" "
insert or replace into station_status
values (?,?,?,?)
"" "
conn.execute (q, (id, dt, a1, a2))


 The following is a sample diagram of the flow of code and information:
 

data.db server.py client.py status.txt
------- --------- --------- ----------
table: station
 
id | date | alarm1 | alarm2 <- create table
                          LOOP:
         client_list <- accept <----------- connect

                           time.sleep (60)
                           send --- "keep alive" ---> recv
                                                   
                                                   open ... <-
                                                   
insert or replace ... <- recv <- --- send
                              123 123-08-01 20:15 1 0
 
                         REPEAT LOOP


