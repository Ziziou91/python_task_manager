"""User class, and eventually admin subclass, 
to contain all data and expected functionality for any user."""
from os import path
from utility_functions import write_json

class User:
    """Creates a task instance which contains all user details, such as password and assigned tasks,
    as well as required functionality."""
    def __init__(self, username:str, password:str, tasks:list, sign_up_date:str) -> None:
        self.username = username
        self.password = password
        self.tasks = tasks
        self.sign_up_date = sign_up_date


    def add_user_to_users(self, users:dict) -> dict:
        """Add this user to users dictionary."""
        users[self.username] = self
        return users


    def write_users_to_file(self, file_name, users: dict) -> None:
        """Ensures that file_name and users are valid before writing to file."""
        # Check if file_name is valid path to file that already exists
        if not path.isfile(file_name):
            return f"ERROR! - '{file_name}' is not a valid path."
        # Check if users is empty
        elif not bool(users):
            return "ERROR! - data is empty."

        else:
            # Check that the newest task in tasks has all expected properties.
            # Sufficent to only check most recent is correct on each call to write_tasks_to_file.
            # Check that most recent task has all required properties.
            required_properties = ["username", "password", "tasks", "sign_up_date"]
            prop_count = 0

            for prop in required_properties:
                if hasattr(self, prop):
                    prop_count += 1
                else:
                    return f"ERROR! property {prop} in task new is not valid."

            # Check number of properties in most recent task matches 'required_properties' length.
            if prop_count != len(required_properties):
                return "ERROR! New task does not have correct number of properties."

            # If all previous checks satisfied create users_data dictionary.
            else:
                users_data = {}
                for user in users:
                    users_data[user] = users[user].__dict__

                write_json(file_name, users_data)
                return f"tasks successfully written to {file_name}"
