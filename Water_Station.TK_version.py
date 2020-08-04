import socket
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from time import sleep
import random
from functools import partial # for the color and text change on alarms state
import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
width, heigth = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) # screen measurement
x = 0
y = 0
p = 0
pages = 0
columns=[]
rows=[]
w = width-500 # available width space
h=heigth-200 # available height space
cols_number = w%270 # number of columns
rows_number = h%200 # number of rows

# list with first position of each column and row
for c in range (0,cols_number):
    columns.append(c*270)
for r in range (0, rows_number):
    rows.append(r*200)


color = ['yellow','red','blue','green','grey','orange','violet']  # 7 colors for the background of each station
str_list=[]
st_list=[]


def create_st_list():  # list in the existing stations in text format
    st_list = []
    str_list=[]
    with sqlite3.connect("station_status.sqlite3") as conn:
        cursor_object = conn.cursor()
        cursor_object.execute('SELECT station_id FROM station_status')
        st_db = cursor_object.fetchall()
        for e in st_db:
            str_list.append(str(e[0]))
        for e in str_list:
            st_list.append(int(e))
    return st_list, str_list


# FILENAME = 'state_data.txt'
SERVER_ADDRESS = ('127.0.0.1', 54321)


class Station():
    def __init__(self,st_number,a1,a2):
        global x
        global y
        global columns
        global rows
        self.a1 = a1
        self.a2=a2
        self.st_number = st_number
        self.st_title = 'Station '+st_number
        self.station = tk.Tk()
        self.station.geometry('270x170+{}+{}'.format(columns[x],rows[y]))
        color_number = random.randrange(6) # returns a value between 0 and 6
        bg_color = color[color_number]
        self.station.configure(bg = bg_color)
        self.station.title(self.st_title)
        x += 1
        if x == 3:
            x = 0
            y += 1
            if y == 3:
                y = 0
                x = 0
                for e in range (0,3):
                    rows[e] = rows[e]+20
                for e in range (0,3):
                    columns[e] = columns[e]+20
        if rows[2]+200 > 768:
            os['state']= tk.DISABLED
            os['text']= 'MAXIMUM REACHED'
        Alarm_Button('Alarm 1', self.station, bg_color, (10, 7), self.st_number, a1)
        Alarm_Button('Alarm 2', self.station, bg_color, (80, 77), self.st_number, a2)


def create_station():
    st_list, str_list = create_st_list()
    st_number = str(len(st_list) + 1)
    Station(st_number,0,0)


def open_it(e):
    with sqlite3.connect("station_status.sqlite3") as conn:
        cursorObject = conn.cursor()
        cursorObject.execute('SELECT alarm1 FROM station_status WHERE station_id = ?', [e, ])
        a1 = cursorObject.fetchall()
        if a1 == [(1,)]:
            a1 = 1
        else:
            a1 = 0

        cursorObject.execute('SELECT alarm2 FROM station_status WHERE station_id = ?', [e, ])
        a2 = cursorObject.fetchall()
        if a2 == [(1,)]:
            a2 = 1
        else:
            a2 = 0

    Station(e, a1, a2)


def callback(combo_list):
    st_number = combo_list.get()
    if st_number == "All":
        st_number = tuple(str_list)
        for e in st_number:
            open_it(e)
    else:
        open_it(st_number)


def open_station(combo_list):
    b1['state'] = tk.DISABLED
    combo_list.place(x=20, y=652)
    combo_list.bind("<<ComboboxSelected>>", lambda x: callback(combo_list))


class Alarm_Button():
    def __init__(self, alarm_number, station, bg_color,pos, sta,al):
        self.sta = sta
        self.alarm_number = alarm_number
        self.station = station
        self.bg_color = bg_color
        self.label_pos = pos[0]
        self.button_pos = pos[1]
        a = al
        a_color = 'thistle1'
        if a == 0:
            kolor = a_color
        else:
            kolor = 'red'

        self.label = tk.Label(self.station, text=self.alarm_number)
        self.label.place(x=50, y=self.label_pos)
        self.button = tk.Button(self.station, text="{}".format(a))
        self.button["command"] = partial(self.press, self.button, self.alarm_number)
        self.button.place(x=130, y=self.button_pos)
        self.button.config(font=('Agency FB', 15))
        self.button.config(bg=kolor)
        self.label.config(font=('Agency FB', 15))
        self.label.config(bg=self.bg_color)
        update_data(self.sta, alarm_number, al)

    def press(self, btn, alr_number):
        if btn.cget("text") == '0':
            a = 1
            btn.configure(bg="red")
            btn.configure(activebackground="pink")
        else:
            a = 0
            btn.configure(bg="thistle1")
            btn.configure(activebackground="pink")

        btn.configure(text="{}".format(a))
        update_data(self.sta, alr_number, a)


