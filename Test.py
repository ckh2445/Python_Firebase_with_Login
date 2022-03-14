import socket
import threading
import time
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db
import select
import errno


PORT = 5050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

firebaseConfig  = { 'apiKey': "AIzaSyAWf5MiI8LzQdodfhwpGF-ZmRwshwJVaJU",
    'authDomain': "py-yolo.firebaseapp.com",
    'projectId': "py-yolo",
    'storageBucket': "py-yolo.appspot.com",
    'messagingSenderId': "632015417889",
    'appId': "1:632015417889:web:4de7a8be07cb65efeb6960",
    'measurementId': "G-DXS0MRTJ1M",
    'databaseURL' : "https://py-yolo-default-rtdb.firebaseio.com/"}

cred = credentials.Certificate("my.json")

firebase_admin.initialize_app(cred, {'databaseURL':'https://py-yolo-default-rtdb.firebaseio.com/'})
firebase = pyrebase.initialize_app(firebaseConfig)
auth2 = firebase.auth()

ref_users = db.reference('users')

email = "ckh2445@naver.com"
password = "ckh2445"
Login = auth2.sign_in_with_email_and_password(email, password)# Email, Password Check

uid = Login['localId']
#ref_users.child(Login['localId']).update({'state' : 0})

print(type(uid))
print(ref_users.get()[uid]['state'])
#user = user.uid

#data = {"uid" : user}
##ref_users.child(user).update({"State": 0})
#print(user)

#uid = user.uid
#db2.child(str(uid)).child("State").set("1")
