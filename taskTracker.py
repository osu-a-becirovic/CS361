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
# flag for using home timezone
use_home_timezone = False

# microserve addresses
MS3_ZMQ_ADDRESS = "tcp://localhost:5555"
MS2_ZMQ_ADDRESS = "tcp://localhost:5556"
MS4_ZMQ_ADDRESS = "tcp://localhost:5554"
MS7_ZMQ_ADDRESS = "tcp://localhost:5552"
MS8_ZMQ_ADDRESS = "tcp://127.0.0.1:5560"

# global variables for pipe
ms2_context = None
ms3_context = None
tz_context = None
recur_context = None
notes_context = None
# microservice sockets
user_socket = None
event_socket = None
tz_socket = None
recur_socket = None
notes_socket = None

# MS2 user global variables
current_user = None
session_token = None

# ZMQ init for MS2 - secure user service
def init_zmq_user():
    global ms2_context, user_socket
    if ms2_context is None:
        ms2_context = zmq.Context()
    if user_socket is None:
        user_socket = ms2_context.socket(zmq.REQ)
        user_socket.connect(MS2_ZMQ_ADDRESS)

# ZMQ init for MS3 - calendar microservice
def init_zmq_event():
    global ms3_context, event_socket
    if ms3_context is None:
        ms3_context = zmq.Context()
    if event_socket is None:
        event_socket = ms3_context.socket(zmq.REQ)
        event_socket.connect(MS3_ZMQ_ADDRESS)

# ZMQ init for MS4 - timezone conversion microservice
def init_zmq_timezone():
    global tz_context, tz_socket
    if tz_context is None:
        tz_context = zmq.Context()
    if tz_socket is None:
        tz_socket = tz_context.socket(zmq.REQ)
        tz_socket.connect(MS4_ZMQ_ADDRESS)

# ZMQ init for MS7 - recurring events microservice
def init_zmq_recurring():
    global recur_context, recur_socket
    if recur_context is None:
        recur_context = zmq.Context()
    if recur_socket is None:
        recur_socket = recur_context.socket(zmq.REQ)
        recur_socket.connect(MS7_ZMQ_ADDRESS)

# ZMQ init for MS8 - notes microservice
def init_zmq_notes():
    global notes_context, notes_socket
    if notes_context is None:
        notes_context = zmq.Context()
    if notes_socket is None:
        notes_socket = notes_context.socket(zmq.REQ)
        notes_socket.connect(MS8_ZMQ_ADDRESS)

# MS2 send function
def send_request(request):
    init_zmq_user()

    user_socket.send_string(json.dumps(request))
    response = user_socket.recv_string()
    return json.loads(response)

# MS3 send function
def call(object):
    init_zmq_event()

    event_socket.send_string(json.dumps(object))
    # Message Contract -- Server Reply:
    response = event_socket.recv().decode()
    return response

# MS4 send function
def timezone_call(object):
    init_zmq_timezone()

    tz_socket.send_string(json.dumps(object))
    # Message Contract -- Server Reply:
    response = tz_socket.recv().decode()
    return response

# MS7 send function
def recurring_call(request):
    init_zmq_recurring()
    recur_socket.send_string(json.dumps(request))
    response = recur_socket.recv().decode()
    return response

# MS8 send function
def note_call(request):
    init_zmq_notes()
    notes_socket.send_json(request)
    response = notes_socket.recv_json()
    return response

# close function for all running ZMQ pipes
def close_zmq():
    global ms2_context, ms3_context, tz_context, user_socket, event_socket, tz_socket, recur_context, recur_socket, notes_context, notes_socket
    
    # we check our context and sockets and close them
    # MS2
    if user_socket is not None:
        user_socket.close()
    if ms2_context is not None:
        ms2_context.term()
    # MS3
    if event_socket is not None:
        event_socket.close()
    if ms3_context is not None:
        ms3_context.term()
    # MS4
    if tz_socket is not None:
        tz_socket.close()
    if tz_context is not None:
        tz_context.term()
    # MS7
    if recur_socket is not None:
        recur_socket.close()
    if recur_context is not None:
        recur_context.term()

    # MS8
    if notes_socket is not None:
        notes_socket.close()
    if notes_context is not None:
        notes_context.term()

    # clear variables
    ms2_context = None
    ms3_context = None
    tz_context = None
    recur_context = None
    user_socket = None
    event_socket = None
    tz_socket = None
    recur_socket = None
    notes_socket = None
    notes_context = None

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

# convertExistingTasksHelper function:
# helper that loops thru all existing tasks, and converts them to the home timezone
def convertExistingTasksHelper():
    if not tasks:
        return
    for item in tasks:
        utc_val = item.get("created_utc")
        local_val = convertHomeTimezone(utc_val)
        if local_val is True:
            item["created_at"] = local_val


