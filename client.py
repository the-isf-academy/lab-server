import requests, time, sys, json, getpass

from view import TerminalView

DEFAULT_MSG_SERVER = '127.0.0.1:5000'

#error codes
SUCCESS = "1"
USER_EXISTS_IN_DB = "10"
PASSWORD_INCORRECT = "11"
USER_PASS_INCORRECT = "12"

class Client():

    def __init__(self, server_address):
        '''
        message: the message sent to the server
        mode: s for sending a message to a person, g for getting messages, u for showing users
        server_address: server IP address
        '''
        authenticated = False
        user = ''
        self.server_address = server_address
        self.view = TerminalView()

        choices = ["Register a New User", "Send a Message", "Get Your Messages", "Quit"]
        choice = self.view.menu_choice(choices)
        while True:
            if choice == 0:
                self.register()

            else:
                if self.authenticate() == True:
                    if choice == 1:
                        self.send_message()
                    elif choice == 2:
                        self.get_messages()
                    else:
                        pass
                else:
                    self.view.error(USER_PASS_INCORRECT, 'Username/password is incorrect')
            break


    def set_user(self, user):
        self.user = user

    def send_message(self):
        # Post the message to the server
        recipient = input('Who do you want to send your message to? ')
        message = input('What is your message? ')
        send_address = self.server_address + "/"
        payload = {"sender": self.user, "message": message, "recipient": recipient, "timestamp": time.time()}
        r = requests.post(send_address, json=payload)
        if r.ok:
            self.view.success('Message Sent')
        else:
            self.view.error(r.status_code, r.reason)

    def get_messages(self):
        ''' Gets the user's messages '''

        get_address = self.server_address + "/get_messages"
        payload = {"username": self.user}
        r = requests.get(get_address, json=payload)
        if r.ok:
            response_content = r.json()
            messageList = response_content['messages']
            self.view.display(messageList)
        else:
            self.view.error(r.status_code, r.reason)
        pass

    def register(self):
        '''Gets a username and password (with a password verification) and sends it to the server'''

        user = input('Enter a username: ')
        password = getpass.getpass(prompt='Enter your password')
        confirm = getpass.getpass(prompt='Enter your password again')

        if password == confirm:
            register_address = self.server_address + "/register"
            payload = {"username": user, "password": password}
            r = requests.post(register_address, json=payload)
            if r.ok:
                if str(r.content, encoding='utf-8') == USER_EXISTS_IN_DB:
                    self.error(USER_EXISTS_IN_DB, "User already exists. Please try again.")
                    return USER_EXISTS_IN_DB
                else:
                    self.view.success("Thank you for registering!")
                    return SUCCESS

            else:
                self.error(r.status_code, r.reason)
                return r.status_code

        else:
            print("The password incorrect. Please try again.")


    def authenticate(self):
        ''' Gets a username and password and sends it to the server'''

        username = input('Enter a username: ')
        password = getpass.getpass(prompt='Enter your password: ')
        auth_address = self.server_address + "/auth"
        payload = {"username": username, "password": password}
        r = requests.get(auth_address, json=payload)
        if str(r.content, encoding='utf-8') == PASSWORD_INCORRECT:
            return False
        else:
            self.set_user(username)
            return True

def set_up_client():
    server_address = input("What server would you like to use? (default, return) ")
    if server_address == "":
        server_address = DEFAULT_MSG_SERVER
    if server_address.find("http://") == -1 and server_address.find("https://") == -1:
        server_address = "http://" + server_address
    #mode = str(sys.argv[1])
    c = Client(server_address)

if __name__ == "__main__":
    set_up_client()
