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
        """Ensures that file_name and data are correct before writing to file."""
        # Return an error message if any tests failed
        # TODO - 1) path.isfile doesn't work with tmpdir in task_test
        #if not path.isfile(file_name):
        #    return "ERROR!"
        ## TODO - 2) check that a JSON file already exists at file name

        # TODO - 3) check that data is non-empty, and there is a task with ID 00001 and it has the expected properties.
        # Only then write to file.
        write_json(file_name, data)
        return path.isfile(file_name)


    def print_this_task(self):
        print(f"due date\t{self.due_date}\ttype\t{type(self.due_date)}")
        print(f"assigned date\t{self.assigned_date}\ttype\t{type(self.assigned_date)}")