# convertHomeTimezone function:
# fetches home timezone value and converts UTC timestamp into home timezone
def convertHomeTimezone(timestamp):
    # call microservice for home timezone
    home_response = timezone_call({
        "action": "get_home",
        "clientID": CLIENT_ID
    })

    home_data = json.loads(home_response)
    home_timezone = home_data.get("timezone")

    # call microservice to localize time
    local_response = timezone_call({
            "action": "localize",
            "timestamp": timestamp,
            "timezone": home_timezone
        })
    
    localize_data = json.loads(local_response)
    local_timestamp = localize_data.get("conversion")
    return local_timestamp

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

        display_timestamp = timestamp

        # check if home timezone flag is on
        if use_home_timezone and timestamp != "N/A":
            ## USER CONVERT HELPER
            display_timestamp = convertHomeTimezone(timestamp)
        
        recurring_flag = False
        repeat_frequency = None

        while True:   
            repeat_answer = input("\nDoes this task repeat? (y/n) > ").strip().lower()
            if repeat_answer == "y":
                recurring_flag = True
     
                while recurring_flag is True:
                    freq = input("How often? (daily/weekly/monthly) > ").strip().lower()
                    if freq in ("daily", "weekly", "monthly"):
                        repeat_frequency = freq
                        break
                    else:
                        print("Please enter 'daily', 'weekly', or 'monthly'.")
                break
            elif repeat_answer == "n":
                break
            else:
                print("Please enter 'y' or 'n'.")

        # else -- valid task -- save in list
        tasks.append({
            "description": task,
            "created_at": display_timestamp,
            "created_utc": timestamp,
            "recurring": recurring_flag,
            "repeat_frequency": repeat_frequency,
        })
        print("\nTask added successfully.")
        promptEnter()

# expandHelper function:
# calls MS7
def expandRecurringTasks():
    while True:
        clearScreen()
        banner("Expand Recurring Events")

        if not tasks:
            print("No tasks added.\n")
            promptEnter()
            return
    
        recurring_task_list = []
        print(f"{'Line':<6} {'Task':<30} {'Recurring':<10} {'Frequency'}")
        print("=" * 64)
        for index, task in enumerate(tasks, start=1):
            description = task.get("description", "")
            recurring = task.get("recurring", False)
            frequency = task.get("repeat_frequency") or "-"
            flag = "Yes" if recurring else "No"
            print(f"{index:<6} {description:<30} {flag:<10} {frequency}")
            if recurring:
                recurring_task_list.append(index)
        print()

        if not recurring_task_list:
            print("You have no recurring tasks to expand.\n")
            promptEnter()
            return
    
        print("Enter the line number of a recurring task to expand,")
        print("or press 'b' and Enter to go back.\n")
        choice = input("> ").strip().lower()

        if choice == "b":
            return

        if not choice.isdigit():
            print("\nPlease enter a valid line number.")
            promptEnter()
            continue

        number = int(choice)
        if number not in recurring_task_list:
            print("\nPlease select a line number for a recurring task.")
            promptEnter()
            continue

        selected = tasks[number - 1]
        start_utc = selected.get("created_utc")
        frequency = selected.get("repeat_frequency")

    # Ask for end date
        while True:
            clearScreen()
            banner("Expand Recurring Events")
            print(f"Task: {selected.get('description', '')}")
            print(f"Start (UTC): {start_utc}")
            print(f"Frequency: {frequency}")
            print("\nEnter the END date for expansion in ISO format (YYYY-MM-DD).")
            print("Press 'b' and Enter to go back.\n")

            end_input = input("> ").strip()
            if end_input.lower() == "b":
                return

            if not end_input:
                print("\nPlease enter a date.")
                promptEnter()
                continue

            # Build request for Recurring Event Service (MS7)
            request = {
                "action": "expand_event",
                "start_date": start_utc,
                "frequency": frequency,
                "end_date": end_input
            }

            response_text = recurring_call(request)
            response = json.loads(response_text)

            clearScreen()
            banner("Recurring Instances")

            status = response.get("status")
            if status != 200:
                print("Recurring Event Service returned an error:\n")
                print(f"Status: {status}")
                print(f"Error: {response.get('error', 'Unknown error')}\n")
                promptEnter()
                return

            instances = response.get("instances", [])
            if not instances:
                print("No occurrences found in the requested date range.\n")
            else:
                print("Upcoming occurrences:\n")
                for idx, instance in enumerate(instances, start=1):
                    print(f"{idx}. {instance}")
                print()

            promptEnter()
            return

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
        print("type 'expand' and hit enter to see recurring instances.")
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
        elif choice == "expand":
            expandRecurringTasks()
            continue
        elif not choice:
            continue
        else:
            print("\nInvalid input. Type 'add', 'delete', 'expand', 'b', or press Enter.")
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
    global use_home_timezone
    while True:
        clearScreen()
        banner("Settings")
        # show toggle for timezone
        if use_home_timezone:
            status = "ON"
        else:
            status = "OFF"
        print(f"Home timezone status: {status}\n")


        print("1) Toggle home timezone on/off")
        print("2) View home timezone")
        print("3) Update home timezone")
        print("4) Back\n")
        
        choice = input("> ").strip().lower()

        if choice == "1":
            # turn flag on/off
            if use_home_timezone:
                if areYouSure("Turn OFF home timezone to use UTC timestamps for tasks?"):
                    use_home_timezone = False
            else:
                if areYouSure("Turn ON home timezone for task timestamps?"):
                    use_home_timezone = True
                    if tasks and areYouSure("Convert existing tasks to your home timezone now?"):
                        convertExistingTasksHelper()
                        print("\nExisting tasks have been converted to your home timezone.")
                        promptEnter()
            continue 

        if choice == "2":
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
    
        elif choice == "3":
            # Update home timezone
            while True:
                clearScreen()
                banner("Update Home Timezone")
                print("Enter the CONTINENT part of your timezone.")
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
                print("Enter the CITY/REGION part of your timezone.")
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
                    print(f"New timezone: {tz_input}\n")
                else:
                    print("Timezone service rejected the update. Please try again.\n")

                promptEnter()
                # return to Settings menu
                break 

        elif choice == "4" or choice == "b":
            return

        else:
            print("\nYou entered an incorrect choice. Try again.")
            promptEnter()

