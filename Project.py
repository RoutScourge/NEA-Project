import random
import tkinter as tk
import time
from math import sqrt


class ReactionTest(tk.Tk):  # Initial class which will create the frames

    def __init__(self):
        tk.Tk.__init__(self)  # As this class is a subclass of tk.Tk, this allows
        # us to inherit the methods of tk.Tk

        container = tk.Frame(self)  # Defines how all frames will look
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Creates an empty dictionary where the frames will be stored
        for F in (
                Login, SignUp, MainMenu, RoundOne, WrongAnswer, RoundTwo, RoundThree, RoundFour, RoundFive, EndScreen,
                StatsPage):
            # for loop to iterate through all classes
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame  # Stores the frame in the dictionary, with
            # the key being page_name
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame("Login")

    def show_frame(self, page_name):  # This method will show a frame when called
        frame = self.frames[page_name]
        frame.tkraise()


class Login(tk.Frame):  # Initial login page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  # When we refer to controller in this class, it means the
        # controller we took into the init method as a parameter

        label_1 = tk.Label(self, text="Welcome - Please login", font=("Helvetica Bold", 35))
        label_1.pack(side="top", fill="x", pady=5)  # Formats this text as a title

        label_2 = tk.Label(self, text="Username")
        label_2.pack(pady=10)

        entry_1 = tk.Entry(self)  # Allows the user to input their username
        entry_1.pack(pady=10)

        label_3 = tk.Label(self, text="Password")
        label_3.pack(pady=10)

        entry_2 = tk.Entry(self)  # Allows the user to input their password
        entry_2.pack(pady=10)

        sub_button = tk.Button(self, text="Submit",
                               command=lambda: Login.submit(self, controller, entry_1.get(), entry_2.get()))
        # Links to the submit method, taking the user's input for their username and password
        sub_button.pack(pady=30)

        label_4 = tk.Label(self, text="Don't have a login?")
        label_4.pack(pady=10)

        self.label_5 = tk.Label(self, text="This login is incorrect", fg="red")
        # Error message if the username is incorrect
        self.label_6 = tk.Label(self, text="This password is incorrect", fg="red")
        # Error message if the password is incorrect

        sign_button = tk.Button(self, text="SignUp",  # Creates a link to the SignUp page
                                command=lambda: controller.show_frame("SignUp"))
        sign_button.pack(pady=10)

    def submit(self, controller, username, password):  # Method to open the main menu if the login is correct

        self.label_5.pack_forget()  # Hides the error message if already shown
        self.label_6.pack_forget()  # ^^

        with open("username.txt", "r") as user:  # Opens the username file as user in read mode
            user_list = user.readlines()  # Puts the contents of the file into the list user_list

        for i in range(len(user_list)):  # To iterate through the list of usernames
            user_list[i] = user_list[i].strip("\n")  # Removes \n from all the usernames

        with open("password.txt", "r") as pass_w:  # Same file opening process as username
            pass_list = pass_w.readlines()

        for j in range(len(pass_list)):  # For loop to remove \n from all passwords
            pass_list[j] = pass_list[j].strip("\n")

        for k in range(len(user_list)):  # Iterates through for the length of user_list
            if username == user_list[k]:
                # Checks if the entered username is the current item in user_list
                if password == pass_list[k]:
                    # Checks if the entered password is the current item in pass_list
                    with open("current_user.txt", "w") as currentUser:
                        currentUser.write(user_list[k])  # Adds the user's username to the current user file
                    currentUser.close()
                    controller.show_frame("MainMenu")  # Takes the user to the main menu page

                elif password not in pass_list:
                    self.label_6.pack(pady=20)
                    # Shows the error message if the password is wrong

            elif username not in user_list:
                self.label_5.pack(pady=20)
                # Shows the error message if the username is wrong


class SignUp(tk.Frame):  # Sign-Up page, used for if the user doesn't yet have a login

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Please enter a username and password to sign up with")
        label.pack(pady=5)

        label_2 = tk.Label(self, text="Username")
        label_2.pack(pady=10)

        entry_1 = tk.Entry(self)  # User enters potential username here
        entry_1.pack(pady=10)

        label_3 = tk.Label(self, text="Password")
        label_3.pack(pady=10)

        entry_2 = tk.Entry(self)  # User enters potential password here
        entry_2.pack(pady=10)

        label_4 = tk.Label(self, text="Password again")
        label_4.pack(pady=10)

        entry_3 = tk.Entry(self)  # User should repeat their password entry here
        entry_3.pack(pady=10)

        sub_button = tk.Button(self, text="Submit",
                               command=lambda: SignUp.submit(self, controller, entry_1.get(), entry_2.get(),
                                                             entry_3.get()))
        sub_button.pack(pady=10)  # Runs submit method below when clicked

        login_button = tk.Button(self, text="Back to Login",
                                 command=lambda: controller.show_frame("Login"))
        login_button.pack(pady=10)  # Takes user back to the Login page when clicked

        self.label_5 = tk.Label(self, text="This username is taken. Please enter another one", fg="red")
        self.label_6 = tk.Label(self, text="The passwords you've entered don't match. Please retype them", fg="red")
        self.label_7 = tk.Label(self, text="Username must contain at least one letter", fg="red")
        # Error messages if the potential login doesn't comply with pre-defined rules

    def has_letters(self, input):
        return any(char.isalpha() for char in input)
        # return True if any character in the input contains a letter

    def submit(self, controller, username_entry, password_one_entry, password_two_entry):
        # This method will validate the new logins against existing ones

        with open("username.txt", "r") as user:  # Opens the username file as user in read mode
            user_list = user.readlines()  # Puts the contents of the file into the list user_list

        for i in range(len(user_list)):  # To iterate through the list of usernames
            user_list[i] = user_list[i].strip("\n")  # Removes \n from all the usernames

        with open("password.txt", "r") as pass_w:  # Same file opening process as username
            pass_list = pass_w.readlines()

        for j in range(len(pass_list)):  # For loop to remove \n from all passwords
            pass_list[j] = pass_list[j].strip("\n")

        user.close()
        pass_w.close()

        if username_entry in user_list:
            self.label_5.pack(pady=10)
            # Shows error message if potential new username already exists

        elif not self.has_letters(username_entry):
            self.label_7.pack(pady=10)
            # Shows error message if username doesn't contain at least one letter

        else:
            if password_one_entry == password_two_entry:
                user = open("username.txt", "a")
                pass_w = open("password.txt", "a")
                # Opens the username and password files in append mode
                user.write(str(username_entry) + "\n")
                pass_w.write(str(password_one_entry) + "\n")
                # Writes the new login to the correct files
                user.close()
                pass_w.close()
                with open("current_user.txt", "w") as currentUser:
                    currentUser.write(username_entry)  # Adds the user's username to the current user file
                currentUser.close()
                controller.show_frame("MainMenu")
                # Takes the user to the main menu once their new login has been made
            else:
                self.label_6.pack(pady=10)


