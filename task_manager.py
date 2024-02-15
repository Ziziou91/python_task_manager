# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
import json
import re
from datetime import datetime, date
from utility_functions import color, print_line, load_json
from draw_tasks import view_all, view_mine
from edit_task import get_task_by_id

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def reg_user(username_password: dict, users: dict) -> None:
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
        username_password[new_username] = new_password
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

def add_task(task_list: list) -> None:
    """Allow a user to add a new task to task.txt file."""
    # TODO - refactor to break out current date and append logic
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password:
        print(f"Error! {task_username} does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    new_task = create_task(task_username, task_title, task_description, due_date_time, curr_user)
    write_task_to_file(new_task, tasks)

def create_task(task_username: str, task_title: str, task_description: str, due_date_time: datetime, curr_user: str) -> dict:
    """Creates task dictionary and then returns."""
    print("curr_user", curr_user)
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

def write_task_to_file(new_task:dict, tasks: dict) -> None:
    """Adds new_task to tast_list before writing it to tasks.txt."""
    new_id = create_task_id(tasks)
    tasks[new_id] = new_task
    # TODO create write_json function, include error handling
    with open("tasks.json", "w", encoding="UTF-8") as f:
        json.dump(tasks, f)
    print("Task successfully added.")

def create_task_id(tasks: dict) -> str:
    """Finds highest current task_id, then creates a task_id for new task."""
    id_list = [int(value) for value in tasks.keys()]
    id_list_max = max(id_list)
    new_id = str(id_list_max +1)
    leading_zero_len = 5 - len(new_id)
    return f"{(("0" * leading_zero_len) + new_id)}"

def format_task_id(task_id: str) -> str:
    """Takes a user inputted task_id and formats it so it can be found in tasks.json"""
    task_id_no_punc = re.sub(r"[^\w\s]", "", task_id)
    leading_zeros_num = 5 - len(task_id_no_punc)
    return f"{'0'* leading_zeros_num}{task_id_no_punc}"

# ===================EXECTUION STARTS HERE===================

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    curr_t['assigned_by'] = task_components[6]
    curr_t['task_id'] = task_components[7]

    task_list.append(curr_t)

users = load_json("users.json")
tasks = load_json("tasks.json")


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print_line()
    print(f"{'*'*30}{color.bold}Main Menu{color.end}{'*'*31}")
    print_line()
    menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password, users)

    elif menu == 'a':
        add_task(task_list)
    
    elif menu == 'va':
        view_all(tasks)
        get_task_by_id(tasks, "va", curr_user) 


    elif menu == 'vm':
        view_mine(tasks, curr_user)
        get_task_by_id(tasks, "vm", curr_user)
        

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")