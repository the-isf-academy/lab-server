import requests
import time
import sys
import json
from sqlalchemy.ext.serializer import loads
import getpass

DEFAULT_MSG_SERVER = '127.0.0.1:5000'

#error codes
SUCCESS = "1"
USER_EXISTS_IN_DB = "10"
PASSWORD_INCORRECT = "11"

class Client():

    def __init__(self, server_address, mode):
        '''
        message: the message sent to the server
        mode: s for sending a message to a person, g for getting messages, u for showing users
        server_address: server IP address
        '''
        authenticated = False
        user = ''
        self.server_address = server_address

        if mode == 'new':
            self.register()
        else:
            if self.authenticate() == True:
                if mode == 'send':
                    self.send_message()
                elif mode == 'get':
                    self.get_messages()
                else:
                    pass
            else:
                print('No selected mode')

    def set_user(self, username):
        self.user = username
        return self.user

    def get_user(self):
        return self.user

    def set_server(self, address):
        self.server_address = address
        return self.server_address

    def send_message(self):
        # Post the message to the server
        recipent = input('Who do you want to send your message to?')
        message = input('What is your message?')
        send_address = self.server_address + "/"
        payload = {"sender": self.user, "message": message, "recipent": recipent, "timestamp": time.time()}
        r = requests.post(send_address, json=payload)
        if r.ok:
            print('Message Sent')
        else:
            self.error(r.status_code, r.reason)

    def get_messages(self):
        get_address = self.server_address + "/get_messages"
        payload = {"user": self.user}
        r = requests.post(get_address, json=payload)
        if r.ok:
            deserialized = loads(r.content)
            for message in deserialized:
                mTime = time.ctime(message.timestamp)
                print(f"{mTime}")
                print(f"From: {message.sender}")
                print(message.message)
        else:
            self.error(r.status_code, r.reason)
        pass

    def register(self):
        user = input('Enter a username: ')
        password = getpass.getpass(prompt='Enter your password')
        confirm = getpass.getpass(prompt='Enter your password again')
        if password == confirm:
            register_address = self.server_address + "/register"
            payload = {"user": user, "password": password}
            r = requests.post(register_address, json=payload)
            if r.ok:
                if str(r.content, encoding='utf-8') == USER_EXISTS_IN_DB:
                    print("User already exists. Please try again.")
                else:
                    print("Thank you for registering!")
            else:
                self.error(r.status_code, r.reason)
        else:
            print("The password incorrect. Please try again.")

    def authenticate(self):
        user = input('Enter a username: ')
        password = getpass.getpass(prompt='Enter your password: ')
        auth_address = self.server_address + "/auth"
        payload = {"user": user, "password": password}
        r = requests.post(auth_address, payload)
        if str(r.content, encoding='utf-8') == PASSWORD_INCORRECT:
            return False
        else:
            self.set_user(user)
            return True

    def error(self, status_code, reason):
        print("Error recieved when contacting server: {} - {}\n".format(status_code, reason))

    def show_users(self):
        show_users_address = self.server_address + "/users"
        pass

def set_up_client():
    server_address = input("What server would you like to use? (default, return) ")
    if server_address == "":
        server_address = DEFAULT_MSG_SERVER
    if server_address.find("http://") == -1 and server_address.find("https://") == -1:
        server_address = "http://" + server_address
    mode = str(sys.argv[1])
    c = Client(server_address, mode)

if __name__ == "__main__":
    set_up_client()
