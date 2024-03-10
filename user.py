"""User class, and eventually admin subclass, 
to contain all data and expected functionality for any user."""
from os import path

class User:
    """Creates a task instance which contains all user details, such as password and assigned tasks,
    as well as required functionality."""
    def __init__(self, username:str, password:str, tasks:list, sign_up_date:str) -> None:
        self.username = username
        self.password = password
        self.tasks = tasks
        self.sign_up_date = sign_up_date


    def write_users_to_file(self, file_name, users: dict) -> None:
        """Ensures that file_name and users are valid before writing to file."""
        # Check if file_name is valid path to file that already exists
        if not path.isfile(file_name):
            return f"ERROR! - '{file_name}' is not a valid path."
        # Check if tasks is empty
        elif not bool(users):
            return "ERROR! - data is empty."
        
        pass
