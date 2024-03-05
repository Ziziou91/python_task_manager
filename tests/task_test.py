"""Tests Task class functionality."""
import json
from os import path, PathLike
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

# ===========Test amend_task============
def test_something_that_involves_user_input(monkeypatch:pytest.MonkeyPatch, test_task_instance:Task) -> None:

    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "Mark")

    assert test_task_instance.amend_task() == "Mark" 

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
@pytest.fixture(name="create_file")
def fixture_create_file(request:list, tmp_path) -> PathLike:
    """Create temp_file for write_tasks_to_file tests in subclasses."""
    temp_dir = tmp_path / "sub"
    temp_dir.mkdir()
    temp_file = temp_dir / request.param
    file = open(temp_file, "w", encoding="UTF-8")
    file.close()
    return temp_file

@pytest.mark.parametrize("create_file", ["output.json"], indirect=True)
class TestWriteTasksToFile():
    """Class to test write_tasks_to_file with provided fixture"""
    def test_create_file(self, create_file:PathLike) -> None:
        """Test 'create_file' fixture correctly creates a file at the provided path."""
        assert isinstance(create_file, PathLike)
        assert create_file.is_file()

    @pytest.mark.parametrize(
            "test_data",
            [
                {"00001" : {"username": "admin", "title": "Add functionality to task manager", "description": "Add additional options and refactor the code.", "due_date": "2024-02-18", "assigned_date": "2022-11-22", "completed": "False", "assigned_by": "admin"}}

            ]
    )
    class TestWriteTasksToFileHappyPath:
        """Tests that data can be written to file and then successfully loaded, as well as function returns expected response."""
        def test_write_task_to_file_stores_data(self, create_file:PathLike, test_task_instance:Task, test_data:dict) -> None:
            """Write data to the file location initialised by 'create_file' and test data can be loaded."""
            # Write the test_data to temp_file
            test_task_instance.write_tasks_to_file(create_file, test_data)
        
            # Open temp_file and save contents as 'data'.
            file = open(create_file, "r", encoding="UTF-8")
            with file:
                data = json.load(file)
        
            assert data == test_data

        def test_write_task_to_file_returns_success_str(self, create_file:PathLike, test_task_instance:Task, test_data:dict) -> None:
            """Write data to the file location initialised by 'create_file' and data can be loaded."""
            assert test_task_instance.write_tasks_to_file(create_file, test_data) == f"data successfully written to {create_file}"

    class TestWriteTasksToFileErrors:
        """Test that write_task_to_file returns expected error strings."""
        def test_write_task_to_file_invalid_path_error(self, create_file:PathLike, test_task_instance:Task) -> None:
            """Test write_task_to_file returns an error string when the provided file_name string is invalid."""
            invalid_path = "wrong_path"
            assert test_task_instance.write_tasks_to_file(invalid_path, {"00001": {}}) == f"ERROR! - '{invalid_path}' is not a valid path."

        @pytest.mark.parametrize(
            ("data", "expected"),
            [
                ("", "ERROR! - data is empty."),
                ([], "ERROR! - data is empty."),
                ({}, "ERROR! - data is empty."),
                ((), "ERROR! - data is empty."),

            ]
        )
        def test_write_task_to_file_empty_data_error(self, create_file:PathLike, test_task_instance:Task, data:any, expected:str) -> None:
            """Test write_task_to_file returns an error when data is empty"""
            assert test_task_instance.write_tasks_to_file(create_file, data) == expected

        def test_write_task_to_file_missing_task_00001_error(self, create_file, test_task_instance):
            """Test write_task_to_file returns an error when data is missing key '00001'."""
            data = {"why is there no task 0001?" : "I don't know"}
            expected = f"ERROR! - missing data. task '00001' could not be found. Provided data is below\n{data}."
            assert test_task_instance.write_tasks_to_file(create_file, data) == expected
