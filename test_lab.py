# Testing file for server lab
# By: Will Chau

# There are 2 users in the database
# User1: username/password is bob/bob
# User2: username/password is will/will

# There are no messages but you can send messages using the bob and will accounts.


import unittest
import sys, io, os
from collections import defaultdict
import random
import threading
import re
from flask import Flask
import testing_server

from client import Client

TEST_SERVER_ADDR="http://127.0.0.1:5000"

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

class PatchStdin(object):
    def __init__(self, value):
        self._value = value
        self._stdin = sys.stdin
    def __enter__(self):
        # Monkey-patch stdin
        sys.stdin = io.StringIO(self._value)
        return self
    def __exit__(self, typ, val, traceback):
        # Undo the monkey-patch
        sys.stdin = self._stdin

class TestServerLab(unittest.TestCase):

    def test_register(self):
        client = Client(TEST_SERVER_ADDR)
        with Capturing() as output:
            #change the line below to create a new user for testing
            with PatchStdin("will\nwill\nwill\n"):
                client.register()

        if not "Thank you for registering!" in output:
            if 'Error recieved when contacting server: 10 - User already exists. Please try again.' in output:
                msg = "User already exists. Please delete the user from the database or use a create a new user"
                self.fail(msg)

    def test_get_messages(self):
        client = Client(TEST_SERVER_ADDR)
        with Capturing() as output:
            with PatchStdin("bob\nbob\n"):
                client.get_messages()

        if not "You have messages!" in output:
            if 'Error recieved when contacting server: 12 - Authentication Failed.' in output:
                msg = "Authentication failed. Check the if the username and passwords are correct."
                self.fail(msg)
            if 'Error recieved when contacting server: 11 - User does not exist.' in output:
                msg = "The user does not exist. Create the user first."
                self.fail(msg)

    def test_send_message(self):
        client = Client(TEST_SERVER_ADDR)
        with Capturing() as output:
            with PatchStdin("bob\nbob\nwill\nhi!\n"):
                client.get_messages()

        if not "Message Sent!" in output:
            if 'Error recieved when contacting server: 12 - Authentication Failed.' in output:
                msg = "Authentication failed. Check the if the username and passwords are correct."
                self.fail(msg)

app = testing_server.create_app()
server = threading.Thread(target=app.run)
server.start()

unittest.main()

server.join()