class MainMenu(tk.Frame):  # Main Menu page, links to the start of the game and stats page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is the main menu")
        label.pack()  # Title label

        button_1 = tk.Button(self, text="Click to start the game",
                             command=lambda: MainMenu.buttonPress(self, controller, button_1, button_1))
        button_1.pack(pady=10)  # Goes to the buttonPress method below when clicked

        button_2 = tk.Button(self, text="Stats Page",
                             command=lambda: MainMenu.buttonPress(self, controller, button_2, button_1))
        button_2.pack(pady=10)

    def buttonPress(self, controller, button_clicked, button_1):

        if button_clicked == button_1:  # If the user clicks the start game button
            initialTime = time.time()  # Take the current time
            with open("time.txt", "w") as timeFile:
                timeFile.write(str(initialTime))  # Write the time to the time file
            timeFile.close()
            controller.show_frame("RoundOne")  # Start the game by going to RoundOne

        else:  # If the stat's page button is clicked
            controller.show_frame("StatsPage")  # Go to the stats page


class StatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_1 = tk.Label(self, text="Stats Page", font=("Helvetica", 20))
        label_1.pack(pady=5)

        button_1 = tk.Button(self, text="Click to see stats",
                             command=lambda: StatsPage.showStats(self, button_1))
        button_1.pack(pady=5)

        button_2 = tk.Button(self, text="Back to Main Menu",
                             command=lambda: controller.show_frame("MainMenu"))
        button_2.pack(pady=5)

    def showStats(self, button_1):  # Run when user clicks to see stats

        button_1["state"] = "disabled"

        with open("recent_scores.txt", "r") as recentScore:
            recent_score = recentScore.readlines()  # Puts the contents of the recent score file into a list
        recentScore.close()

        for i in range(len(recent_score)):
            recent_score[i] = recent_score[i].strip("\n")

        with open("current_user.txt", "r") as user:
            username = user.read()  # Gets the current users username

        user_recent = []
        for j in range(len(recent_score)):
            if recent_score[j] == username:  # Finds the user in the recent score file
                for k in range(1, 6):
                    try:
                        if not self.has_letters(recent_score[j + k]):
                            user_recent.append(recent_score[j + k])
                            # Put the users scores into the user_recent list
                        else:
                            break  # Stops once it has put them all into the list

                    except:
                        break  # Stops if it reaches the end of the recent_score list

        label_2 = tk.Label(self, text="Recent scores:", font=("Helvetica Bold", 12))
        label_2.pack(pady=5)

        label_3 = tk.Label(self, text=str(user_recent))
        label_3.pack(pady=5, padx=10)  # Shows the user their recent scores

        with open("best_scores.txt", "r") as bestScore:
            best_scores = bestScore.readlines()
        bestScore.close()  # Puts the contents of the best_scores file into a list

        for k in range(len(best_scores)):  # Removes \n from the contents of the list
            best_scores[k] = best_scores[k].strip("\n")

        user_bestScore = "N/A"  # Predefines user_bestScore so it isn't a local variable
        for m in range(len(best_scores)):
            if best_scores[m] == username:  # Finds the username in the best_scores list
                user_bestScore = best_scores[m + 1]  # Sets the variable to be the users best score

        label_5 = tk.Label(self, text="Your best score:", font=("Helvetica Bold", 12))
        label_5.pack(pady=5)

        label_6 = tk.Label(self, text=user_bestScore)
        label_6.pack(pady=5)  # Shows the user their best score

        leaderboard_temp = []
        temp = int(len(best_scores) / 2)
        for n in range(temp):  # Iterates for half the length of the list
            leaderboard_temp.append(best_scores[(2 * n) + 1])  # Append the leaderboard_temp list with just the scores
        leaderboard_temp.sort()  # Sort the list from lowest to highest

        for p in range((len(leaderboard_temp)) - 5):
            leaderboard_temp.pop()  # Removes all except the best 5 scores

        leaderboard_list = []
        for q in range(5):
            for r in range(len(best_scores)):
                if leaderboard_temp[q] == best_scores[r]:  # Searches and finds the correct score
                    leaderboard_list.append(best_scores[r - 1])  # Puts the username in the leaderboard
                    leaderboard_list.append(best_scores[r])  # Puts the score in the leaderboard

        label_7 = tk.Label(self, text="Leaderboard:", font=("Helvetica Bold", 12))
        label_7.pack(pady=5)  # Below code outputs the leaderboard to the user
        label_8 = tk.Label(self, text=(str(leaderboard_list[0]) + ": " + str(leaderboard_list[1])))
        label_9 = tk.Label(self, text=(str(leaderboard_list[2]) + ": " + str(leaderboard_list[3])))
        label_10 = tk.Label(self, text=(str(leaderboard_list[4]) + ": " + str(leaderboard_list[5])))
        label_11 = tk.Label(self, text=(str(leaderboard_list[6]) + ": " + str(leaderboard_list[7])))
        label_12 = tk.Label(self, text=(str(leaderboard_list[8]) + ": " + str(leaderboard_list[9])))
        label_8.pack(pady=5)
        label_9.pack(pady=5)
        label_10.pack(pady=5)
        label_11.pack(pady=5)
        label_12.pack(pady=5)
        label_13 = tk.Label(self, text="*Note that each user can only appear once at max*")
        label_13.pack(pady=5)

    def has_letters(self, input):
        return any(char.isalpha() for char in input)


