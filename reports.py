from typing import Tuple
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def file_title(file_name: str) -> str:
    """Creates the title string for the report."""
    remaining_length = 70 - len(file_name)
    if remaining_length % 2 == 1:
        return f"{'='* round(remaining_length/2)}{file_name}{'='* (round(remaining_length/2) + 1)}"
    else:
        return f"{'='* round(remaining_length/2)}{file_name}{'='* round(remaining_length/2)}"

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

def generate_task_report(tasks: dict) -> None:
    """Creates a report on all tasks and writes to reports/task_overview.txt.""" 
    completed_tasks, incomplete_tasks, overdue_tasks = calculate_task_stats(tasks)

    # Create strings to write to file
    str_line = f"{'*'*70}"
    name_line = file_title("task_overview")
    number_of_tasks = f"TASKS TOTAL - {len(tasks)}"
    completed_tasks_str = create_task_str("Completed", completed_tasks, tasks)
    incomplete_tasks_str = create_task_str("Incomplete", incomplete_tasks, tasks)
    overdue_tasks_str = create_task_str("Overdue", overdue_tasks, tasks)

    text = f"{str_line}\n{name_line}\n{str_line}\n\n{number_of_tasks}\n\n{completed_tasks_str}\n\n{incomplete_tasks_str}\n\n{overdue_tasks_str}"

    with open("../reports/task_overview.txt", "w", encoding="UTF-8") as f:
        f.write(text)


def generate_user_report():
    print("in generate_user_report")
