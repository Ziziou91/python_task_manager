# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

#=====importing libraries===========
import json
import os
from datetime import date
from task import Task
from user import User

from utility_functions import color, print_line, load_json
from reports import generate_task_report, generate_user_report

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def add_task(tasks: dict, users: dict, curr_user: str) -> None:
    """Allow a user to add a new task to task.json file."""
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
    new_task = Task(task_username,
                    task_title,
                    task_description,
                    curr_user,
                    due_date_time,
                    False,
                    assigned_date)
    tasks = new_task.add_task_to_tasks(tasks)
    new_task.write_tasks_to_file("tasks.json", tasks)


def add_user(users: dict) -> None:
    """Create a new user to write to the user.json file"""

    new_username = input("New Username: ")
    # Check if provided new_username is already registered.
    while new_username in users.keys():
        print(f"""Error! {new_username} has already been registered.
              Please choose a different username.""")
        new_username = input("New Username: ")

    # Get required inputs.
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # If passwords match create new user, add to users dict and write users data to json.
    if new_password == confirm_password:
        new_user = User(new_username, new_password, [], date.today().strftime("%Y-%m-%d"))
        users = new_user.add_user_to_users(users)
        new_user.write_users_to_file("users.json", users)
        print("\nNew user added!\n")
    else:
        print("Passwords do no match")


def create_data(file_name:str, data_request:str) -> dict:
    """At startup loads tasks data from JSON file and then creates a dictionary of task objects."""
    result = {}
    data = load_json(file_name)

    if data_request == "tasks":
        for task_data in data:
            result[task_data] = Task(data[task_data]["username"],
                                     data[task_data]["title"],
                                     data[task_data]["description"],
                                     data[task_data]["assigned_by"],
                                     data[task_data]["due_date"],
                                     data[task_data]["completed"],
                                     data[task_data]["assigned_date"])
    elif data_request == "users":
        for user_data in data:
            result[user_data] = User(data[user_data]["username"],
                                     data[user_data]["password"],
                                     data[user_data]["tasks"],
                                     data[user_data]["sign_up_date"])

    return result


def edit_tasks(tasks: dict, users: dict, curr_user: str, called_from: str) -> str:
    """Take a task_id, check it can be edited, take new value and then amend task."""
    task_id = input("""if you would like to edit a task enter it's id (e.g. 00001),
                    otherwise type anything else to return to the menu: """)

    # Check user input is a valid task_id.
    if task_id in tasks:

        # Check is task is marked as complete. If so, notify user and end execution.
        if getattr(tasks[task_id], "completed"):
            print("\nERROR. Task has been marked as complete so can no longer be edited.\n")
            return

        if called_from == "view_mine":
            # If edit_tasks called from 'view_mine', user can only view and amend their tasks.
            if task_id in getattr(users[curr_user], "tasks"):
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


def write_user_to_file(users: dict) -> None:
    """Write new user to user.txt file."""
    with open("users.json", "w", encoding="UTF-8") as f:
        json.dump(users, f)
    print("User successfully added.")


def main() -> None:
    """Main function where app logic is run."""
    #===================LOAD USERS AND TASKS===================
    users = create_data("users.json", "users")
    tasks = create_data("tasks.json", "tasks")

    #===================Login Section===================
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in users:
            print("User does not exist")
            continue
        elif getattr(users[curr_user], "password") != curr_pass:
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
            add_user(users)
        elif menu == 'a':
            add_task(tasks, users, curr_user)
        elif menu == 'va':
            view_tasks(tasks, users, curr_user, "view_all")
        elif menu == 'vm':
            view_tasks(tasks, users, curr_user, "view_mine")
        elif menu == "gr":
            generate_user_report(tasks, users)
            generate_task_report(tasks)
        elif menu == 's':
            # Generate reports first. Ensures files exist and subsequent logic is using latest data.
            generate_user_report(tasks, users)
            generate_task_report(tasks)

            with open("reports/task_overview.txt", mode="w", encoding="UTF-8") as file:
                print(file.read())

            print("\n\n\n")

            with open("reports/user_overview.txt", mode="w", encoding="UTF-8") as file:
                print(file.read())

        elif menu == 'e':
            print_line()
            print(f"{'*'*30}{color.bold}Task Manager END.{color.end}{'*'*31}")
            print_line()
            exit()



        else:
            print("You have made a wrong choice, Please Try again")


# ===================EXECTUION STARTS HERE===================
if __name__ == "__main__":
    main()
