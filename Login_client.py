import base64
from PyQt5.QtWidgets import (QApplication,QWidget, QPushButton, QLabel, QLineEdit, QGridLayout,QMessageBox,QMainWindow) 
from PyQt5 import  QtGui,QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import sys 
import socket
import atexit

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = '192.168.0.2'
ADDR = (SERVER,PORT)
 
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

ID = ""
PW = ""

stylesheet_Btn = ("color: #dc3545;"
                    "border-color: #dc3545;"
                    "background-color: whitesmoke;"
                    "border-radius: 10px;")

stylesheet_Back = ("background-color: pink;"
                    "QAbstractScrollArea.background:white;")

stylesheet_Label = ("border: 2px solid white;"
                    "color: #5B2386;"
                    "border-radius: 10px;")

def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)

class game_Form(QWidget):
    def __init__(self):
        super().__init__()
        global ID,PW
        self.setStyleSheet(stylesheet_Back)
        self.setWindowTitle('game_Form')
        #self.resize(400,150)
        self.setFixedSize(400,180)

        layout = QGridLayout()

        #----------------------------------ID----------------------------------#
        label_ID = QLabel('<font size="4"> Email </font>')
        label_ID.setFixedWidth(110)
        label_ID.setFixedHeight(25)
        label_ID.setAlignment(Qt.AlignCenter)
        label_ID.setFont(QtGui.QFont("Consolas"))
        label_ID.setStyleSheet("color: black;"
                            "border-style: solid;"
                            "background-color: white;"
                            "border-width: 1px;"
                            "border-color: black;"
                            "border-radius: 3px")
        self.lineEdit_ID = QLineEdit()
        self.lineEdit_ID.setFixedWidth(250)
        self.lineEdit_ID.setFixedHeight(25)
        self.lineEdit_ID.setStyleSheet("color: black;"
                                "border-style: solid;"
                                "background-color: white;"
                                "border-width: 1px;"
                                "border-color: black;"
                                "border-radius: 3px")

        self.lineEdit_ID.setPlaceholderText('Please enter your Email')
        self.lineEdit_ID.setFont(QtGui.QFont("Consolas"))

        layout.addWidget(label_ID, 0, 0)
        layout.addWidget(self.lineEdit_ID, 0, 1)

        #----------------------------------PASSWORD----------------------------------#
        label_password = QLabel('<font size="4">Password </font>')
        label_password.setAlignment(Qt.AlignCenter)
        label_password.setFont(QtGui.QFont("Consolas"))
        label_password.setFixedWidth(110)
        label_password.setFixedHeight(25)
        label_password.setStyleSheet("color: black;"
                            "border-style: solid;"
                            "background-color: #c6c6c6;"
                            #"border-style: dashed;"
                            "border-width: 1px;"
                            "border-color: black;"
                            "border-radius: 3px")
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setFixedWidth(250)
        self.lineEdit_password.setFont(QtGui.QFont("Consolas"))
        self.lineEdit_password.setFixedHeight(25)
        self.lineEdit_password.setStyleSheet("color: black;"
                                "background-color: #c6c6c6;"
                                #"border-style: dashed;"
                                "border-width: 1px;"
                                "border-color: black;"
                                "border-radius: 3px")
        self.lineEdit_password.setPlaceholderText('Please enter your Password')

        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        #----------------------------------Login----------------------------------#
        button_login = QPushButton('Login')
        button_login.setFixedHeight(30)
        #button_login.setFixedWidth(250)
        button_login.setFont(QtGui.QFont("Consolas"))
        button_login.clicked.connect(self.Check_Login)
        button_login.setStyleSheet("color: white;"
                                "background-color: black;"
                                #"border-style: dashed;"
                                #"border-width: 1px;"
                                "border-color: white;"
                                "font-size: 16px;"
                                "border-radius: 3px")
        layout.addWidget(button_login, 2, 0,1,2)
        #layout.setRowMinimumHeight(2, 75)5 

        self.setLayout(layout)

    def Check_Login(self):
        self.msg = QMessageBox()
        ID = self.lineEdit_ID.text()
        PW = self.lineEdit_password.text()
        send("ID:" + str(ID)) #server ??????
        send("PW:" + str(PW)) #server ??????
        recv = client.recv(2048).decode(FORMAT)

        if recv == 'Welcome to Py-Yolo':
            self.msg.setWindowTitle('Result')
            self.msg.setText(recv)
            self.msg.exec_()
        
        else:
            self.msg.setWindowTitle('Result')
            self.msg.setText(recv)
            self.msg.exec_()
		
    def get_ID(self):
        return self.lineEdit_ID.text()

