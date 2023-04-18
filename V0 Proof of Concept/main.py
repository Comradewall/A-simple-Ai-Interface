import sys
import os
import threading

import openai

from PyQt5.QtGui import QBrush, QImage, QPalette, QPixmap, QColor
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMenu,QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize

#Global Variables

openai.api_key = ""

messages = [
    {"role": "system", "content": ""},
]

#The chatbot function it prompts the AI with what it is and what its function is. In the new version we installed a response logger, it is bad but if it works.

LoggerDateSet = 0

def chatbot(input):
    def Logger(input, filename,setState):
         import datetime 
         date = datetime.datetime.now()
         with open('log.txt', 'w', encoding="utf-8") as f:
            if (setState == 1):
                f.write(input)
                f.write("\n")
            else:
                f.write(str(date))
                f.write("\n")
                f.write(input)
                f.write("\n")
                setState = 1
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        Logger(reply,"log.txt",LoggerDateSet)

        return reply
    
def StartWebInterface():

    import gradio as gr

    print("Web Interface is assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running Web Interface: {}".format(os.getpid()))

    #Implementation with gradio as an example may integrate gtts later

    inputs = gr.inputs.Textbox(lines=7, label="Chat with AI")
    outputs = gr.outputs.Textbox(label="Reply")

    gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title="AI Chatbot",
        description="Ask anything you want",
        theme="compact").launch(share=True) 
        
    CommandSucessState = 1
    return CommandSucessState
    

class MainAIWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(1000,500))
        self.setWindowTitle("AI Communications Panel")

        font = self.font()
        font.setPointSize(20)
        
        BackgroundImage = QImage("background.png")
        ScaledBackground = BackgroundImage.scaled(QSize(1000,500))
        AppPallette = QPalette()
        AppPallette.setBrush(QPalette.Window, QBrush(ScaledBackground))
        self.setPalette(AppPallette)
            
def ExitApplication():
    sys.exit()

#Control Panel(Main GUI Elmenets)
def ControlWindow(WebIfThread):
    class ControlPanel(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)

            self.w = None

            self.setMinimumSize(QSize(1000,500))
            self.setWindowTitle("AI Control Panel")

            TitleFont = self.font()
            TitleFont.setPointSize(20)

            TextFont = self.font()
            TextFont.setPointSize(13)
        
            BackgroundImage = QImage("background.png")
            ScaledBackground = BackgroundImage.scaled(QSize(1000,500))
            AppPallette = QPalette()
            AppPallette.setBrush(QPalette.Window, QBrush(ScaledBackground))
            self.setPalette(AppPallette)

            self.WindowTitle = QLabel(self)
            self.WindowTitle.setText("AI Control Panel")
            self.WindowTitle.setFont(TitleFont)
            self.WindowTitle.adjustSize()
            self.WindowTitle.move(410,10)

            MainMenu = QMenu(self)
            MainMenu.addAction("Start Interface", WebIfThread)
            MainMenu.addAction("Start Local Interface", self.StartLocalInterface)
            MainMenu.addAction("Quit",ExitApplication)

            self.MenuButton = QPushButton("Main Menu",self)
            self.MenuButton.setMenu(MainMenu)
            self.MenuButton.move(10,5)

            self.AiOptionsLabel = QLabel(self)
            self.AiOptionsLabel.setFont(TextFont)
            self.AiOptionsLabel.setText("AI Options:")
            self.AiOptionsLabel.adjustSize()
            self.AiOptionsLabel.move(5,50)
            
            self.AiOptions = QLineEdit(self)
            self.AiOptions.setText(str(messages[0]))
            self.AiOptions.adjustSize()
            self.AiOptions.move(100,50)

        #Simple interface to start a new window in PyQt5 (Inspiration: PyQt5_WeatherApp)

        def StartLocalInterface(self):
            if self.w is None:
                self.w = MainAIWindow()
            self.w.show()    

    if __name__ =="__main__":
        app = QtWidgets.QApplication(sys.argv)
        mainWin = ControlPanel()
        mainWin.show()
        sys.exit(app.exec_())

 #Main Function

def Main():
    if __name__ == "__main__":

        print("Main Process is assigned to thread: {}".format(threading.current_thread().name))
        print("ID of process running the Main Process: {}".format(os.getpid()))

        def StartWebThread():
            WebIfThread = threading.Thread(target=StartWebInterface, name="WebIfThread")
            WebIfThread.start()
            return WebIfThread
    
        ControlWindow(StartWebThread)

Main()


