

def file_title(file_name: str) -> str:
    """Creates the title string for the report."""
    remaining_length = 70 - len(file_name)
    if remaining_length % 2 == 1:
        return f"{'='* round(remaining_length/2)}{file_name}{'='* (round(remaining_length/2) + 1)}"
    else:
        return f"{'='* round(remaining_length/2)}{file_name}{'='* round(remaining_length/2)}"

def calculate_completed_tasks(tasks: dict) -> int:
    """Loop through tasks and record the total number of completed tasks."""
    completed_tasks_total = 0
    for task_id in tasks:
        if tasks[task_id]["completed"]:
            completed_tasks_total += 1
    return completed_tasks_total

def generate_task_report(tasks: dict) -> None:
    """Creates a report on all tasks and writes to reports/task_overview.txt."""
    print("in generate_task_report")
    # task_overview.txt should contain:
    # - The total number of tasks that have been generated and tracked

    # - The total number of completed tasks
    completed_tasks = calculate_completed_tasks(tasks)
    # - The total number on uncompleted tasks
    # - The percentage of tasks that are uncompleted

    # - The total number of uncompleted, overdue tasks
    # - The percentage of taskss that are overdue

    # Calculate completed, uncompleted and overdue tasks

    # Create strings to write to file
    str_line = f"{'*'*70}"
    name_line = file_title("task_overview")
    number_of_tasks = f"TASKS TOTAL - {len(tasks)}"
    completed_tasks_str = f"Completed tasks - {completed_tasks}\nPercentage completed - {(completed_tasks/len(tasks)* 100)}%"

    text = f"{str_line}\n{name_line}\n{str_line}\n\n{number_of_tasks}\n\n{completed_tasks_str}"

    with open("../reports/task_overview.txt", "w", encoding="UTF-8") as f:
        f.write(text)


def generate_user_report():
    print("in generate_user_report")
