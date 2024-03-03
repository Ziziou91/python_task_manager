"""Tests Task class functionality."""
from datetime import date
import pytest
from task import Task

@pytest.fixture(name="test_task_instance")
def fixure_test_task_instance() -> Task:
    """This fixture will only be available within the scope of TestGroup"""
    return Task("Jane", "Test Task", "This is a test task", "Jane", "2024-08-01")

# ============Task instance tests============
def test_Task_creates_working_instance(test_task_instance:Task) -> None:
    """Test that Task can be called to create new isntance"""
    assert isinstance(test_task_instance, Task)

def test_Task_class_attributes(test_task_instance:Task) -> None:
    """Test instances of Task have expected class attributes."""
    assert  isinstance(test_task_instance.completed, bool)
    assert test_task_instance.completed is False

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
class TestTaskInstanceAttributes:
    """Test that the instance attributes of a Task object behave as expected."""
    def test_Task_instance_attributes_type(self, task_attr:str, expected:str|date, test_task_instance:Task) -> None:
        """Tests that instance attributes have correct type."""
        test_attr = getattr(test_task_instance, task_attr)
        assert isinstance(test_attr, type(expected))

    def test_Task_instance_attributes_value(self, task_attr:str, expected:str|date, test_task_instance:Task) -> None:
        """Test that instance attributes have the expected value."""
        test_attr = getattr(test_task_instance, task_attr)
        assert test_attr == expected

# ===========Test create_due_date============
def test_create_due_date_returns_date_object(test_task_instance:Task) -> None:
    """Ensure that create_due_date returns a date object."""
    assert isinstance(test_task_instance.create_due_date("2024-08-01"), date)

def test_create_due_date_returns_expected(test_task_instance:Task) -> None:
    """Test that create_due_date returns expected value."""
    assert test_task_instance.create_due_date("2024-08-01") == date(2024, 8, 1)

# ===========Test create_task_id============
class TestCreateTaskId:
    """Test create_task functionality"""
    TASKS:dict = {"00001": {}}
    def test_create_task_id_returns_str(self, test_task_instance:Task) -> None:
        """Test that create_due_date returns a string."""
        assert isinstance(test_task_instance.create_task_id(self.TASKS), str)

class TestCreateTaskIdHandlesEmpty(TestCreateTaskId):
    """Tests create_task_id for empty tasks dictionary."""
    TASKS:dict = {}
    def test_create_task_id_creates_initial_id(self, test_task_instance:Task) -> None:
        """Test that create_due_date works when given an empy dictionary."""
        assert test_task_instance.create_task_id(self.TASKS) == "00001"

class TestCreateTaskIdHandlesLargerTasksDict(TestCreateTaskId):
    """Tests create_task_id for longer tasks dictionary."""
    TASKS = {"00001": {}, "00002": {}, "00003": {}, "00004": {}}
    def test_create_task_id_returns_expected(self, test_task_instance:Task) -> None:
        """Test that create_due_date works when given an empy dictionary."""
        assert test_task_instance.create_task_id(self.TASKS) == "00005"

# ===========Test write_tasks_to_file============
def test_write_tasks_to_file(test_task_instance:Task, tmpdir) -> None:
    """Test that write_tasks_to_file works."""
    file = tmpdir.join("output.json")
    test_task_instance.write_tasks_to_file(file, {"00001": {}})
    assert file.read() == '{"00001": {}}'
    assert test_task_instance.write_tasks_to_file(file, {"00001": {}}) is True

# What happens when data is empty, or not what the function expects?
# def test_write_tasks_to_file_handles_invalid_path(test_task_instance:Task) -> None:
#     """Test write_tasks_to_file returns an error message when given an invalid file path."""
#     assert test_task_instance.write_tasks_to_file("invalid_path", {"00001": {}}) == "ERROR!"