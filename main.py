import sys
import os
import platform

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.daily import run_daily
from src.ref import run_ref

def print_menu():
    print("=== Menu ===")
    print("1. Auto chat (daily)")
    print("2. Auto reff")
    print("3. Exit")
    print("==============")

def run_auto_chat():
    print("Running Auto Chat (daily)...")
    run_daily()

def run_auto_reff():
    print("Running Auto Reff...")
    run_ref()

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')

def main():
    clear()
    while True:
        print_menu()
        choice = input("Please choose an option: ")

        if choice == "1":
            run_auto_chat()
        elif choice == "2":
            print('Not Available')
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
