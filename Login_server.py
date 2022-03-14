import socket
import threading
import time
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db
import select

PORT = 5050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = '203.232.193.169'
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print(type(SERVER))
cred = credentials.Certificate("my.json")

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

def handle_client(conn,addr):
    def Login_state_check(uid):
        state = ref_users.get()[uid]['state'] # user의 state를 불러옴
        
        return int(state)
            
    email = ""
    password = ""
    connected = True
    
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT) #받은 데이터의 길이 
            if msg_length:
                msg_length = int(msg_length)
                msg = str(conn.recv(msg_length).decode(FORMAT)) # 받은 데이터의 길이만큼을 문자열로 변환 
                if msg == DISCONNECTED_MESSAGE:
                    connected = False

                if msg[0:4] == "Exit": # 프로그램 종료 시 client에서 Exit: email을 server에 전송한다 그러면 raise로 except(select.error)예외를 발생시킴
                    """Login.append(str(msg[5:]))
                    if msg[5:] in Login:
                        Login.remove(str(msg[5:])) 
                        conn.close()"""
                    raise(select.error)
                    
                if email == "": # email 저장
                    if msg[0:2] == "ID":
                        email = str(msg[3:])
                        if email == "":
                            conn.send('Insert Email'.encode('utf-8'))
                            email = ""
                            password = ""

                if password == "" and email != "": #password 저장 
                    if msg[0:2] == "PW": 
                        password = str(msg[3:])
                        if password == "":
                            conn.send('Insert Password'.encode('utf-8'))
                            email = ""
                            password = ""
                    

                if email != "" and password != "": #Login 구현 
                    try:
                        
                        Login = auth2.sign_in_with_email_and_password(email, password)# Email, Password Check
                        uid = Login['localId'] # uid 확인 
                        
                        try: # user의 state를 불러오는 try 문구 
                            state = Login_state_check(uid)
                            
                            if state == 1:
                                conn.send("Already Login".encode('utf-8')) #이미 로그인중이라고 client에 전송
                                email = "" #초기화를 안시키면 DB에 state0으로 바껴 중복 로그인이 가능함
                                password = ""
                            elif state == 0:
                                state = Login_state_check(uid)
                                if state == 1:
                                    conn.send("Already Login".encode('utf-8')) #이미 로그인중이라고 client에 전송
                                    email = "" #초기화를 안시키면 DB에 state0으로 바껴 중복 로그인이 가능함
                                    password = ""
                                else:
                                    ref_users.child(uid).update({'state' : 1}) # DB에 user의 state를 업데이트
                                    conn.send("Welcome to Py-Yolo".encode('utf-8')) #client에 로그인되었다 전송
                                
                                
                        except: # user의 state를 불러오지 못하면 업데이트한다. 
                            ref_users.child(uid).update({'state' : 1}) # DB에 user의 state를 업데이트
                            conn.send("Welcome to Py-Yolo".encode('utf-8')) #client에 로그인되었다 전송 
                    except:
                        conn.send('ID or PassWord Check'.encode('utf-8'))    
                        email = ""
                        password = ""
                        
        except: #예외 발생 시 처리문 
            if email != "":
                ref_users.child(uid).update({'state' : 0})
            conn.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
            conn.close()
            break

def start():
    server.listen()
    while True:
        conn, addr = server.accept() #socket 연결을 기다림 
        thread = threading.Thread(target=handle_client,args = (conn, addr)) #socket 연결된 후 handle_cleint 함수에 conn, addr 변수를 인자로 절달한 후 Thread 생성
        thread.start() #thread 시작
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") #thread 갯수 count

if __name__ == "__main__":
    print("[STARTING] server is starting...")
    #print(SERVER)
    start() #start 함수 실행

