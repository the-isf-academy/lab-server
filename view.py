# view.py
# Author: Emma Brown
# ==================

#from rgb import RGBLight
import time

class TerminalView:
    """ Creates a TerminalView object which displays the TriviaGame in
        terminal.
    """

    def menu_choice(self, choices):
        print("Here's what you can do:")
        for i in range(len(choices)):
            print("({}) {}".format(i, choices[i]))
        print("")
        choice = ""
        while True:
            choice = input("What would you like to do? ")
            try:
                choice = int(choice)
                if choice >= 0 and choice <= len(choices)-1:
                    break
            except:
                print("Please enter a number from 0 to {}.".format(len(choices) - 1))
        return choice

    def display(self, messageList):
        for message in messageList:
            print("===============================================")
            print(f"From: {message['sender']} ({time.ctime(message['timestamp'])})")
            print("-----------------------------------------------")
            print(message["message"])
            print("")

    def success(self, reason):
        print(reason)

    def error(self, status_code, reason):
        print("Error recieved when contacting server: {} - {}\n".format(status_code, reason))

    def end(self):
        return

class PiView(TerminalView):
    """ Extend the TerminalView to implent a PiView which displays LED feedback
        through the Raspberry Pi GPIO hardware.
    """

    def __init__(self):
        self.rgb = RGBLight(11,13,15)
        self.rgb.gpioSetUp()
        #self.rgb.setLightStrength(5)

    def correct_annswer(self):
        """ Flashed the LED green for half a second.
        """
        super().correct_answer()
        # WRITE CODE FOR PART F HERE
        pass

    def wrong_answer(self):
        """ Flashed the LED red for half a second.
        """
        super().wrong_answer()
        # WRITE CODE FOR PART F HERE
        pass

    def error(self, status_code, reason):
        """ Flashes out the status code in morse code
        """
        super().error(status_code, reason)
        # WRITE CODE FOR PART F HERE


    def end_game(self):
        """ Turns off and cleans up the LED component at the end of the game.
        """
        self.rgb.light_off()
