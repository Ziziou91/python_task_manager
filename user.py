"""User class, and eventually admin subclass, 
to contain all data and expected functionality for any user."""

class User:
    """Creates a task instance which contains all user details, such as password and assigned tasks,
    as well as required functionality."""
    def __init__(self, username:str, password:str, tasks:list, sign_up_date:str) -> None:
        self.username = username
        self.password = password
        self.tasks = tasks
        self.sign_up_date = sign_up_date