class RoundOne(tk.Frame):  # First round of the game

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        listColour = ["red", "blue", "purple", "deeppink2", "gold2", "green", "darkorange1", "brown"]
        listWord = ["RED", "BLUE", "PURPLE", "PINK", "YELLOW", "GREEN", "ORANGE", "BROWN"]
        listPrompt = ["colour", "word"]  # Lists used to choose the colour of buttons, the word of buttons
        # and decide the prompt respectively

        promptColour = random.choice(listWord)  # Chooses the colour of the prompt
        promptWord = random.choice(listPrompt)  # Chooses whether the prompt will be a word or colour

        label_1 = tk.Label(self, text="Click the " + promptWord + " " + promptColour)
        label_1.grid(row=0, column=4)  # Displays the prompt to the user

        button_1 = tk.Button(self, text="button1", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_1, controller, promptWord, promptColour))
        button_1.grid(row=5, column=2, padx=35, pady=10)  # Top left

        button_2 = tk.Button(self, text="button2", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_2, controller, promptWord, promptColour))
        button_2.grid(row=5, column=3, padx=15, pady=10)

        button_3 = tk.Button(self, text="button3", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_3, controller, promptWord, promptColour))
        button_3.grid(row=5, column=4, padx=15, pady=10)

        button_4 = tk.Button(self, text="button4", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_4, controller, promptWord, promptColour))
        button_4.grid(row=5, column=5, padx=25, pady=10)  # Top right

        button_5 = tk.Button(self, text="button5", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_5, controller, promptWord, promptColour))
        button_5.grid(row=7, column=2, padx=35, pady=10)  # Bottom left

        button_6 = tk.Button(self, text="button6", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_6, controller, promptWord, promptColour))
        button_6.grid(row=7, column=3, padx=15, pady=10)

        button_7 = tk.Button(self, text="button7", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_7, controller, promptWord, promptColour))
        button_7.grid(row=7, column=4, padx=15, pady=10)

        button_8 = tk.Button(self, text="button8", bg="grey90",
                             command=lambda:
                             RoundOne.answer(self, button_8, controller, promptWord, promptColour))
        button_8.grid(row=7, column=5, padx=25, pady=10)  # Bottom right

        buttonList = [button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8]
        # List of the buttons, which will be used for the answer method and for getting colours

        for i in range(8):
            textColour = random.choice(listWord)
            colourColour = random.choice(listColour)
            # Randomises the colours from the lists

            # If the variables are the same colour, they
            # should be randomised until they're different
            # if statement used for most colours
            if textColour == colourColour.upper():
                while textColour == colourColour.upper():
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for pink
            elif colourColour == "deeppink2" and textColour == "PINK":
                while colourColour == "deeppink2" and textColour == "PINK":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for yellow
            elif colourColour == "gold2" and textColour == "YELLOW":
                while colourColour == "gold2" and textColour == "YELLOW":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for orange
            elif colourColour == "darkorange1" and textColour == "ORANGE":
                while colourColour == "darkorange1" and textColour == "ORANGE":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)

            # Checks the text and colour of the current button to textColour
            # and colourColour respectively
            buttonList[i].configure(text=textColour)
            buttonList[i].configure(fg=colourColour)

            # Removes the current colours from their respective lists
            listWord.remove(textColour)
            listColour.remove(colourColour)

        with open("time.txt", "r") as timeFile:
            initialTime = float(timeFile.read())
        timeFile.close()

        startTime = time.time()  # Starts a timer once the page has been formatted
        startTime = startTime - initialTime  # startTime is now the time that the round starts
        with open("time.txt", "w") as timeFile:
            timeFile.write(str(startTime))  # Writes startTime to the time file
        timeFile.close()

    def answer(self, button_clicked, controller, promptWord, promptColour):
        # This method is run if a button is clicked
        newTime = time.time()  # Takes the time for the end of the round

        text = button_clicked["text"]  # Takes the text of the clicked button
        colour = button_clicked["fg"]  # Takes the colour of the clicked button

        if promptWord == "word":  # If the prompt said to click the word
            if text == promptColour:  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:  # Opens the time file in read mode
                    startTime = float(timeFile.read())  # Takes the startTime
                roundTime = newTime - startTime  # Finds the time taken this round
                with open("round_times.txt", "w") as roundTimeFile:  # Opens the round-time file
                    roundTimeFile.write(str(roundTime) + "\n")  # Adds the round time to it
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:  # Opens the time file again
                    timeFile.write(str(newTime))  # Changes the contents to newTime
                timeFile.close()
                controller.show_frame("RoundTwo")  # Takes the user to round two

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")

        else:  # If the prompt said to click the colour
            if colour == promptColour.lower():  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "w") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundTwo")

            elif colour == "deeppink2" and promptColour == "PINK":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "w") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundTwo")

            elif colour == "gold2" and promptColour == "YELLOW":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "w") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundTwo")

            elif colour == "darkorange1" and promptColour == "ORANGE":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "w") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundTwo")

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")


class RoundTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        listColour = ["red", "blue", "purple", "deeppink2", "gold2", "green", "darkorange1", "brown"]
        listWord = ["RED", "BLUE", "PURPLE", "PINK", "YELLOW", "GREEN", "ORANGE", "BROWN"]
        listPrompt = ["colour", "word"]  # Lists used to choose the colour of buttons, the word of buttons
        # and decide the prompt respectively

        promptColour = random.choice(listWord)  # Chooses the colour of the prompt
        promptWord = random.choice(listPrompt)  # Chooses whether the prompt will be a word or colour

        label_1 = tk.Label(self, text="Click the " + promptWord + " " + promptColour)
        label_1.grid(row=0, column=4)  # Displays the prompt to the user

        button_1 = tk.Button(self, text="button1", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_1, controller, promptWord, promptColour))
        button_1.grid(row=5, column=2, padx=35, pady=10)  # Top left

        button_2 = tk.Button(self, text="button2", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_2, controller, promptWord, promptColour))
        button_2.grid(row=5, column=3, padx=15, pady=10)

        button_3 = tk.Button(self, text="button3", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_3, controller, promptWord, promptColour))
        button_3.grid(row=5, column=4, padx=15, pady=10)

        button_4 = tk.Button(self, text="button4", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_4, controller, promptWord, promptColour))
        button_4.grid(row=5, column=5, padx=25, pady=10)  # Top right

        button_5 = tk.Button(self, text="button5", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_5, controller, promptWord, promptColour))
        button_5.grid(row=7, column=2, padx=35, pady=10)  # Bottom left

        button_6 = tk.Button(self, text="button6", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_6, controller, promptWord, promptColour))
        button_6.grid(row=7, column=3, padx=15, pady=10)

        button_7 = tk.Button(self, text="button7", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_7, controller, promptWord, promptColour))
        button_7.grid(row=7, column=4, padx=15, pady=10)

        button_8 = tk.Button(self, text="button8", bg="grey90",
                             command=lambda:
                             RoundTwo.answer(self, button_8, controller, promptWord, promptColour))
        button_8.grid(row=7, column=5, padx=25, pady=10)  # Bottom right

        buttonList = [button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8]
        # List of the buttons, which will be used for the answer method and for getting colours

        for i in range(8):
            textColour = random.choice(listWord)
            colourColour = random.choice(listColour)
            # Randomises the colours from the lists

            # If the variables are the same colour, they
            # should be randomised until they're different
            # if statement used for most colours
            if textColour == colourColour.upper():
                while textColour == colourColour.upper():
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for pink
            elif colourColour == "deeppink2" and textColour == "PINK":
                while colourColour == "deeppink2" and textColour == "PINK":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for yellow
            elif colourColour == "gold2" and textColour == "YELLOW":
                while colourColour == "gold2" and textColour == "YELLOW":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for orange
            elif colourColour == "darkorange1" and textColour == "ORANGE":
                while colourColour == "darkorange1" and textColour == "ORANGE":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)

            # Checks the text and colour of the current button to textColour
            # and colourColour respectively
            buttonList[i].configure(text=textColour)
            buttonList[i].configure(fg=colourColour)

            # Removes the current colours from their respective lists
            listWord.remove(textColour)
            listColour.remove(colourColour)

        with open("time.txt", "r") as timeFile:
            initialTime = float(timeFile.read())
        timeFile.close()

        startTime = time.time()  # Starts a timer once the page has been formatted
        startTime = startTime - initialTime  # startTime is now the time that the round starts
        with open("time.txt", "w") as timeFile:
            timeFile.write(str(startTime))  # Writes startTime to the time file
        timeFile.close()

    def answer(self, button_clicked, controller, promptWord, promptColour):
        # This method is run if a button is clicked
        newTime = time.time()  # Takes the time for the end of the round

        text = button_clicked["text"]  # Takes the text of the clicked button
        colour = button_clicked["fg"]  # Takes the colour of the clicked button

        if promptWord == "word":  # If the prompt said to click the word
            if text == promptColour:  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())  # Takes the startTime
                roundTime = newTime - startTime  # Finds the time taken this round
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundThree")

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")

        else:  # If the prompt said to click the colour
            if colour == promptColour.lower():  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundThree")

            elif colour == "deeppink2" and promptColour == "PINK":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundThree")

            elif colour == "gold2" and promptColour == "YELLOW":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundThree")

            elif colour == "darkorange1" and promptColour == "ORANGE":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundThree")

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")


class RoundThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        listColour = ["red", "blue", "purple", "deeppink2", "gold2", "green", "darkorange1", "brown"]
        listWord = ["RED", "BLUE", "PURPLE", "PINK", "YELLOW", "GREEN", "ORANGE", "BROWN"]
        listPrompt = ["colour", "word"]  # Lists used to choose the colour of buttons, the word of buttons
        # and decide the prompt respectively

        promptColour = random.choice(listWord)  # Chooses the colour of the prompt
        promptWord = random.choice(listPrompt)  # Chooses whether the prompt will be a word or colour

        label_1 = tk.Label(self, text="Click the " + promptWord + " " + promptColour)
        label_1.grid(row=0, column=4)  # Displays the prompt to the user

        button_1 = tk.Button(self, text="button1", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_1, controller, promptWord, promptColour))
        button_1.grid(row=5, column=2, padx=35, pady=10)  # Top left

        button_2 = tk.Button(self, text="button2", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_2, controller, promptWord, promptColour))
        button_2.grid(row=5, column=3, padx=15, pady=10)

        button_3 = tk.Button(self, text="button3", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_3, controller, promptWord, promptColour))
        button_3.grid(row=5, column=4, padx=15, pady=10)

        button_4 = tk.Button(self, text="button4", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_4, controller, promptWord, promptColour))
        button_4.grid(row=5, column=5, padx=25, pady=10)  # Top right

        button_5 = tk.Button(self, text="button5", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_5, controller, promptWord, promptColour))
        button_5.grid(row=7, column=2, padx=35, pady=10)  # Bottom left

        button_6 = tk.Button(self, text="button6", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_6, controller, promptWord, promptColour))
        button_6.grid(row=7, column=3, padx=15, pady=10)

        button_7 = tk.Button(self, text="button7", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_7, controller, promptWord, promptColour))
        button_7.grid(row=7, column=4, padx=15, pady=10)

        button_8 = tk.Button(self, text="button8", bg="grey90",
                             command=lambda:
                             RoundThree.answer(self, button_8, controller, promptWord, promptColour))
        button_8.grid(row=7, column=5, padx=25, pady=10)  # Bottom right

        buttonList = [button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8]
        # List of the buttons, which will be used for the answer method and for getting colours

        for i in range(8):
            textColour = random.choice(listWord)
            colourColour = random.choice(listColour)
            # Randomises the colours from the lists

            # If the variables are the same colour, they
            # should be randomised until they're different
            # if statement used for most colours
            if textColour == colourColour.upper():
                while textColour == colourColour.upper():
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for pink
            elif colourColour == "deeppink2" and textColour == "PINK":
                while colourColour == "deeppink2" and textColour == "PINK":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for yellow
            elif colourColour == "gold2" and textColour == "YELLOW":
                while colourColour == "gold2" and textColour == "YELLOW":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for orange
            elif colourColour == "darkorange1" and textColour == "ORANGE":
                while colourColour == "darkorange1" and textColour == "ORANGE":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)

            # Checks the text and colour of the current button to textColour
            # and colourColour respectively
            buttonList[i].configure(text=textColour)
            buttonList[i].configure(fg=colourColour)

            # Removes the current colours from their respective lists
            listWord.remove(textColour)
            listColour.remove(colourColour)

        with open("time.txt", "r") as timeFile:
            initialTime = float(timeFile.read())
        timeFile.close()

        startTime = time.time()  # Starts a timer once the page has been formatted
        startTime = startTime - initialTime  # startTime is now the time that the round starts
        with open("time.txt", "w") as timeFile:
            timeFile.write(str(startTime))  # Writes startTime to the time file
        timeFile.close()

    def answer(self, button_clicked, controller, promptWord, promptColour):
        # This method is run if a button is clicked
        newTime = time.time()  # Takes the time for the end of the round

        text = button_clicked["text"]  # Takes the text of the clicked button
        colour = button_clicked["fg"]  # Takes the colour of the clicked button

        if promptWord == "word":  # If the prompt said to click the word
            if text == promptColour:  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())  # Takes the startTime
                roundTime = newTime - startTime  # Finds the time taken this round
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFour")

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")

        else:  # If the prompt said to click the colour
            if colour == promptColour.lower():  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFour")

            elif colour == "deeppink2" and promptColour == "PINK":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFour")

            elif colour == "gold2" and promptColour == "YELLOW":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFour")

            elif colour == "darkorange1" and promptColour == "ORANGE":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFour")

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")


class RoundFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        listColour = ["red", "blue", "purple", "deeppink2", "gold2", "green", "darkorange1", "brown"]
        listWord = ["RED", "BLUE", "PURPLE", "PINK", "YELLOW", "GREEN", "ORANGE", "BROWN"]
        listPrompt = ["colour", "word"]  # Lists used to choose the colour of buttons, the word of buttons
        # and decide the prompt respectively

        promptColour = random.choice(listWord)  # Chooses the colour of the prompt
        promptWord = random.choice(listPrompt)  # Chooses whether the prompt will be a word or colour

        label_1 = tk.Label(self, text="Click the " + promptWord + " " + promptColour)
        label_1.grid(row=0, column=4)  # Displays the prompt to the user

        button_1 = tk.Button(self, text="button1", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_1, controller, promptWord, promptColour))
        button_1.grid(row=5, column=2, padx=35, pady=10)  # Top left

        button_2 = tk.Button(self, text="button2", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_2, controller, promptWord, promptColour))
        button_2.grid(row=5, column=3, padx=15, pady=10)

        button_3 = tk.Button(self, text="button3", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_3, controller, promptWord, promptColour))
        button_3.grid(row=5, column=4, padx=15, pady=10)

        button_4 = tk.Button(self, text="button4", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_4, controller, promptWord, promptColour))
        button_4.grid(row=5, column=5, padx=25, pady=10)  # Top right

        button_5 = tk.Button(self, text="button5", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_5, controller, promptWord, promptColour))
        button_5.grid(row=7, column=2, padx=35, pady=10)  # Bottom left

        button_6 = tk.Button(self, text="button6", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_6, controller, promptWord, promptColour))
        button_6.grid(row=7, column=3, padx=15, pady=10)

        button_7 = tk.Button(self, text="button7", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_7, controller, promptWord, promptColour))
        button_7.grid(row=7, column=4, padx=15, pady=10)

        button_8 = tk.Button(self, text="button8", bg="grey90",
                             command=lambda:
                             RoundFour.answer(self, button_8, controller, promptWord, promptColour))
        button_8.grid(row=7, column=5, padx=25, pady=10)  # Bottom right

        buttonList = [button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8]
        # List of the buttons, which will be used for the answer method and for getting colours

        for i in range(8):
            textColour = random.choice(listWord)
            colourColour = random.choice(listColour)
            # Randomises the colours from the lists

            # If the variables are the same colour, they
            # should be randomised until they're different
            # if statement used for most colours
            if textColour == colourColour.upper():
                while textColour == colourColour.upper():
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for pink
            elif colourColour == "deeppink2" and textColour == "PINK":
                while colourColour == "deeppink2" and textColour == "PINK":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for yellow
            elif colourColour == "gold2" and textColour == "YELLOW":
                while colourColour == "gold2" and textColour == "YELLOW":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for orange
            elif colourColour == "darkorange1" and textColour == "ORANGE":
                while colourColour == "darkorange1" and textColour == "ORANGE":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)

            # Checks the text and colour of the current button to textColour
            # and colourColour respectively
            buttonList[i].configure(text=textColour)
            buttonList[i].configure(fg=colourColour)

            # Removes the current colours from their respective lists
            listWord.remove(textColour)
            listColour.remove(colourColour)

        with open("time.txt", "r") as timeFile:
            initialTime = float(timeFile.read())
        timeFile.close()

        startTime = time.time()  # Starts a timer once the page has been formatted
        startTime = startTime - initialTime  # startTime is now the time that the round starts
        with open("time.txt", "w") as timeFile:
            timeFile.write(str(startTime))  # Writes startTime to the time file
        timeFile.close()

    def answer(self, button_clicked, controller, promptWord, promptColour):
        # This method is run if a button is clicked
        newTime = time.time()  # Takes the time for the end of the round

        text = button_clicked["text"]  # Takes the text of the clicked button
        colour = button_clicked["fg"]  # Takes the colour of the clicked button

        if promptWord == "word":  # If the prompt said to click the word
            if text == promptColour:  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())  # Takes the startTime
                roundTime = newTime - startTime  # Finds the time taken this round
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFive")

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")

        else:  # If the prompt said to click the colour
            if colour == promptColour.lower():  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFive")

            elif colour == "deeppink2" and promptColour == "PINK":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFive")

            elif colour == "gold2" and promptColour == "YELLOW":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFive")

            elif colour == "darkorange1" and promptColour == "ORANGE":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                controller.show_frame("RoundFive")

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")


class RoundFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        listColour = ["red", "blue", "purple", "deeppink2", "gold2", "green", "darkorange1", "brown"]
        listWord = ["RED", "BLUE", "PURPLE", "PINK", "YELLOW", "GREEN", "ORANGE", "BROWN"]
        listPrompt = ["colour", "word"]  # Lists used to choose the colour of buttons, the word of buttons
        # and decide the prompt respectively

        promptColour = random.choice(listWord)  # Chooses the colour of the prompt
        promptWord = random.choice(listPrompt)  # Chooses whether the prompt will be a word or colour

        label_1 = tk.Label(self, text="Click the " + promptWord + " " + promptColour)
        label_1.grid(row=0, column=4)  # Displays the prompt to the user

        button_1 = tk.Button(self, text="button1", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_1, controller, promptWord, promptColour))
        button_1.grid(row=5, column=2, padx=35, pady=10)  # Top left

        button_2 = tk.Button(self, text="button2", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_2, controller, promptWord, promptColour))
        button_2.grid(row=5, column=3, padx=15, pady=10)

        button_3 = tk.Button(self, text="button3", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_3, controller, promptWord, promptColour))
        button_3.grid(row=5, column=4, padx=15, pady=10)

        button_4 = tk.Button(self, text="button4", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_4, controller, promptWord, promptColour))
        button_4.grid(row=5, column=5, padx=25, pady=10)  # Top right

        button_5 = tk.Button(self, text="button5", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_5, controller, promptWord, promptColour))
        button_5.grid(row=7, column=2, padx=35, pady=10)  # Bottom left

        button_6 = tk.Button(self, text="button6", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_6, controller, promptWord, promptColour))
        button_6.grid(row=7, column=3, padx=15, pady=10)

        button_7 = tk.Button(self, text="button7", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_7, controller, promptWord, promptColour))
        button_7.grid(row=7, column=4, padx=15, pady=10)

        button_8 = tk.Button(self, text="button8", bg="grey90",
                             command=lambda:
                             RoundFive.answer(self, button_8, controller, promptWord, promptColour))
        button_8.grid(row=7, column=5, padx=25, pady=10)  # Bottom right

        buttonList = [button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8]
        # List of the buttons, which will be used for the answer method and for getting colours

        for i in range(8):
            textColour = random.choice(listWord)
            colourColour = random.choice(listColour)
            # Randomises the colours from the lists

            # If the variables are the same colour, they
            # should be randomised until they're different
            # if statement used for most colours
            if textColour == colourColour.upper():
                while textColour == colourColour.upper():
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for pink
            elif colourColour == "deeppink2" and textColour == "PINK":
                while colourColour == "deeppink2" and textColour == "PINK":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for yellow
            elif colourColour == "gold2" and textColour == "YELLOW":
                while colourColour == "gold2" and textColour == "YELLOW":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)
            # elif for orange
            elif colourColour == "darkorange1" and textColour == "ORANGE":
                while colourColour == "darkorange1" and textColour == "ORANGE":
                    textColour = random.choice(listWord)
                    colourColour = random.choice(listColour)

            # Checks the text and colour of the current button to textColour
            # and colourColour respectively
            buttonList[i].configure(text=textColour)
            buttonList[i].configure(fg=colourColour)

            # Removes the current colours from their respective lists
            listWord.remove(textColour)
            listColour.remove(colourColour)

        with open("time.txt", "r") as timeFile:
            initialTime = float(timeFile.read())
        timeFile.close()

        startTime = time.time()  # Starts a timer once the page has been formatted
        startTime = startTime - initialTime  # startTime is now the time that the round starts
        with open("time.txt", "w") as timeFile:
            timeFile.write(str(startTime))  # Writes startTime to the time file
        timeFile.close()

    def answer(self, button_clicked, controller, promptWord, promptColour):
        # This method is run if a button is clicked
        newTime = time.time()  # Takes the time for the end of the round

        text = button_clicked["text"]  # Takes the text of the clicked button
        colour = button_clicked["fg"]  # Takes the colour of the clicked button

        if promptWord == "word":  # If the prompt said to click the word
            if text == promptColour:  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())  # Takes the startTime
                roundTime = newTime - startTime  # Finds the time taken this round
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                RoundFive.endRoundCalculations(self, controller)

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")

        else:  # If the prompt said to click the colour
            if colour == promptColour.lower():  # Checks if the button clicked is correct
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                RoundFive.endRoundCalculations(self, controller)

            elif colour == "deeppink2" and promptColour == "PINK":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                RoundFive.endRoundCalculations(self, controller)

            elif colour == "gold2" and promptColour == "YELLOW":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                RoundFive.endRoundCalculations(self, controller)

            elif colour == "darkorange1" and promptColour == "ORANGE":
                with open("time.txt", "r") as timeFile:
                    startTime = float(timeFile.read())
                roundTime = newTime - startTime
                with open("round_times.txt", "a") as roundTimeFile:
                    roundTimeFile.write(str(roundTime) + "\n")
                roundTimeFile.close()
                with open("time.txt", "w") as timeFile:
                    timeFile.write(str(newTime))
                timeFile.close()
                RoundFive.endRoundCalculations(self, controller)

            else:  # If the button clicked was wrong
                controller.show_frame("WrongAnswer")

    def has_letters(self, input):
        return any(char.isalpha() for char in input)
        # return True if any character in the input contains a letter

    def endRoundCalculations(self, controller):
        with open("round_times.txt", "r") as roundTimeFile:
            round_times = roundTimeFile.readlines()  # Makes a list containing the round times

        roundTotal = 0
        for i in range(len(round_times)):
            round_times[i] = round_times[i].strip("\n")  # Removes \n from all items of the list
            roundTotal += float(round_times[i])  # Adds the round times together
        score = roundTotal / 5  # Gets the average time taken per round (the users score)

        with open("best_scores.txt", "r") as bestScore:
            best_scores = bestScore.readlines()  # Puts the bestScore file contents in best_scores
        bestScore.close()
        for j in range(len(best_scores)):
            best_scores[j] = best_scores[j].strip("\n")  # Removes \n from the items

        with open("current_user.txt", "r") as currentUser:
            username = currentUser.read()  # Gets the user's username
        username = username.strip("\n")
        currentUser.close()

        new_best = False

        if username in best_scores:  # if the username is in best_scores
            for k in range(len(best_scores)):
                if best_scores[k] == username:  # Finds the username in best_scores
                    if float(best_scores[k + 1]) > score:
                        #  If the user's new score is better than their previous best score

                        best_scores[k + 1] = score  # Set the new best score to be the current score
                        new_best = True  # Sets to True as we have a new high score
                        with open("best_scores.txt", "w") as bestScore:
                            for listItem in best_scores:  # Updates the best score file
                                bestScore.write(str(listItem) + "\n")
                        bestScore.close()
                        break

        else:  # If the user isn't in the best_scores
            bestScore = open("best_scores.txt", "a")
            bestScore.write(str(username + "\n"))  # Add their username to the file
            bestScore.write(str(score) + "\n")  # Add their score to the file
            bestScore.close()

        with open("recent_scores.txt", "r") as recentScore:
            recent_score = recentScore.readlines()
        recentScore.close()  # Puts the contents of the recent score file into a list

        for q in range(len(recent_score)):
            recent_score[q] = recent_score[q].strip("\n")

        if username in recent_score:  # If the username is in the file
            for m in range(len(recent_score)):
                if recent_score[m] == username:  # If the current item is the current username
                    for n in range(1, 6):
                        try:  # Line below can sometimes produce an index error
                            if self.has_letters(recent_score[m + n]):  # If the current item is a different username
                                recentLength = len(recent_score)  # Set a variable equal to the current list length
                                recent_score.append("")  # Append the list
                                for p in range(recentLength - m):
                                    # For all the items after the other username, and the username itself
                                    recent_score[recentLength - p] = recent_score[recentLength - p - 1]
                                    # Move all the items up by one index
                                recent_score[m + 1] = str(score)  # Add in the new score
                                with open("recent_scores.txt", "w") as recentScore:
                                    for listItem in recent_score:
                                        recentScore.write(str(listItem) + "\n")  # Updates the recent_score file
                                break

                            elif n == 5 and not self.has_letters(recent_score[m + n]):
                                # If we've stored the max amount of recent scores for this user
                                recent_score[m + 5] == ""  # Delete the oldest score
                                for r in range(5):
                                    recent_score[m + 5 - r] = recent_score[m + 4 - r]  # Move the scores up one index
                                recent_score[m + 1] = score  # Add the new score
                                with open("recent_scores.txt", "w") as recentScore:
                                    for listItem in recent_score:
                                        recentScore.write(str(listItem) + "\n")  # Update the recent_scores file
                                break

                        except:
                            recent_score.append("")  # Append the list
                            for p in range(n):
                                # For all the items after the other username, and the username itself
                                recent_score[m + n - p] = recent_score[m + n - p - 1]
                                # Move all the items up by one index
                            recent_score[m + 1] = str(score)  # Add in the new score
                            with open("recent_scores.txt", "w") as recentScore:
                                for listItem in recent_score:
                                    recentScore.write(str(listItem) + "\n")  # Update the recent_scores file
                            break

        else:  # If the username isn't in the file
            with open("recent_scores.txt", "a") as recentScore:
                recentScore.write(str(username) + "\n")  # Add the username and score to the file
                recentScore.write(str(score) + "\n")

        recentScore.close()
        end = open("end_round.txt", "w")
        end.write(str(score) + "\n")  # Takes the score and new_best to the end screen
        end.write(str(new_best) + "\n")
        end.close()
        controller.show_frame("EndScreen")  # Shows the user the end screen


