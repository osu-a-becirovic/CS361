# CS 361
# Alen Becirovic
# Sprint 1 View, Create, Delete Implementation
import os

# clearScreen function:
# uses OS to call the cls command to clear screen
def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

# banner function:
# takes argument 'title' and prints a border around it for visual acuity
def banner(title):
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
            print(f"{'Line':<6} Task")
            # print border
            print("=" * 64)
            # use enumerate() to add task number to our list items and print them
            for index, task in enumerate(tasks, start=1):
                print(f"{index:<6} {task}")
                print()
        print("=" * 64)
        print()
        print()
        print("press 'b' and enter to go back to home screen")
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
        print(f"\nYou are about to delete:\n{number}. {tasks[number-1]}")
        if not areYouSure("Are you sure you want to delete this item?"):
            print("\n Deletion request canceled.")
            promptEnter()
            return
        
        # delete item
        tasks.pop(number - 1)
        print("\n Deleted task")
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
        print("press 'b' and enter to go back to home screen")

        task = input("> ").strip()

        # check for back
        if task.lower() == "b":
            return
        # check for no entry
        if not task:
            print("\nPlease enter a task.")
            promptEnter()
            continue
        # else -- valid task -- save in list
        tasks.append(task)
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
            print(f"{'Line':<6} Task")
            # print border
            print("=" * 64)
            # use enumerate() to add task number to our list items and print them
            for index, task in enumerate(tasks, start=1):
                print(f"{index:<6} {task}")
                print()
        print("=" * 64)
        print()
        print()
        print("press 'b' and enter to go back to home screen")
        choice = input("> ").strip().lower()
        if choice == "b":
            return



# homeMenu function:
# main loop of program -- functions as home page

def homeMenu():
    while True:
        clearScreen()
        banner("Task Tracker")
        print("1) View Tasks")
        print("2) Add Task")
        print("3) Delete Task")
        print("4) Exit\n")

        choice = input("> ").strip()
        if choice == "1":
            viewTasksScreen()
        elif choice == "2":
            addTaskScreen()
        elif choice == "3":
            deleteTaskScreen()
        elif choice == "4":
            clearScreen()
            print("Goodbye!")
            return
        else:
            print("\nYou entered an incorrect choice. Try again.")
            promptEnter()

if __name__ == "__main__":
    homeMenu()