class Login_Form(QWidget): 
    def __init__(self,game_form:QWidget):
        super().__init__()
        global ID,PW
        self.setStyleSheet(stylesheet_Back)
        self.setWindowTitle('pylo_Login')
        #self.resize(400,150)
        self.setFixedSize(400,180)

        layout = QGridLayout()

        #----------------------------------ID----------------------------------#
        self.label_ID = QLabel('<font size="4"> Email </font>')
        self.label_ID.setFixedWidth(110)
        self.label_ID.setFixedHeight(25)
        self.label_ID.setAlignment(Qt.AlignCenter)
        #self.label_ID.setFont(QtGui.QFont("Consolas"))
        self.label_ID.setFont(QtGui.QFont("Consolas",weight=QtGui.QFont.Bold))
        #self.label_ID.setFont(QtGui.QFont.setBold(True))
        # label_ID.setStyleSheet("color: black;"
        #                     "border-style: solid;"
        #                     "background-color: white;"
        #                     "border-width: 1px;"
        #                     "border-color: black;"
        #                     "border-radius: 3px")
        self.label_ID.setStyleSheet(stylesheet_Label)
        self.lineEdit_ID = QLineEdit()
        self.lineEdit_ID.setFixedWidth(250)
        self.lineEdit_ID.setFixedHeight(25)
        # self.lineEdit_ID.setStyleSheet("color: black;"
        #                         "border-style: solid;"
        #                         "background-color: white;"
        #                         "border-width: 1px;"
        #                         "border-color: black;"
        #                         "border-radius: 3px")
        self.lineEdit_ID.setStyleSheet(stylesheet_Btn)
        self.lineEdit_ID.setPlaceholderText('Please enter your Email')
        self.lineEdit_ID.setFont(QtGui.QFont("Consolas"))

        layout.addWidget(self.label_ID, 0, 0)
        layout.addWidget(self.lineEdit_ID, 0, 1)

        #----------------------------------PASSWORD----------------------------------#
        self.label_password = QLabel('<font size="4">Password </font>')
        self.label_password.setAlignment(Qt.AlignCenter)
        self.label_password.setFont(QtGui.QFont("Consolas",weight=QtGui.QFont.Bold))
        self.label_password.setFixedWidth(110)
        self.label_password.setFixedHeight(25)
        # label_password.setStyleSheet("color: black;"
        #                     "border-style: solid;"
        #                     "background-color: #c6c6c6;"
        #                     #"border-style: dashed;"
        #                     "border-width: 1px;"
        #                     "border-color: black;"
        #                     "border-radius: 3px")
        self.label_password.setStyleSheet(stylesheet_Label)
        
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setFixedWidth(250)
        self.lineEdit_password.setFont(QtGui.QFont("Consolas"))
        self.lineEdit_password.setFixedHeight(25)
        # self.lineEdit_password.setStyleSheet("color: black;"
        #                         "background-color: #c6c6c6;"
        #                         #"border-style: dashed;"
        #                         "border-width: 1px;"
        #                         "border-color: black;"
        #                         "border-radius: 3px")
        self.lineEdit_password.setStyleSheet(stylesheet_Btn)
        self.lineEdit_password.setPlaceholderText('Please enter your Password')

        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        #----------------------------------Login----------------------------------#
        self.button_login = QPushButton('Login')
        self.button_login.setFixedHeight(30)
        #button_login.setFixedWidth(250)
        self.button_login.setFont(QtGui.QFont("Consolas"))
        
        self.button_login.clicked.connect(self.Check_Login)
        # button_login.setStyleSheet("color: white;"
        #                         "background-color: black;"
        #                         #"border-style: dashed;"
        #                         #"border-width: 1px;"
        #                         "border-color: white;"
        #                         "font-size: 16px;"
        #                         "border-radius: 3px")
        self.button_login.setStyleSheet(stylesheet_Btn)
        layout.addWidget(self.button_login, 2, 0,1,2)
        #layout.setRowMinimumHeight(2, 75)5 
        self.button_login.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setLayout(layout)

    def Check_Login(self):
        self.msg = QMessageBox()
        ID = self.lineEdit_ID.text()
        PW = self.lineEdit_password.text()
        send("ID:" + str(ID)) #server ??????
        send("PW:" + str(PW)) #server ??????
        recv = client.recv(2048).decode(FORMAT)

        if recv == 'Welcome to Py-Yolo':
            self.msg.setWindowTitle('Result')
            self.msg.setText(recv)
            self.msg.exec_()
            self.close()
            game_form.show()
            
        elif recv == "ID or PassWord Check":
            self.lineEdit_ID.setText("")
            self.lineEdit_password.setText("")
            self.msg.setText(recv)
            self.msg.exec_()
        else:
            self.msg.setWindowTitle('Result')
            self.msg.setText(recv)
            self.msg.exec_()
            
		
    def get_ID(self):
        return self.lineEdit_ID.text()

def exit2():
	global ID,PW
	ID = Login_form.get_ID()
	send("Exit:" + str(ID))
	ID = ""
	PW = ""
	client.shutdown() #?????? ????????? ?????? 


atexit.register(exit2)

if __name__ == '__main__':
    #exec(base64.b64decode(my_code))

    app = QApplication(sys.argv)
    game_form = game_Form()
    Login_form  = Login_Form(game_form)

    Login_form.show()
    #Chating_form.show()
    #Test = Signup_Form()
    #Test.show()


    sys.exit(app.exec_())