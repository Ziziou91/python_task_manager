# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import json
import re
from datetime import datetime, date
from task import Task

from utility_functions import color, print_line, load_json, create_task_due_date
from draw_tasks import view_mine
from reports import generate_task_report, generate_user_report


DATETIME_STRING_FORMAT = "%Y-%m-%d"


def reg_user(users: dict) -> None:
    """Create a new user to write to the user.txt file"""
    new_username = input("New Username: ")
    while new_username in users.keys():
        print(f"Error! {new_username} has already been registered. Please choose a different username.")
        new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    user_type = input("User type - admin or user: ")
    while user_type != "admin" and user_type != "user":
        print(f"Error! {user_type} is not a valid user type.")
        user_type = input("User type - admin or user?")
    if new_password == confirm_password:
        print("New user added")
        users[new_username] = {
            "password" : new_password,
            "role" : user_type,
            "tasks" : [],
            "sign_up_date" : date.today().strftime(DATETIME_STRING_FORMAT)
        }
        write_user_to_file(users)
    else:
        print("Passwords do no match")

def write_user_to_file(users: dict) -> None:
    """Write new user to user.txt file."""
    with open("users.json", "w", encoding="UTF-8") as f:
        json.dump(users, f)
    print("User successfully added.")

def add_task(tasks: dict, users: dict, curr_user: str) -> None:
    """Allow a user to add a new task to task.txt file."""
    # Get all the required user inputs.
    task_username = input("Name of person assigned to task: ")
    while task_username not in users.keys():
        print(f"Error! {task_username} does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    due_date_time = input("Due date in the following format 'YYYY-MM-DD': ")
    
    # Create new task instance, add to tasks dictionary and then write data to JSON.
    new_task = Task(task_username, task_title, task_description, curr_user, due_date_time, False)
    tasks = new_task.add_task_to_tasks(tasks)
    new_task.write_tasks_to_file("tasks.json", tasks)

def create_task(task_username: str, task_title: str, task_description: str, due_date_time: datetime, curr_user: str) -> dict:
    """Creates task dictionary and then returns."""
    curr_date = date.today()
    task = {
    "username": task_username,
    "title": task_title,
    "description": task_description,
    "due_date": due_date_time.strftime(DATETIME_STRING_FORMAT),
    "assigned_date": curr_date.strftime(DATETIME_STRING_FORMAT),
    "completed": False,
    "assigned_by": curr_user,
    }
    return task

def create_tasks(file_name:str) -> dict:
    """Loads tasks data from JSON file and then creates a dictionary of task objects."""
    tasks = {}
    tasks_data = load_json(file_name)

    for task_data in tasks_data:
        tasks[task_data] = Task(tasks_data[task_data]["username"], tasks_data[task_data]["title"], tasks_data[task_data]["description"], tasks_data[task_data]["assigned_by"], tasks_data[task_data]["due_date"], tasks_data[task_data]["completed"])

    return tasks


def view_all(tasks: list) -> None:
    """Reads tasks from task.txt file and prints all tasks to the console."""
    print_line()
    print(f"{'*'*31}{color.bold}All tasks{color.end}{'*'*31}")
    print_line()
    for key, task in tasks.items():
        task_str = task.create_task_str(key, "view_all")
        print(task_str)
        print_line()

def main() -> None:
    """Main function where app logic is run."""
    #===================LOAD USERS AND TASKS===================
    users = load_json("users.json")
    tasks = create_tasks("tasks.json")
    
    #===================Login Section===================
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in users.keys():
            print("User does not exist")
            continue
        elif users[curr_user]["password"] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
    
    
    while True:
        # Presents menu to the user and takes input.
        print_line()
        print(f"{'*'*30}{color.bold}Main Menu{color.end}{'*'*31}")
        print_line()
        menu = input('''Select one of the following options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    s - Stastics
    e - Exit
    : ''').lower()
    
        # Routes input to desired logic.
        if menu == 'r':
            reg_user(users)
        elif menu == 'a':
            add_task(tasks, users, curr_user)
        elif menu == 'va':
            view_all(tasks)
            # TODO - Wait to see if user would like to edit a task
        elif menu == 'vm':
            view_mine(tasks, curr_user)
            # TODO - Wait to see if user would like to edit a task
        elif menu == "gr":
            generate_user_report(tasks, users)
            generate_task_report(tasks)
        elif menu == 'ds' and curr_user == 'admin':
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            num_users = len(users)
            num_tasks = len(tasks)

            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")

# ===================EXECTUION STARTS HERE===================

if __name__ == "__main__":
    main()
