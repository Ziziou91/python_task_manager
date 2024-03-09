# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import json
from datetime import date
from task import Task

from utility_functions import color, print_line, load_json
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
    assigned_date = date.today().strftime("%Y-%m-%d")

    # Create new task instance, add to tasks dictionary and then write data to JSON.
    new_task = Task(task_username, task_title, task_description, curr_user, due_date_time, False, assigned_date)
    tasks = new_task.add_task_to_tasks(tasks)
    new_task.write_tasks_to_file("tasks.json", tasks)


def create_tasks(file_name:str) -> dict:
    """At startup loads tasks data from JSON file and then creates a dictionary of task objects."""
    tasks = {}
    tasks_data = load_json(file_name)

    for task_data in tasks_data:
        tasks[task_data] = Task(tasks_data[task_data]["username"], tasks_data[task_data]["title"], tasks_data[task_data]["description"], tasks_data[task_data]["assigned_by"], tasks_data[task_data]["due_date"], tasks_data[task_data]["completed"], tasks_data[task_data]["assigned_date"])

    return tasks

def edit_tasks(tasks: dict, users: dict, curr_user: str, called_from: str) -> str:
    """Take a task_id, check it can be edited, take new value and then amend task."""
    task_id = input("if you would like to edit a task enter it's id (e.g. 00001), otherwise type anything else to return to the menu: ")

    # Check user input is a valid task_id.
    if task_id in tasks:
        if called_from == "view_mine":
            # If edit_tasks called from 'view_mine', user can only view and amend their tasks.
            if task_id in users[curr_user]["tasks"]:
                print(f"\n{tasks[task_id].create_task_str(task_id, "view_all")}")
                tasks[task_id].amend_task(users, "tasks.json", tasks)

                # Draw task after it's been amended to show user changes were successful.
                print(f"\n{tasks[task_id].create_task_str(task_id, "view_all")}")
                return "Task amended."
            else:
                print(f"\n{'='*5}ERROR! task {task_id} is not assigned to you.{'='*5}")
                return "Error. Task is not assigned to you."
        elif called_from == "view_all":
            print(f"\n{tasks[task_id].create_task_str(task_id, "view_all")}")
            tasks[task_id].amend_task(users, "tasks.json", tasks)

            # Draw task after it's been amended to show user changes were successful.
            print(f"\n{tasks[task_id].create_task_str(task_id, "view_all")}")
            return "Task amended."
    else:

        return "Error. Provided task_id cannot be found."

def view_tasks(tasks: dict, users: dict, curr_user: str, called_from: str) -> None:
    """Reads tasks from task.txt file and prints all tasks to the console."""
    # TODO - break logic into functions.
    # Create menu heading. Text depends on if called_from is view_all or view_mine.
    if called_from == "view_all":
        heading_str = "All tasks"
    elif called_from == "view_mine":
        heading_str = "My tasks"
    print_line()
    print(f"{'*'*31}{color.bold}{heading_str}{color.end}{'*'*31}")
    print_line()


    for key, task in tasks.items():
        if called_from == "view_mine":
            # Check task is assigned to user when view_tasks is called from 'view_mine'.
            if getattr(task, "username") == curr_user:
                task_str = task.create_task_str(key, called_from)
                print(task_str)
                print_line()
        else:
            task_str = task.create_task_str(key, called_from)
            print(task_str)
            print_line()

    edit_tasks(tasks, users, curr_user, called_from)


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
            view_tasks(tasks, users, curr_user, "view_all")
            # TODO - change to view_tasks with argument to say if it's all or just users tasks.
        elif menu == 'vm':
            view_tasks(tasks, users, curr_user, "view_mine")
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
