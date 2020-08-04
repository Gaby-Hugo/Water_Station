import os.path as path

FILENAME = 'state_data.txt'
st_list = []  # existing water station list


def refresh():  # loading the existing data from state_data.txt in st,a1,a2
    try:
        with open(FILENAME, 'r') as f:
            st = int(f.readline())
            a1 = int(f.readline())
            a2 = int(f.readline())
    except ValueError:  # if the text was manually modified with error
        print("file corrupted, needs to be three lines with integers.The file is update to dafault")
        st = a1 = a2 = 0
        if __name__ == "__main__":
            with open(FILENAME, 'w') as f:
                f.write('{}\n{}\n{}\n'.format(st, a1, a2))
    except FileNotFoundError: # if the text was manually deleted or the name changed
        print("error:", FILENAME, "not found.")
    except PermissionError:
        print("error:", FILENAME, "not readable.")
    except OSError:
        print("error: problem with ", FILENAME)
    except:
        print("unexpected error")
        raise

    return (st, a1, a2)


if not path.exists('stations.txt'):  # if text with the numbers of the exist stations not exist yet
    f = open('stations.txt', 'w')
    f.close()
if not path.exists('state_data.txt'):  # text for the update of the state from one station
    st = a1 = a2 = '0'
    f = open('state_data.txt', 'w')
    f.write('{}\n{}\n{}\n'.format(st, a1, a2))
    f.close()
else:
    try:
        with open(FILENAME, 'r') as f: # saving the values in the text
            st, a1, a2 = refresh()
    except FileNotFoundError:
        print("error:", FILENAME, "not found.")
    except PermissionError:
        print("error:", FILENAME, "not readable.")
    except OSError:
        print("error: problem with ", FILENAME)
    except:
        print("unexpected error")
        raise


def save_stations(st_list): # saving the new stations ingresed
    try:
        with open('stations.txt', 'w') as f:
            for station in st_list:
                f.write(str(station))
    except FileNotFoundError:
        print("error:", 'stations.txt', "not found.")
    except PermissionError:
        print("error:", 'stations.txt', "not readable.")
    except OSError:
        print("Can't save the nuew station. The file is open by other user. Try later")
    except:
        print("unexpected error")
        raise


def create_st_list():  # list in the existing stations in text format
    x = 1
    with open('stations.txt', 'r') as s:  # loading de existing stations
        while x:
            x = s.readline()
            st_list.append(x)
    st_list.pop()
    return st_list

def create_num_list(st_list):   # numbers of existing station list
    num_list = []
    for e in st_list:
        num_list.append(int(e))
    return num_list

if __name__ == '__main__':

    st_list = create_st_list()
    st, a1, a2 = refresh()

    while True:
        print("""
        Data Menu:
        ---------
        0. View the actual state
        1. Set New state
        2. Update data 
        3. Add a new Station
        4. View the existing Station List
        q. Quit
        """)

        option = input("Enter your option: ").lower()

        if option == '0':
            print("Station number = {}    Alarm 1 = {}    Alarm 2 = {}".format(st, a1, a2))  # show the actual state

        elif option == '1':   # Set New state
            st_x = input("Enter the Station number: ")
            message = "The station not exist"
            if st_x.isdigit():
                for e in st_list:
                    if int(st_x) == int(e):
                        st = st_x
                        message = "The station is " + st
                print(message)

            if message != "The station not exist":
                a1_x = input("Enter the value for Alarm 1 (0/1): ")
                if a1_x == '0' or a1_x == '1':
                    a1 = int(a1_x)
                    a2_x = input("Enter the value for Alarm 2 (0/1): ")
                    if a2_x == '0' or a2_x == '1':
                        a2 = int(a2_x)
                    else:
                        print("Invalid value")
                else:
                    print("Invalid value")

                try:
                    with open(FILENAME, 'w') as f:
                        f.write('{}\n{}\n{}\n'.format(st, a1, a2))
                except OSError:
                    print("Can't save the nuew state. The file is open by other user. Try later")


        elif option == '2':   # Update data : if change made out of the program.(using text editor).
            st, a1, a2 = refresh()
            print("Station number = {}    Alarm 1 = {}    Alarm 2 = {}".format(st, a1, a2))  # state after update


        elif option == '3': # Add a new Station
            num_list = create_num_list(st_list)
            new_st = input("Enter the number for the new station: ")
            if new_st.isdigit():
                if int(new_st) in num_list:
                    print("This station exist. Choice another number")
                else:
                    st_list.append(new_st + '\n')
                    save_stations(st_list)
                    print("Added station number ", new_st)
            else:
                print("Invalid value - Enter only numbers please")

        elif option == '4': # View the existing Station List
            print ("Autorizated stations: ")
            for e in st_list:
                print(e, end='')

        elif option == 'q':
            break
        else:
            print("Error: invalid option!")
