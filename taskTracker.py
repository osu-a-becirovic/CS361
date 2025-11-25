# CS 361
# Alen Becirovic
# Sprint 2 incorporate small pool microservices
import os
import json
import zmq

#
# ZMQ CONFIG
#

# global app ID
CLIENT_ID = "TaskTracker"

# microserve addresses
MS3_ZMQ_ADDRESS = "tcp://localhost:5555"
MS2_ZMQ_ADDRESS = "tcp://localhost:5556"
MS4_ZMQ_ADDRESS = "tcp://localhost:5554"

# gloobal variables for pipe
ms2_context = None
ms3_context = None
tz_context = None
# microservice sockets
user_socket = None
event_socket = None
tz_socket = None

# MS2 user global variables
current_user = None
session_token = None

# ZMQ init for MS2
def init_zmq_user():
    global ms2_context, user_socket
    if ms2_context is None:
        ms2_context = zmq.Context()
    if user_socket is None:
        user_socket = ms2_context.socket(zmq.REQ)
        user_socket.connect(MS2_ZMQ_ADDRESS)

# ZMQ init for MS3
def init_zmq_event():
    global ms3_context, event_socket
    if ms3_context is None:
        ms3_context = zmq.Context()
    if event_socket is None:
        event_socket = ms3_context.socket(zmq.REQ)
        event_socket.connect(MS3_ZMQ_ADDRESS)

# ZMQ init for MS4
def init_zmq_timezone():
    global tz_context, tz_socket
    if tz_context is None:
        tz_context = zmq.Context()
    if tz_socket is None:
        tz_socket = tz_context.socket(zmq.REQ)
        tz_socket.connect(MS4_ZMQ_ADDRESS)

# MS2 send function
def send_request(request):
    init_zmq_user()

    user_socket.send_string(json.dumps(request))
    response = user_socket.recv_string()
    return json.loads(response)

#MS3 send function
def call(object):
    init_zmq_event()

    event_socket.send_string(json.dumps(object))
    # Message Contract -- Server Reply:
    response = event_socket.recv().decode()
    return response

#MS4 send function
def timezone_call(object):
    init_zmq_timezone()

    tz_socket.send_string(json.dumps(object))
    # Message Contract -- Server Reply:
    response = tz_socket.recv().decode()
    return response

# close function for all running ZMQ pipes
def close_zmq():
    global ms2_context, ms3_context, tz_context, user_socket, event_socket, tz_socket
    
    # we check our context and sockets and close them
    if user_socket is not None:
        user_socket.close()
    if ms2_context is not None:
        ms2_context.term()

    if event_socket is not None:
        event_socket.close()
    if ms3_context is not None:
        ms3_context.term()

    if tz_socket is not None:
        tz_socket.close()
    if tz_context is not None:
        tz_context.term()

    # clear variables
    ms2_context = None
    ms3_context = None
    tz_context = None
    user_socket = None
    event_socket = None
    tz_socket = None

#
# HELPERS
#


# clearScreen function:
# uses OS to call the cls command to clear screen
def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

# banner function:
# takes argument 'title' and prints a border around it for visual acuity
def banner(title):
    print(ASCII_TITLE)
    print("=" * 64)
    print(title.center(64))
    print("=" * 64)

def promptEnter(msg: str = "Press Enter to continue."):
    input(msg)

# store tasks in local list 
tasks = []

# areYouSure function:
# helper that assigns boolean vals to y/n for quick input validation
def areYouSure(prompt):
    while True:
        answer = input(f"{prompt} (y/n) > ").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please enter 'y' or 'n'.")

# ASCII title
# source: https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type+Something+&x=none&v=4&h=4&w=80&we=false

ASCII_TITLE = r"""
  _______        _      _______             _             
 |__   __|      | |    |__   __|           | |            
    | | __ _ ___| | __    | |_ __ __ _  ___| | _____ _ __ 
    | |/ _` / __| |/ /    | | '__/ _` |/ __| |/ / _ \ '__|
    | | (_| \__ \   <     | | | | (_| | (__|   <  __/ |   
    |_|\__,_|___/_|\_\    |_|_|  \__,_|\___|_|\_\___|_|   
 
""".strip("\n")


