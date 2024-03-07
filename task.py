"""Task class to contain all data and expected functionality for any task."""
from datetime import date
from os import path
from utility_functions import color, difference_between_dates, write_json

class Task:
    """Each instance will include all task details, as well functionality."""
    def __init__(self, username: str, title:str, description:str, assigned_by:str, due_date_str:str, completed:bool) -> None:
        self.username = username
        self.title = title
        self.description = description
        self.due_date = self.create_due_date(due_date_str).strftime("%Y-%m-%d")
        self.assigned_date = date.today().strftime("%Y-%m-%d")
        self.assigned_by = assigned_by
        self.completed = completed

    def add_task_to_tasks(self, tasks:dict) -> dict:
        """Add this task to tasks dictionary.
        Creates task_id by finding current max task_id in tasks and adding 1."""
        task_id_list = [int(task_id) for task_id in tasks.keys()]
        new_task_id = str(max(task_id_list) + 1)
        leading_zero_len = 5 - len(new_task_id)
        new_task_id = f"{(("0" * leading_zero_len) + new_task_id)}"

        tasks[new_task_id] = self
        return tasks


    def amend_task(self, users:dict) -> None:
        """Gets a user input, validates and then sets coresponding attribute."""
        new_value = self.amend_task_get_user_input(users)

        setattr(self, new_value["property"], new_value["data"])
        return new_value["property"]

    def amend_task_get_user_input(self, users:dict) -> dict:
        """Walks user through a menu or options to edit task. 
        Returns a dictionary with the property to change and new value."""
        # Create 'completed_switch' variable to dynamically represent status of
        # 'completed' in upcoming input prompt.
        completed_switch = "complete"
        if  self.completed:
            completed_switch = "incomplete"
        
        print(f"\n{color.bold}Edit Task.{color.end}")
        menu = input(f"""Select what you would like to edit:
\tm - Mark task as {completed_switch}
\tt - Edit title
\td - Edit description
\tu - Change assigned user
\ta - Amend due date
""").lower()
        
        # Take user's 'menu' input, check it's valid. If not, ask again.
        valid_inputs = {"m": f"Mark task as {completed_switch}", "t": "Edit title", "d": "Edit description", "u" : "changed assigned user - must be a valid username", "a": "amend due date - must be in format 'YYYY-MM-DD'"}
        while True:
            if menu in valid_inputs:
                break
            else:
                print(f"ERROR! {menu} is not a valid input.")
                menu = input("Please select what you would like to edit: ")
        print(f"\n{valid_inputs[menu]}")
        new_data = input("\nPlease enter new value: ")

        # =====new_data validation and formatting.=====
        # Username validation - check user (new_data) is in user.
        if menu == "u":
            while True:
                if new_data not in users:
                    print(f"ERROR! {new_data} is not a user.")
                    new_data = input("\nPlease enter a valid username.")
                else:
                    break
        # Due date validation.
        elif menu == "a":
            new_data = self.create_due_date(new_data)
        # Completed logic - flip bool
        elif menu == "m":
            new_data = not self.completed

        task_properties = {"m": "completed", "t": "title", "d": "description", "u" : "username", "a": "due_date"}
        return {"property": task_properties[menu], "data": new_data}

    def create_due_date(self, due_date_str) -> date:
        """takes a due_date_str (format 'YYYY-MM-DD') and returns a date object"""
        while True:
            try:
                date.fromisoformat(due_date_str)
            except ValueError:
                print("ERROR! Incorrect format. Needs to be 'YYYY-MM-DD'.")
                due_date_str = input("\nEnter date string: ")
            else:
                break

        due_date_list = [int(val) for val in due_date_str.split("-")]
        return date(*due_date_list)


    def create_task_id(self, tasks:dict) -> str:
        """Finds highest current task_id in tasks, then creates unique task_id for current task."""
        if not tasks:
            return "00001"
        else:    
            task_id_list = [int(task_id) for task_id in tasks.keys()]
            max_task_id = max(task_id_list)
            new_task_id = str(max_task_id +1)
    
            # Create the desired string format (e.g. 00005) for task_id and return.
            leading_zero_len = 5 - len(new_task_id)
            return f"{(("0" * leading_zero_len) + new_task_id)}"


    def create_task_line(self, title: str, num: int, length: int=70) -> str:
        """Create a line of a given length that includes title and num."""
        num_str = str(num)
        spacing = length - (len(title) + len(num_str))
        return f"{title + (" "*spacing) + num_str}\n"


    def create_task_str(self, key:str, called_from: str) -> str:
        """Builds task_str to be printed in the terminal."""    
        # Get all required dates, including how long left until deadline.
        current_date = date.today()
        due_date = self.create_due_date(self.due_date)
        days_left = difference_between_dates(current_date, due_date)
        due_date_line = self.create_task_line(f"Due: {due_date}", days_left, 79)

        # Build task_str, adding information until ready to return.
        task_str = f"{color.bold}{self.create_task_line(self.title, key)}{color.end}"
        task_str += f"{self.description}\n\n"
        task_str += f"{due_date_line}\n"

        # Assigned_by string only includes assigned_to if this function is called from 'view_all'.
        # If called from 'view_mine', the fact it's assigned to the current user is implied.
        assigned_by = f"Assigned by: {self.assigned_by}"
        if called_from == "view_all":
            assigned_to = f"Assigned to: {self.username}"
            task_str += f"{self.create_task_line(assigned_by, assigned_to)}"
        else:
            task_str += f"{assigned_by}\n"
        
        task_str += f"{color.bold}Completed: {self.completed}{color.end}"
        return task_str


    def write_tasks_to_file(self, file_name:str, tasks:dict) -> str:
        """Ensures that file_name and tasks are valid before writing to file."""
        # Check if file_name is valid path to file that already exists
        if not path.isfile(file_name):
            return f"ERROR! - '{file_name}' is not a valid path."
        # Check if tasks is empty
        elif not bool(tasks):
            return "ERROR! - data is empty."
        # Check if tasks doesn't include "00001" - func will only ever be called when there is something to write,
        # and task_id's are assigned numerically, so follows there should always be a task with id "00001".
        elif "00001" not in tasks:
            return f"ERROR! - missing data. task '00001' could not be found. Provided data is below\n{tasks}."

        else:
            # Check that the newest task in tasks has all expected properties. As tasks are added 1 at a time,
            # sufficent to only check most recent is correct on each call to write_tasks_to_file.
            # Check that most recent task has all required properties.
            required_properties = ["username", "title", "description", "due_date", "assigned_date", "completed", "assigned_by"]
            prop_count = 0
    
            for prop in required_properties:
                if hasattr(self, prop):
                    prop_count += 1
                else:
                    return f"ERROR! property {prop} in task new is not valid."

            # Check number of properties in most recent task matches 'required_properties' length.
            if prop_count != len(required_properties):
                return "ERROR! New task does not have correct number of properties."

            # If all previous checks satisfied create tasks_data dictionary that can be converted to JSON.
            else:
                tasks_data = {}
                for task in tasks:
                    tasks_data[task] = tasks[task].__dict__

                write_json(file_name, tasks_data)
                return f"tasks successfully written to {file_name}"

    def print_this_task(self):
        print(f"due date\t{self.due_date}\ttype\t{type(self.due_date)}")
        print(f"assigned date\t{self.assigned_date}\ttype\t{type(self.assigned_date)}")