def update_alarms(sta):

    with sqlite3.connect("station_status.sqlite3") as conn:
        cursor_object = conn.cursor()
        cursor_object.execute('SELECT alarm1 FROM station_status WHERE station_id = ?', [sta, ])
        a1 = cursor_object.fetchall()

        cursor_object.execute('SELECT alarm2 FROM station_status WHERE station_id = ?', [sta, ])
        a2 = cursor_object.fetchall()
    return a1, a2


def update_data(sta, al_n, val):
    a1, a2 = update_alarms(sta)
    if a2 == [(1,)]:
        a2 = 1
    else:
        a2 = 0
    if a1 == [(1,)]:
        a1 = 1
    else:
        a1 = 0
    if al_n == 'Alarm 1':
        a1 = val
    elif al_n == 'Alarm 2':
        a2 = val

    message = [str(sta), a1, a2]

    message_str = ''
    for e in message:
        message_str = message_str + str(e) + ' '
    data = message_str.encode()
    s = socket.socket()
    s.connect(SERVER_ADDRESS)
    s.send(data)
    s.close()
    sleep(0.5)
    p = int(int(sta)/15)
    show_table(p)


def show_table(p):
    with sqlite3.connect("station_status.sqlite3") as conn:
        cursorObject = conn.cursor()
        cursorObject.execute('SELECT * FROM station_status')
        rows = cursorObject.fetchall()
        rows.sort()
        columns_print(rows, p)


def columns_print(rows, p):
    # global p
    global pages
    xp = 100
    yp = 60
    cell10 = tk.Entry(ui, width=10)
    cell10.place(x=xp, y=yp - 30)
    cell10.insert(0, "Station ")
    cell20 = tk.Entry(ui, width=10)
    cell20.place(x=xp + 100, y=yp - 30)
    cell20.insert(0, "ALARM 1")
    cell30 = tk.Entry(ui, width=10)
    cell30.place(x=xp + 200, y=yp - 30)
    cell30.insert(0, "ALARM 2")

    pages = int(len(rows)/15)   # number of pages to print from zero
    last_page = len(rows) - pages*15 # number of elements on the last page
    # prepare the pages to print
    # pages with 15 elements

    rows_page = []
    if p != pages:
        for r in range ((p*15),15+(p*15)):
            rows_page.append(rows[r])
    else:
        for r in range((len(rows) - last_page), len(rows)):
            rows_page.append(rows[r])
        for r in range(len(rows),15+(p*15)):
            rows_page.append(('',0,0,0))

    print_it(rows_page)


def Next_Page():
    global p
    global pages
    p += 1
    if p == pages:
        next_page['state']= tk.DISABLED
    if p != 0:
        previous_page['state']=tk.NORMAL

    show_table(p)



def Previous_Page():
    global p
    p -= 1
    if p == 0:
        previous_page['state']= tk.DISABLED
    if p != pages:
        next_page['state']= tk.NORMAL

    show_table(p)


def print_it(rows):
    xp = 100
    yp = 60

    for x in range (0,15):
        bg1 = 'white'
        bg2 = ('red' if rows[x][2] == 1 else 'lawn green')
        bg3 = ('red' if rows[x][3] == 1 else 'lawn green')
        if rows[x][0] == '':
            bg1 = bg2 = bg3 = 'gray90'
        cell1 = tk.Entry(ui, width=10, bg = bg1)
        cell1.place(x=xp, y=yp)
        cell1.insert(0, rows[x][0])
        cell2 = tk.Entry(ui, width=10, bg = bg2)
        cell2.place(x=xp + 100, y=yp)
        cell3 = tk.Entry(ui, width=10, bg = bg3)
        cell3.place(x=xp + 200, y=yp)
        yp = yp + 30

    # print(yp) 510


if __name__ == '__main__':
    st_list, str_list = create_st_list()

    ui = tk.Tk()  # User Interface
    ui.geometry('500x700-0+0')
    ui.title('Water Status')
    txt_display = ttk.Label(ui, text='ALARM STATE').pack()
    os = ttk.Button(ui, text="OPEN NEW STATION", command=create_station)
    os.pack(side=tk.BOTTOM)
    b1 = ttk.Button(ui, text="OPEN AN EXISTING STATION", command=lambda: open_station(combo_list))
    b1.pack(side=tk.BOTTOM)
    st_num = tk.StringVar()
    str_list_expanded = str_list.copy()
    str_list_expanded.insert(0, 'All')
    combo_list = ttk.Combobox(ui, textvariable=st_num, state='readonly', values=str_list_expanded)
    combo_list.current(0)
    show_table(0)
    next_page = ttk.Button(ui, text="NEXT PAGE", command= Next_Page)
    next_page.place(x=300, y=520)
    previous_page = ttk.Button(ui, text="PREVIOUS PAGE", command= Previous_Page)
    previous_page.place(x=100, y=520)
    previous_page['state'] = tk.DISABLED
    ui.mainloop()