#
# SCREENS
#

# authorizationMenu function:
# displays options to login / create an acct

def authorizationMenu():
    while True:
        clearScreen()
        banner("Task Tracker -- Authentication")
        print("1) Login")
        print("2) Create Account")
        print("3) Exit Program\n")


        choice = input("> ").strip().lower()

        if choice == "1":
            if loginScreen():
                return True

        elif choice == "2":
            createAccountScreen()
        
        elif choice == "3":
            clearScreen()
            print("Goodbye!")
            close_zmq()
            return False

        else:
            print("\nYou entered an incorrect choice. Try again.")
            promptEnter()



# createAccountScreen function:
# allows user to create an account via Microservice 2

def createAccountScreen():
    while True:
        clearScreen()
        banner("Create Account")
        print("press 'b' and enter to go back to the previous screen\n")
        
        # get info for MS2 message contract -- check inputs for back command
        username = input("Username > ").strip()
        if username.lower() == "b":
            return

        email = input("Email > ").strip()
        if email.lower() == "b":
            return

        # check that username and email are not blank
        if not username or not email:
            print("\nPlease enter both a username and an email.")
            promptEnter()
            continue
        # get password for MS2 message contract - check input for back command
        password = input("Password > ").strip()
        if password.lower() == "b":
            return
        # have user enter password again
        confirm = input("Confirm Password > ").strip()
        if confirm.lower() == "b":
            return
        # check that pass is not blank
        if not password:
            print("\nPassword cannot be empty.")
            promptEnter()
            continue
        # check that password confirm is not blank
        if password != confirm:
            print("\nPasswords do not match. Try again.")
            promptEnter()
            continue

        # Call microservice 2: create_user
        request = {
            "action": "create_user",
            "user_data": {
                "username": username,
                "email": email,
                "password": password
            }
        }

        response = send_request(request)

        if response.get("status") == "success":
            print(f"\nAccount created for user '{username}'.")
            print("You can now log in from the Login screen.")
            promptEnter()
            return
        else:
            message = response.get("message", "Unknown error.")
            print(f"\nAccount creation failed: {message}")
            if not areYouSure("Try creating an account again?"):
                return


# loginScreen function:
# allows user to login via Microservice 2
def loginScreen():
    global current_user, session_token
    
    while True:
        clearScreen()
        banner("Login")
        print("press 'b' and enter to go back to the previous screen\n")
        print("You can log in using your username and password.")

        username = input("Username > ").strip()
        if username.lower() == "b":
            return False
        
        if not username:
            print("\nPlease enter a username or email.")
            promptEnter()
            continue

        password = input("Password > ").strip()
        if password.lower() == "b":
            return False
        
        if not password:
            print("\nPlease enter a password.")
            promptEnter()
            continue

        # Call microservice 2: login
        request = {
            "action": "login",
            "credentials": {
                "username": username,
                "password": password
            }
        }
    
        response = send_request(request)

        if response.get("status") == "success":
            session_token = response.get("session_token")
            user_obj = response.get("user", {})
            current_user = user_obj.get("username", username)
            print(f"\nWelcome, {current_user}!")
            promptEnter()
            return True
        else:
            message = response.get("message", "Unknown error.")
            print(f"\nLogin failed: {message}")
            if not areYouSure("Try logging in again?"):
                return False