#notesScreen function:asdf
# show shows add/delete/view for Notes microservice
def notesScreen():
    while True:
        clearScreen()
        banner("Notes")

        print("1) View all notes")
        print("2) View a note by ID")
        print("3) Add a note")
        print("4) Delete a note")
        print("5) Back\n")

        choice = input("> ").strip().lower()
        if choice == "1":
            clearScreen()
            banner("All Notes")
            response = note_call({"command": "show_all"})
            # check for notes
            if not response:
                print("No notes found.\n")
            else:
                # print table
                print(f"{'ID':<6} {'Note'}")
                print("=" * 64)
                # iterate through notes array and print notes
                for note_id, note_text in response.items():
                    print(f"{note_id:<6} {note_text}")
                print()
            promptEnter()

        elif choice == "2":
            clearScreen()
            banner("View Note")
            print("Enter the Note's ID to view.")
            print("Press 'b' and Enter to go back.\n")
            note_id_input = input("> ").strip().lower()
            # validate input -- exit out if b
            if note_id_input == "b":
                continue
            if not note_id_input.isdigit():
                print("\nPlease enter a numeric ID.")
                promptEnter()
                continue

            note_id = int(note_id_input)
            # call notes microservice -- get note
            response = note_call({
                "command": "get_note",
                "id": note_id
            })

            print()
            print(f"ID:   {response.get('id')}")
            print(f"Note: {response.get('note')}\n")
            promptEnter()

        elif choice == "3":
            clearScreen()
            banner("Add Note")
            print("Add your note and press Enter.")
            print("Press 'b' and Enter to go back.\n")
            # validate input
            note_id_input = input("> ").strip()
            if note_id_input.lower() == "b":
                continue
            if not note_id_input:
                print("\nPlease enter a note.")
                promptEnter()
                continue
            # call notes microservice -- add
            response = note_call({
                "command": "add",
                "note": note_id_input
            })
            note_id = response.get("id")
            print(f"\nNote added with ID {note_id}.")
            promptEnter()

        elif choice == "4":
            clearScreen()
            banner("Delete Note")
            print("Enter the ID of the note you want to delete.")
            print("Press 'b' and Enter to go back.\n")

            note_id_input = input("> ").strip().lower()
            # validate numerical input / back
            if note_id_input == "b":
                continue
            if not note_id_input.isdigit():
                print("\nPlease enter a number for ID.")
                promptEnter()
                continue
            note_id = int(note_id_input)
            # confirm delete
            if not areYouSure(f"Do you really want to delete {note_id}? This cannot be undone."):
                print("\nOperation canceled.")
                promptEnter()
                continue
            response = note_call({
                "command": "delete",
                "id": note_id
            })
            print()
            print(f"\nNote with ID {note_id} deleted.")
            promptEnter()

        elif choice == "5" or choice == "b":
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
        print("4) Notes\n") 
        print("5) Settings")
        print("6) Exit Program\n")
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
            notesScreen()
        elif choice == "5":
            settingsScreen()
        elif choice == "6":
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
        elif choice == "h":
            clearScreen()
            banner("Quick Overview")
            print("• View Tasks shows your list of to-do items.")
            print("• Add Task lets you add a new task.")
            print("• Delete Task removes a task you added to your list.")
            print("• View Settings lets you view and change your home region.")
            print("• View Notes lets you add, delete, and view Notes you set.")
            promptEnter()
            continue
        else:
            print("\nYou entered an incorrect choice. Try again.")
            promptEnter()

if __name__ == "__main__":
    if authorizationMenu():
        homeMenu()