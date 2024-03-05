"""Task class to contain all data and expected functionality for any task."""
from datetime import date
from os import path
from utility_functions import write_json

class Task:
    """Each instance will include all task details, as well functionality."""
    # TODO - Should datetime be stored utf best practice
    # TODO - New instance of class should write task details to tasks.json on creation
    def __init__(self, username: str, title:str, description:str, assigned_by:str, due_date_str:str) -> None:
        self.username = username
        self.title = title
        self.description = description
        self.due_date = self.create_due_date(due_date_str)
        self.assigned_date = date.today()
        self.assigned_by = assigned_by

    completed = False

    def amend_task(self):
        # Needs menu logic
        # go about using input() like you normally would:
        i = input("What is your name?")
        return i 
        # Take property and data arguments
        # check type of data is correct
        # route accordingly - call: 
        # create_due_date
        # Update username 
        # - call method on associated user object to add the task
        # - "                                   " to remove the task
        pass

    def create_due_date(self, due_date_str) -> date:
        """takes a due_date_str (format 'YYYY-MM-DD') and returns a date object"""
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


    def write_tasks_to_file(self, file_name:str, data:dict) -> str:
        """Ensures that file_name and data are valid before writing to file."""
        # Check if file_name is valid path to file that already exists
        if not path.isfile(file_name):
            return f"ERROR! - '{file_name}' is not a valid path."
        # Check if data is empty
        elif not bool(data):
            return "ERROR! - data is empty."
        # Check if data doesn't include "00001" - func will only ever be called when there is something to write,
        # and task_id's are assigned numerically, so follows there should always be a task with id "00001".
        elif "00001" not in data:
            return f"ERROR! - missing data. task '00001' could not be found. Provided data is below\n{data}."

        else:
            # Check that the newest task in data has all expected properties. As tasks are added 1 at a time,
            # sufficent to only check most recent is correct on each call to write_tasks_to_file.

            # Get the most recent (greatest) task_id.
            task_id_list = [int(task_id) for task_id in data.keys()]
            new_task_id = str(max(task_id_list))
            leading_zero_len = 5 - len(new_task_id)
            new_task_id = f"{(("0" * leading_zero_len) + new_task_id)}"

            # Check that most recent task has all required properties.
            required_properties = ["username", "title", "description", "due_date", "assigned_date", "completed", "assigned_by"]
            print("new_task_id", new_task_id)
            prop_count = 0
            for prop in data[new_task_id]:
                prop_count += 1
                if prop not in required_properties:
                    return f"ERROR! property {prop} in task {new_task_id} is not valid."

            # Check number of properties in most recent task matches 'required_properties' length.
            if prop_count != len(required_properties):
                return f"ERROR! Task {new_task_id} does not have correct number of properties."

            # If all previous checks satisfied write to 'file_name'.
            else:
                write_json(file_name, data)
                return f"data successfully written to {file_name}"


    def print_this_task(self):
        print(f"due date\t{self.due_date}\ttype\t{type(self.due_date)}")
        print(f"assigned date\t{self.assigned_date}\ttype\t{type(self.assigned_date)}")
