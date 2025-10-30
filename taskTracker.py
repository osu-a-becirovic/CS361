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


def prompt_enter(msg: str = "Press Enter to continue."):
    input(msg)
# homeMenu function:
# main loop of program -- functions as home page

def homeMenu():
    while True:
        clearScreen()
        banner("Task Tracker")
        print("3) Exit\n")

        choice = input("> ").strip()


        if choice == "3":
            clearScreen()
            print("Goodbye!")
            return
        else:
            print("\nYou entered an incorrect choice. Try again.")
            prompt_enter()

if __name__ == "__main__":
    homeMenu()