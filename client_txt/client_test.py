from socket import *
import schedule

FILENAME = "status.txt"
SERVER_ADDRESS = ("127.0.0.1", 54321)


def main():
    global text, f
    while True:
        s = socket()
        print("\nconnecting to sever at {}:{}..".format(*SERVER_ADDRESS))
        try:
            s.connect(SERVER_ADDRESS)
        except ConnectionRefusedError:
            print("Connection Refused")
        except KeyboardInterrupt:
            print("For exit click and hold CRL Z!")
        else:
            print("connected.")

        try:
            f = open(FILENAME, "r")
            line1 = int(f.readline())
            line2 = int(f.readline())
            line3 = int(f.readline())
            text = "{} {} {}".format(line1, line2, line3)
        except KeyboardInterrupt:
            print("For exit click and hold CRL Z!")
            break
        except ValueError:
            print("ValueError: data in status.txt must be int or you typed incorrectly fix the data.")
            print("\nPlease enter new data to text.\nThe format need to be:\nxxx --> (for station id must "
                  "be integer) \nx   --> (for alarm 1 status, must be integer.)\nx   -->(for alarm 2 status, "
                  "must be integer.)\n")
            client_yes_or_no = input("would you like to fix the problem manually or in terminal ? ['t' for terminal or "
                                     "any key for manually] ")
            if client_yes_or_no.lower() == 't':
                station_id = input("Please enter station id: ")
                alarm_1 = input("Please enter alarm 1 status: ")
                alarm_2 = input("Please enter alarm 2 status: ")
                print("Updating new data into status.txt file...\n")
                f = open(FILENAME, "w")
                f.write('{}\n{}\n{}'.format(station_id, alarm_1, alarm_2 ))
                f.close()
            else:
                print("Trying to send data to server again..")
                break

            break
        finally:
            f.close()

        # Client handling
        print("Sending data about station to server..")
        try:
            msg = text
            s.send(msg.encode())
        except NameError:
            print("Problem with getting the right data, Might be problem with 'status.txt' data.")
        except KeyboardInterrupt:
            print("For exit click and hold CRL Z")
            break
        except BrokenPipeError:
            print("Server might be shout down!\n")
            break
        else:
            response = s.recv(1024).decode()
            print("Response from the server:")
            print(response)
            print("Closing connection\n")
            s.close()
            break


if __name__ == '__main__':
    schedule.every(5).seconds.do(main)

    while True:
        # run scheduled tasks
        try:
            schedule.run_pending()
        except KeyboardInterrupt:
            print("For exit click and hold CRL Z")
