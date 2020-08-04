import socket
import sqlite3
from sqlite3 import Error
# import Change_Data
import datetime


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

# st_list = Change_Data.create_st_list()


LISTEN_SIZE = 128
RECV_SIZE = 1024
SERVER_ADDRESS = ('127.0.0.1', 54321)
s = socket.socket()
s.bind(SERVER_ADDRESS)
s.listen(LISTEN_SIZE)

while True:
    c, addr = s.accept()
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
            cursorObject = conn.cursor()
            cursorObject.execute('INSERT OR REPLACE INTO station_status VALUES (?, ?, ?, ?)',
                                 (new_data[0],new_data[1],new_data[2],new_data[3]))
            conn.commit()


    except sqlite3.Error as e:
        conn.rollback()
        conn.close()

    c.close()