# deleteTaskScreen function:
# allows user to delete a task to be displayed in the task list.
def deleteTaskScreen():
    while True:
        clearScreen()
        banner("Delete Task")
        print("=" * 64)
        print()
         # display message if task list is empty
        if not tasks:
            print("No tasks to delete.\n")
        # else display saved tasks
        else:
            # print header row
            print(f"{'Line':<6} {'Task':<30} {'Added At'}")
            # print border
            print("=" * 64)
            # use enumerate() to add task number to our list items and print them
            for index, task in enumerate(tasks, start=1):
                description = task.get("description", "")
                created_at = task.get("created_at", "")
                print(f"{index:<6} {description:<30} {created_at}")
                print()

        print("=" * 64)
        print()
        print()
        print("press 'b' and enter to go back to the previous screen")
        print("\nEnter the line number of the task you want to delete.")
        choice = input("> ").strip().lower()
        if choice == "b":
            return
        
         # check for no entry
        if not choice:
            print("\nPlease enter a line number.")
            promptEnter()
            continue

        # else -- validate input is a digit
        if not choice.isdigit():
            print("\nInvalid input. Enter a single number.")
            promptEnter()
            continue

        # validate digit entry exists in list
        number = int(choice)
        if not (1 <= number <= len(tasks)):
            print("\nInvalid input. Enter a number within range of the Task List.")
            promptEnter()
            continue

        # confirm deletion
        delete_task = tasks[number -1]
        delete_description = delete_task.get("description", "")
        delete_created = delete_task.get("created_at", "")
        print(f"\nYou are about to delete:\n{number}. {delete_description} (added at {delete_created})")

        if not areYouSure("Are you sure you want to delete this item? \nThis action cannot be undone."):
            print("\n Deletion request canceled.")
            promptEnter()
            return
        
        # delete item
        tasks.pop(number - 1)
        print("\n Deleted task. \n If this was a mistake, re-add the task from the home screen.")
        promptEnter()
        return

# addTaskScreen function:
# allows user to add a task to be displayed in the task list.

def addTaskScreen():
    while True:
        clearScreen()
        banner("Add Task")
        print("=" * 64)
        print()
        print("Type your task and press Enter.")
        print("=" * 64)
        print()
        print()
        print("press 'b' and enter to go back to the previous screen")

        task = input("> ").strip()

        # check for back
        if task.lower() == "b":
            return
        
        # check for no entry
        if not task:
            print("\nPlease enter a task.")
            promptEnter()
            continue

        # call MS3
        event_call = call({
            "action": "timestamp",
            "clientID": "TaskTracker",
            "eventName": "add.task"
        })

        # get timestamp
        data = json.loads(event_call)
        timestamp = data.get("timestamp", "N/A")
        

        # else -- valid task -- save in list
        tasks.append({
            "description": task,
            "created_at": timestamp
        })
        print("\nTask added successfully.")
        promptEnter()
        

# viewTasksScreen function:
# show task list, allow for addition / deletion of tasks

def viewTasksScreen():
    while True:
        clearScreen()
        banner("View Tasks")

        # display message if task list is empty
        if not tasks:
            print("No tasks added.\n")
        # else display saved tasks
        else:
            # print header row
            print(f"{'Line':<6} {'Task':<30} {'Added At'}")
            # print border
            print("=" * 64)
            # use enumerate() to add task number to our list items and print them
            for index, task in enumerate(tasks, start=1):
                description = task.get("description", "")
                created_at = task.get("created_at", "")
                print(f"{index:<6} {description:<30} {created_at}")
                print()
        print("=" * 64)
        print("type 'add' and hit enter to add tasks.")
        print("type 'delete' and hit enter to delete tasks.")
        print()
        print("press 'b' and enter to go back to the previous screen")
        choice = input("> ").strip().lower()
        if choice == "b":
            return
        elif choice == "add":
            addTaskScreen()
            continue
        elif choice == "delete":
            deleteTaskScreen()
            continue
        elif not choice:
            continue
        else:
            print("\nInvalid input. Type 'add', 'delete' 'b', or press Enter.")
            promptEnter()

# normalizationHelper function:
# converts user defined entries into IANA format

def normalizationHelper(value):
    # remove leading & trailing chars
    value = value.strip()

    # divide string into substring removing underscores and spaces
    segment = value.replace("_", " ").split()

    # capitalize each substring
    normalized_segment = [item.capitalize() for item in segment]

    # connect substrings with underscores
    return "_".join(normalized_segment)

