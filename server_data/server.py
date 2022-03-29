import datetime
import sqlite3
from socket import *

CREAT_TABLE = """CREATE TABLE IF NOT EXISTS station_status (
                                                station_id INT,
                                                last_date TEXT,
                                                alarm1 INT,
                                                alarm2 INT,
                                                PRIMARY KEY(station_id));"""

INSERT_STATION_STATUS = """INSERT OR REPLACE INTO station_status
                          (station_id, last_date, alarm1, alarm2)
                          VALUES (?, ?, ?, ?);"""


def connect():
    """
    connect to database
    :return: qlite3.connect("data.sqlite")
    """
    return sqlite3.connect("data.sqlite")


def create_table(fconnection):
    """
    Creat table
    :param fconnection:
    :return: none
    """
    with fconnection:
        fconnection.execute(CREAT_TABLE)


def add_station(fconnection, fstation_id, flast_date, falarm1, falarm2):
    """
    Add/update station to database
    :param fconnection:
    :param fstation_id:
    :param flast_date:
    :param falarm1:
    :param falarm2:
    :return: none
    """
    with fconnection:
        fconnection.execute(INSERT_STATION_STATUS, (fstation_id, flast_date, falarm1, falarm2))
        fconnection.commit()


if __name__ == '__main__':
    global client
    # SQLITE3
    connection = connect()
    create_table(connection)
    # SOCKETS
    accept_socket = socket()
    try:
        accept_socket.bind(('127.0.0.1', 54321))
        print("\nserver online!")
        accept_socket.listen(4)
        while True:
            try:
                client, address = accept_socket.accept()
                print("Server waiting for new data...\n")
            except BlockingIOError:
                pass
            except KeyboardInterrupt:
                pass
            except OSError:
                print("Client {}:{} connection failed!".format(*client.getpeername()))
            else:
                print("trying to update new data incoming from:{} at time: {}".format(address, datetime.datetime.now().strftime(
                    '%Y-%m-%d '
                    '%H:%M:%S')))

            # for each client:
            try:
                data = client.recv(1024)
                txt = data.decode()
                txt = txt.split()
                last_date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                station_id = int(txt[0])
                alarm1 = int(txt[1])
                alarm2 = int(txt[2])
                add_station(connection, station_id, last_date, alarm1, alarm2)
            except BlockingIOError:
                pass
            except (IndexError, OSError):
                print("\nProblem might be KeyboardInterrupt or might be problem with 'status.txt' data.\nfor exit "
                      "please click and hold CRL Z close terminal and run again.")
            except NameError:
                print("\nClient not connected please check client connection\n or if you wish to exit press CRL Z")
            else:
                print("Data updated successfully!")
                client.send("Data updated successfully!".encode())
    finally:
        accept_socket.close()
