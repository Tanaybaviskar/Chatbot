import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
from googletrans import Translator
from gtts import gTTS
import wolframalpha
from requests import get
import pywhatkit as kit
import pyjokes
import newsapi
import requests
import sys
import pyautogui
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisui import Ui_JARVIS


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak (audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am Jarvis. Please tell me how may I help you")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 535)
    server. ehlo()
    server.starttls()
    server.login('tanaybaviskardpsv@gmail.com', 'dtanay@123')
    server.sendmail('tanaybaviskardpsv@gmail.com', to, content)
    server.close()

def news():
    main_url = 'https://newsapi.org/v2/everything?q=tesla&from=2021-07-01&sortBy=publishedAt&apiKey=d19972b3dae64da38f66746ddebd075d'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day=["first", "second", "third"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        print(f"today's {day[i]} news is: {head[i]}")
        speak(f"today's {day[i]} news is: {head[i]}")

def WolfRam(query):
    api_key = "7Q7GVK-GKEU33QJGH"
    requester = wolframalpha.Client(api_key)
    requested = requester.query(query)
    try:
        Answer = next(requested.results).text
        return Answer
    except:
        speak("String value is not answerable")

def Calculator(query):
    Term = str(query)
    Term = Term.replace("jarvis","")
    Term = Term.replace("plus","+")
    Term = Term.replace("minus","-")
    Term = Term.replace("divided by","/")
    Term = Term.replace("into","*")
    Term = Term.replace("multiplied by","*")
    Term = Term.replace("upon","/")

    Final = str(query)
    try:
        result = WolfRam(Final)
        speak(f"{result}")
        print(result)
    except:
        speak("String value is not answerable")

def Temp(query):
    Temp = str(query)

    Temp = Temp.replace("what is","")
    Temp = Temp.replace("jarvis","")
    Temp = Temp.replace("temperature","")
    Temp = Temp.replace("the","")
    Temp = Temp.replace("in","")
    temp_query = str(Temp)

    if 'outside' in Temp:
        i = "Temperature in vadodara"
        answer = WolfRam(i)
        speak(f"{i} is {answer}")

    else:
        j = "Temperature in " + temp_query
        answer = WolfRam(j)
        speak(f"{j} is {answer}")



class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        #it takes microphone input from the user and returns string output

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognising...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            #print(e)

            print("Say that again please...")
            return " "
        return query

    def TaskExecution(self):
        wishMe()
        while True:
            self.query = self.takeCommand().lower()
        #logic for executing tasks based on query
            if 'wikipedia' in self.query:
                speak ('Searching wikipedia...')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                #print(results)
                speak (results)

    #open statements

            elif 'open youtube' in self.query:
                webbrowser.open("youtube.com")
            elif 'open google' in self.query:
                webbrowser.open("google.com")
            elif 'open stack overflow' in self.query:
                webbrowser.open("stackoverflow.com")

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"sir, the time is {strTime}")

            elif 'weather' in self.query:
                webbrowser.open("https://www.google.com/search?authuser=1&sxsrf=ALeKk02Zx-sdEt0zrYAQf41Fec-xY3CPCg%3A1597311979559&source=hp&ei=6ws1X6b1H9zfz7sPyMKkgAk&q=weather&oq=weather&gs_lcp=CgZwc3ktYWIQARgAMg0IABCxAxCDARBGEIACMggIABCxAxCDATIICAAQsQMQgwEyCAgAELEDEIMBMgIIADICCC4yAggAMggILhDHARCjAjICCAAyAggAUPgBWKkLYMUfaABwAHgBgAHxBIgB8A6SAQswLjEuMS4xLjAuMpgBAKABAaoBB2d3cy13aXo&sclient=psy-ab")

            #elif 'how are you' in query:
                #speak("I am fine. I hope you are fine too")

    #Email

            #elif 'send an email' in query:
                #try:
                    #speak ("What should i write?")
                    #content = takeCommand()
                    #to = "tanaybaviskar@gmail.com"
                    #sendEmail(to, content)
                    #speak("Email has been sent!")
                #except Exception as e:
                    #print(e)
                    #speak("sorry i couldn't send this email")

            elif 'send an email' in self.query:
                try:
                    speak("what should i write?")
                    content = self.takeCommand().lower()
                    to = "tanaybaviskar@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent")
                except Exception as e:
                    print(e)
                    speak("sorry i couldn't deliver this email")

    #opening apps in the laptop
            elif 'open notepad' in self.query:
                npath="C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif 'open command prompt' in self.query:
                os.system("start cmd")

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP adress is {ip}")

            elif 'google' in self.query:
                speak("what do you want me search on google?")
                cm = self.takeCommand().lower()
                try:
                    from googlesearch import search
                except ImportError:
                    print("No module named 'google' found")

                # to search
                self.query = cm
                for j in search(cm, tld="co.in", num=1, stop=1, pause=2):
                    webbrowser.open(f"{j}")

            elif 'send message' in self.query:
                mummy = "+918460448586"
                speak("to whome should i send this message?")
                cm = self.takeCommand().lower()
                speak("what should i say?")
                dm = self.takeCommand().lower()
                kit.sendwhatmsg(cm, dm, 20,37)

            elif 'play songs' in self.query:
                speak("which song do you want me to play?")
                cm = self.takeCommand().lower()
                kit.playonyt(cm)

            elif "set an alarm" in self.query:
                speak("for what time should i set it?")
                i = self.takeCommand().lower()
                nm = int(datetime.datetime.now().hour)
                if nm==i:
                    kit.playonyt("shape of you")

            elif 'tell me a joke' in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif 'shutdown the system' in self.query:
                speak("Shutting down the system")
                os.system("shutdown /s /t 0")

            elif 'restart the system' in self.query:
                speak("Restarting the system")
                os.system("shutdown /r /t 0")

            elif 'news' in self.query:
                speak("Here are the latest updates")
                news()

            elif 'screenshot' in self.query or 'take a screenshot' in self.query:
                speak("taking screenshot")
                img = pyautogui.screenshot()
                speak("What should i name the screenshot file?")
                name = self.takeCommand().lower()
                img.save(f"{name}.png")
                speak("screenshot saved")

            elif 'record screen' in self.query or 'screen recorder' in self.query:

                screen_size=(1920,1080)
                fourcc=cv2.VideoWriter_fourcc(*"XVID")
                out=cv2.VideoWriter("output.avi",fourcc,20.0,(screen_size))
                cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Live", 480, 270)

                while True:
                    img=pyautogui.screenshot()
                    frame=np.array(img)
                    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    out.write(frame)
                    cv2.imshow("show",frame)
                    if cv2.waitKey(1)==ord("q"):
                        break

                cv2.destroyAllWindows()
                out.release()

            elif 'temperature' in self.query:
                Temp(self.query)

            elif 'calculate' in self.query or 'calculation' in self.query:
                Calculator(self.query)

            elif "you can quit now" in self.query:
                speak("Thanks for using me sir")
                sys.exit()

            else:
                result = WolfRam(self.query)
                speak(result)


startExecutiom = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JARVIS()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../../../Downloads/jarvisgif1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../../Downloads/jarvisgif2.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../../Downloads/jarvisgif3.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecutiom.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
