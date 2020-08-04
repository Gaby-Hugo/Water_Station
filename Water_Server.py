import socket
import sqlite3
from sqlite3 import Error
import Change_Data
import datetime

# head from the table for print the state of the station
table = '''
+---------------------------------------------------------------+
|  Cod  |       date              |   Alarm 1    |   Alarm 2    |
|---------------------------------------------------------------|
'''


def columns_print(rows):
    # Print the data from the station list in rows
    if len(rows) != 0:
        print(table, end='')
        for row in rows:
            print('| {:^5} | {:^14}    | {:^13}| {:^13}|'.format(*row))
        print('+---------------------------------------------------------------+')
    else:
        print("No data in database yet")



try:

    with sqlite3.connect("station_status.sqlite3") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS station_status (
                station_id INT PRIMARY KEY,
                last_date TEXT,
                alarm1 INT,
                alarm2 INT
            );    
            """)
        conn.commit()
except Error:
    print("Error on connect to the data base")

st_list = Change_Data.create_st_list()


def show_table():
    cursorObject = conn.cursor()
    cursorObject.execute('SELECT * FROM station_status')
    rows = cursorObject.fetchall()
    rows.sort()
    columns_print(rows)


print("EXISTING DATA: ")
show_table()



LISTEN_SIZE = 128
RECV_SIZE = 1024
SERVER_ADDRESS = ('127.0.0.1', 54321)
s = socket.socket()
s.bind(SERVER_ADDRESS)
s.listen(LISTEN_SIZE)

print("server is listening on", SERVER_ADDRESS)


while True:
    c, addr = s.accept()
    print("got connection from", addr)
    data = c.recv(RECV_SIZE)
    message = data.decode()
    new_data_aux = message.split()
    new_data = []
    new_data.append(int(new_data_aux[0])) # Add number station
    # Add date and time
    actual_time = datetime.datetime.now().strftime("%m/%d/%Y  %H:%M:%S")  # Asign datetime
    new_data.append(actual_time)
    new_data.append(int(new_data_aux[1])) # Add alarm 1
    new_data.append(int(new_data_aux[2])) # Add alarm 2

    try:
        with sqlite3.connect("station_status.sqlite3") as conn:
            print("Conected to db")
            cursorObject = conn.cursor()
            cursorObject.execute('INSERT OR REPLACE INTO station_status VALUES (?, ?, ?, ?)',
                                 (new_data[0],new_data[1],new_data[2],new_data[3]))
            conn.commit()

            cursorObject.execute('SELECT * FROM station_status WHERE station_id = ?', [new_data[0]])
            rows = cursorObject.fetchall()
            columns_print(rows)
            if new_data[2] or new_data[3]:
                print("ALARM ACTIVE DETECTED")
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        print(e)

    ack = "Message from server: The update done - Thanks"
    c.send(ack.encode())
    c.close()