class WrongAnswer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_1 = tk.Label(self, text="GAME OVER", font=("Helvetica Bold", 20))
        label_1.pack(pady=5)


class EndScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_1 = tk.Label(self, text="You win!", font=("Helvetica Bold", 20))
        label_1.pack(pady=5)  # Title

        button_1 = tk.Button(self, text="Click here for results",
                             command=lambda: EndScreen.results(self, button_1))
        button_1.pack(pady=5)  # Gets the user to click for results

    def results(self, button_1):  # Method which shows results when the button is clicked

        button_1["state"] = "disabled"  # Disables the button once it's clicked

        with open("end_round.txt", "r") as end:
            temp = end.readlines()  # Sets a temp list to be the contents of the end file
            score = temp[0]  # Defines score for the EndScreen class
            new_best = temp[1]  # Defines new_best for the EndScreen class

        label_2 = tk.Label(self, text="Your score was: " + score)
        label_2.pack(pady=5)  # Shows the user their score

        if "True" in new_best:  # If this is the user's new best score
            label_3 = tk.Label(self, text="New low score!", fg="red")
            label_3.pack(pady=5)  # Tell the user it's their new best score

        with open("recent_scores.txt", "r") as recentScore:
            recent_score = recentScore.readlines()

        for i in range(len(recent_score)):  # Opens the recent score file and removes \n
            recent_score[i] = recent_score[i].strip("\n")

        user_scores = []
        square_total = 0
        for j in range(len(recent_score)):
            try:
                if self.has_letters(recent_score[j]):  # If the current item is a username
                    for k in range(1, 6):  # Iterate through 5 times from the username
                        if not self.has_letters(recent_score[j + k]):  # If the current item is a score
                            user_scores.append(recent_score[j + k])  # Add the score to the user_scores list
                            square_item = float(recent_score[j + k]) * float(
                                recent_score[j + k])  # Squares the current item
                            square_total += square_item  # Adds the squared parts together

                        else:
                            break
            except:
                break

        total = 0
        for m in range(len(user_scores)):
            total += float(user_scores[m])  # Add all recent scores together
        mean = total / len(user_scores)  # Divide by the number of scores for the mean
        square_mean = square_total / len(user_scores)  # Take the mean of the sum of squared scores
        mean_squared = mean * mean  # Square the mean
        deviation = sqrt(square_mean - mean_squared)  # Standard deviation

        lower_bound = mean - (deviation / 2)  # Determines the bounds for the next section
        upper_bound = mean + (deviation / 2)
        print(str(mean))
        print(str(lower_bound))
        print(str(upper_bound))

        score = float(score)
        if score < lower_bound:  # If the score was lower than the lower bound
            label_4 = tk.Label(self, text="That score was very good compared to others", fg="green")
        elif lower_bound <= score <= upper_bound:  # If the score was between the two bounds
            label_4 = tk.Label(self, text="That score was average compared to others", fg="orange")
        else:  # If the score was greater than the upper bound
            label_4 = tk.Label(self, text="That score wasn't good compared to others", fg="red")
        label_4.pack(pady=5)

        with open("best_scores.txt") as bestScore:
            best_scores = bestScore.readlines()  # Puts the best_scores file contents into a list

        for n in range(len(best_scores)):  # Removes \n from the contents
            best_scores[n] = best_scores[n].strip("\n")

        leaderboard_temp = []
        temp = int(len(best_scores) / 2)
        for p in range(temp):  # Iterates for half the length of the list
            leaderboard_temp.append(best_scores[(2 * p) + 1])  # Append the leaderboard_temp list with just the scores
        leaderboard_temp.sort()  # Sort the list from lowest to highest

        for q in range((len(leaderboard_temp)) - 5):
            leaderboard_temp.pop()  # Removes all except the best 5 scores

        leaderboard_list = []
        for r in range(5):
            for s in range(len(best_scores)):
                if leaderboard_temp[r] == best_scores[s]:  # Searches and finds the correct score
                    leaderboard_list.append(best_scores[s - 1])  # Puts the username in the leaderboard
                    leaderboard_list.append(best_scores[s])  # Puts the score in the leaderboard

        label_5 = tk.Label(self, text="Leaderboard:", font=("Helvetica Bold", 15))
        label_5.pack(pady=5)  # Below code outputs the leaderboard to the user
        label_6 = tk.Label(self, text=(str(leaderboard_list[0]) + ": " + str(leaderboard_list[1])))
        label_7 = tk.Label(self, text=(str(leaderboard_list[2]) + ": " + str(leaderboard_list[3])))
        label_8 = tk.Label(self, text=(str(leaderboard_list[4]) + ": " + str(leaderboard_list[5])))
        label_9 = tk.Label(self, text=(str(leaderboard_list[6]) + ": " + str(leaderboard_list[7])))
        label_10 = tk.Label(self, text=(str(leaderboard_list[8]) + ": " + str(leaderboard_list[9])))
        label_6.pack(pady=5)
        label_7.pack(pady=5)
        label_8.pack(pady=5)
        label_9.pack(pady=5)
        label_10.pack(pady=5)
        label_11 = tk.Label(self, text="*Note that each user can only appear once at max*")
        label_11.pack(pady=5)

    def has_letters(self, input):
        return any(char.isalpha() for char in input)


if __name__ == "__main__":  # Allows tkinter to run
    app = ReactionTest()
    app.mainloop()
