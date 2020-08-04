import socket
import Change_Data
from datetime import datetime, timedelta


def st_list_update():
    st_list = Change_Data.create_st_list() # existing station list in format for write on the text
    num_list = Change_Data.create_num_list(st_list) # numbers (int) for the stations
    return st_list, num_list

period = 10  # time between sends
# Asign datetime from actual time
time1 = datetime.now()
SERVER_ADDRESS = ('127.0.0.1', 54321)


while True:
    if datetime.now() - time1 >= timedelta(seconds=period):
        time1 = datetime.now()
        st_list, num_list = st_list_update() # autorizted stations list in text and number format
        message = Change_Data.refresh() # save the actual data
        if message[0] in num_list: # checking if the station exist
            if message[1] in (0,1) and message[2] in (0,1): # checking de values of alarms (0 or 1)
                print("\nSending data from station {}: Alarm1={}  Alarm2={}\n". format(*message))
                message_str =''
                for e in message:
                    message_str = message_str + str(e) + ' '
                data = message_str.encode()
                print("connecting to ", SERVER_ADDRESS)
                s = socket.socket()
                s.connect(SERVER_ADDRESS)
                s.send(data)
                recv_data = s.recv(1024)
                recv_message = recv_data.decode()
                print(recv_message)
                s.close()
            else:
                print("Not valid value for alarms")
        else:
            print("Not autorizated station")