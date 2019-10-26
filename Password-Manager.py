import sqlite3
from hashlib import sha256

MASTERPW = "KHAN4712"

PASSWORD = input("ENTER THE MASTER PASSWORD :-")

while MASTERPW != PASSWORD:
    if MASTERPW != PASSWORD:
        print("Invalid Password\n")
        break
    
if MASTERPW == PASSWORD:
        print("WELCOME BACK SIR :)")

conn = sqlite3.connect('pass_manager.db')

def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)

def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)

    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key +'"')        
    conn.execute(command)
    conn.commit()
    return create_password(secret_key, service, admin_pass)

if MASTERPW == PASSWORD:
    try:
        conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")
    
    
    while True:
        print("\n"+ "*"*15)
        print("Commands:")
        print("Press 1 : TO Genrate a Password")
        print("Press 2 : To Get Stored Password")
        print("Press 3 : Quit")
        print("*"*15)
        input_ = input(":")

        if input_ == "3":
            break
        if input_ == "1":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password created:\n" + add_password(service, MASTERPW))
        if input_ == "2":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password:\n" +get_password(MASTERPW, service))







    