# settingsScreen function:
# show settings for home region
def settingsScreen():
    while True:
        clearScreen()
        banner("Settings")
        print("1) View home timezone")
        print("2) Update home timezone")
        print("3) Back\n")
        
        choice = input("> ").strip().lower()

        if choice == "1":
            # View home timezone
            clearScreen()
            banner("Home Timezone")

            request = {
                "action": "get_home",
                "clientID": "TaskTracker"
            }

            response = timezone_call(request)
            data = json.loads(response)

            if data.get("status") == 200:
                print("Your configured home timezone is:\n")
                print(f"  {data.get('timezone')}\n")
            else:
                print("Unable to fetch home timezone from service.\n")

            promptEnter()
    
        elif choice == "2":
            # Update home timezone
            while True:
                clearScreen()
                banner("Update Home Timezone")
                print("Enter timezone in IANA format (for example:)")
                print("Enter the CONTINENT part of your timezone (IANA format).")
                print("Exampl: America, Europe, Asia, Africa, Australia")
                print("\nPress 'b' and Enter to go back without changes.\n")

                continent = input("> ").strip()
                if continent.lower() == "b":
                    break

                if not continent:
                    print("\nPlease enter a continent.")
                    promptEnter()
                    continue

                clearScreen()
                banner("Update Home Timezone")
                print(f"Continent: {continent}")
                print("Enter the CITY/REGION part of your timezone (IANA format).")
                print("Examples: Los_Angeles, New_York, Berlin, Tokyo")
                print("\nPress 'b' and Enter to go back without changes.\n")

                city = input("> ").strip()
                if city.lower() == "b":
                    break

                if not city:
                    print("\nPlease enter a city/region.")
                    promptEnter()
                    continue

                # call normalization helper on inpuits
                normalized_city = normalizationHelper(city)
                normalized_continent = normalizationHelper(continent)

                tz_input = input("> ").strip()
                if tz_input.lower() == "b":
                    break

                # concatenate IANA timezone
                tz_input = f"{normalized_continent}/{normalized_city}"

                request = {
                    "action": "set_home",
                    "clientID": "TaskTracker",
                    "timezone": tz_input
                }

                response = timezone_call(request)

                clearScreen()
                banner("Update Home Timezone")

                if data.get("status") == 200:
                    print("Home timezone updated successfully.\n")
                    print(f"New timezone: {data.get('timezone')}\n")
                else:
                    print("Timezone service rejected the update. Please try again.\n")

                promptEnter()
                # return to Settings menu
                break 

        elif choice == "3" or choice == "b":
            return

        else:
            print("\nYou entered an incorrect choice. Try again.")
            promptEnter()

        



# homeMenu function:
# main loop of program -- functions as home page

def homeMenu():
    while True:
        clearScreen()
        banner("Task Tracker")
        print("1) View Tasks")
        print("2) Add Task")
        print("3) Delete Task")
        print("4) Exit Program\n")
        print("5) Settings\n")
        print()
        print("Track simple to-dos right from your terminal.")
        print("\nPress 'h' for a quick overview.\n")

        choice = input("> ").strip().lower()

        if choice == "1":
            viewTasksScreen()
        elif choice == "2":
            addTaskScreen()
        elif choice == "3":
            deleteTaskScreen()
        elif choice == "4":
            # log out of microservice 2
            # check if we have a session token
            if session_token:
                # send request to MS 2
                send_request({
                    "action": "logout",
                    "session_token": session_token
                })
            
            clearScreen()
            print("Goodbye!")
            # close pipes
            close_zmq()
            return
        elif choice == "5":
            settingsScreen()
        elif choice == "h":
            clearScreen()
            banner("Quick Overview")
            print("• View Tasks shows your list of to-do items.")
            print("• Add Task lets you add a new task.")
            print("• Delete Task removes a task you added to your list.")
            promptEnter()
            continue
        else:
            print("\nYou entered an incorrect choice. Try again.")
            promptEnter()

if __name__ == "__main__":
    if authorizationMenu():
        homeMenu()