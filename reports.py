from typing import Tuple
from datetime import datetime, date
from utility_functions import create_task_line

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def create_title_str(file_name: str) -> str:
    """Creates the title string for the report."""
    remaining_length = 70 - len(file_name)
    if remaining_length % 2 == 1:
        return f"{'='* round(remaining_length/2)}{file_name}{'='* (round(remaining_length/2) + 1)}"
    else:
        return f"{'='* round(remaining_length/2)}{file_name}{'='* round(remaining_length/2)}"
    
#===================TASK REPORT LOGIC===================
def generate_task_report(tasks: dict) -> None:
    """Creates a report on all tasks and writes to reports/task_overview.txt.""" 
    completed_tasks, incomplete_tasks, overdue_tasks = calculate_task_stats(tasks)

    # Create strings to write to file
    str_line = f"{'*'*70}"
    name_line = create_title_str("task_overview")
    number_of_tasks = f"TASKS TOTAL - {len(tasks)}"
    completed_tasks_str = create_task_str("Completed", completed_tasks, tasks)
    incomplete_tasks_str = create_task_str("Incomplete", incomplete_tasks, tasks)
    overdue_tasks_str = create_task_str("Overdue", overdue_tasks, tasks)

    text = f"{str_line}\n{name_line}\n{str_line}\n\n{number_of_tasks}\n\n{completed_tasks_str}\n\n{incomplete_tasks_str}\n\n{overdue_tasks_str}"

    with open("../reports/task_overview.txt", "w", encoding="UTF-8") as f:
        f.write(text)

def calculate_task_stats(tasks: dict) -> Tuple[int, int]:
    """Loop through tasks and record the total number of completed tasks."""
    current_date = date.today().strftime(DATETIME_STRING_FORMAT)
    completed_tasks_total = 0
    incomplete_tasks_total = 0
    overdue_tasks_total = 0
    for task_id in tasks:
        if tasks[task_id]["completed"]:
            completed_tasks_total += 1
        else:
            if tasks[task_id]["due_date"] < current_date:
                overdue_tasks_total += 1
            incomplete_tasks_total += 1
    return completed_tasks_total, incomplete_tasks_total, overdue_tasks_total

def create_task_str(status: str, status_total: int, tasks: dict) -> str:
    """Build string for each type of task (complete, incomplete and overdue)."""
    return f"{status} tasks - {status_total}\nPercentage completed - {(status_total/len(tasks)*100)}%"

#===================USER REPORT LOGIC===================
def generate_user_report(tasks: dict, users: dict) -> None:
    """Creates a report on all users and writes to reports/user_overview.txt.""" 
    str_line = f"{'*'*70}"
    name_line = create_title_str("user_overview")

    # Build a string for each user that include total tasks, complete, incomplete and overdue
    users_str = ""
    for user in users:
        users_str += create_user_str(tasks, users, user)

    total_users = f"Total users - {len(users)}"
    
    text = f"{str_line}\n{name_line}\n{str_line}\n\n{total_users}\n\n{users_str}"
    with open("../reports/user_overview.txt", "w", encoding="UTF-8") as f:
        f.write(text)

def create_user_str(tasks: dict, users: dict, user: str) -> str:
    """Creates the data for each user. Includes their total tasks, complete, incomplete and incomplete tasks."""
    task_list = users[user]["tasks"]

    user_str = f"{create_title_str(user)}\nTotal tasks: {len(task_list)}\n\n"
    user_str += f"{create_user_task_str("complete", tasks, task_list)}\n"
    user_str += f"{create_user_task_str("incomplete", tasks, task_list)}\n"
    user_str += create_user_task_str("overdue", tasks, task_list)
    return f"{user_str}\n"

def create_user_task_str(status: str, tasks: dict, task_list: list) -> str:
    """Builds the string for each type of task status. Includes count, percentage of total and title of all relevant tasks."""
    current_date = date.today().strftime(DATETIME_STRING_FORMAT)
    status_check = False
    tasks_str = ""
    if status == "complete":
        status_check = True

    task_count = 0
    for task in tasks:
        if status == "overdue":
            if task in task_list and tasks[task]["completed"] == status_check and tasks[task]["due_date"] < current_date:
                task_count += 1
                tasks_str += f"* {create_task_line(tasks[task]["title"], task, 68)}"
        elif task in task_list and tasks[task]["completed"] == status_check:
            task_count += 1
            tasks_str += f"* {create_task_line(tasks[task]["title"], task, 68)}"
    if task_count == 0:
        status_str = create_task_line(f"{status} tasks: {task_count}", "0%")
    else:
        status_str = create_task_line(f"{status} tasks: {task_count}", f"{round((task_count/len(task_list))* 100)}%")
    return status_str + tasks_str
