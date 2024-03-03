from datetime import date
import pytest
from task import Task

# ============Task instance tests============
def test_Task_creates_working_instance():
    """Test that Task can be called to create new isntance"""
    assert isinstance(Task("Test", "Test", "Test", "Test", "2024-08-01"), Task)

def test_Task_class_attributes():
    """Test instances of Task have expected class attributes."""
    test_task = Task("Test", "Test", "Test", "Test", "2024-08-01")
    assert  isinstance(test_task.completed, bool)
    assert test_task.completed is False

@pytest.mark.parametrize(
        ("task_attr", "expected"),
        (
            ("username", str),
            ("title", str),
            ("description", str),
            ("due_date", date),
            ("assigned_date", date),
            ("assigned_by", str)
        )
)
def test_Task_instance_attributes_type(task_attr, expected):
    """Tests that instance attributes have correct type."""
    test_task = Task("Test", "Test", "Test", "Test", "2024-08-01")
    test_attr = getattr(test_task, task_attr)
    assert isinstance(test_attr, expected)

@pytest.mark.parametrize(
        ("task_attr", "expected"),
        (
            ("username", "Jane"),
            ("title", "Test Task"),
            ("description", "This is a test task"),
            ("due_date", date(2024, 8, 1)),
            ("assigned_by", "Jane")
        )
)
def test_task_instance_attributes_value(task_attr, expected):
    """Test that instance attributes have the expected value."""
    test_task = Task("Jane", "Test Task", "This is a test task", "Jane", "2024-08-01")
    test_attr = getattr(test_task, task_attr)
    assert test_attr == expected

# ===========Test create_due_date============
def test_create_due_date_returns_date_object():
    """Ensure that create_due_date returns a date object."""
    test_task = Task("Test", "Test", "Test", "Test", "2024-08-01")
    assert isinstance(test_task.create_due_date("2024-08-01"), date)

def test_create_due_date_returns_expected():
    """Test that create_due_date returns expected value."""
    test_task = Task("Test", "Test", "Test", "Test", "2024-08-01")
    assert test_task.create_due_date("2024-08-01") == date(2024, 8, 1)

# ===========Test create_task_id============
def create_task_id_returns_str():
    """Test that create_due_date returns a string."""
    test_task = Task("Test", "Test", "Test", "Test", "2024-08-01")
    assert isinstance(test_task.create_due_date({"00001": {}}), str)

def create_task_id_handles_empty_dict():
    """Test that create_due_date works when given an empy dictionary."""
    test_task = Task("Test", "Test", "Test", "Test", "2024-08-01")
    assert isinstance(test_task.create_due_date({}), str)
    assert test_task.create_due_date({}) == "00001"