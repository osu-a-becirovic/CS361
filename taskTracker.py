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

#viewTasksScreen function:
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
        print("press 'b' to go back to home screen")
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
        print("3) Exit\n")

        choice = input("> ").strip()
        if choice == "1":
            viewTasksScreen()
        elif choice == "3":
            clearScreen()
            print("Goodbye!")
            return
        else:
            print("\nYou entered an incorrect choice. Try again.")
            promptEnter()

if __name__ == "__main__":
    homeMenu()