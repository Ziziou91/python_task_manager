"""Tests Task class functionality."""
import json
from os import path, PathLike
from datetime import date
import pytest
from task import Task

@pytest.fixture(name="test_task_instance")
def fixure_test_task_instance() -> Task:
    """Create an instance of Task to run tests on."""
    return Task("Jane", "Test Task", "This is a test task", "Jane", "2024-08-01", False, "2024-08-01")

# ============Task instance tests============
def test_Task_creates_working_instance(test_task_instance: Task) -> None:
    """Test that Task can be called to create new isntance"""
    assert isinstance(test_task_instance, Task)

def test_Task_class_attributes(test_task_instance: Task) -> None:
    """Test instances of Task have expected class attributes."""
    assert  isinstance(test_task_instance.completed, bool)
    assert test_task_instance.completed is False

@pytest.mark.parametrize(
        ("task_attr", "expected"),
        (
            ("username", "Jane"),
            ("title", "Test Task"),
            ("description", "This is a test task"),
            ("due_date", "2024-08-01"),
            ("assigned_by", "Jane"),
            ("completed", False),
            ("assigned_date", "2024-08-01")
        )
)
class TestTaskInstanceAttributes:
    """Test that the instance attributes of a Task object behave as expected."""
    def test_Task_instance_attributes_type(self,
                                           task_attr: str,
                                           expected: str|bool,
                                           test_task_instance: Task) -> None:
        """Tests that instance attributes have correct type."""
        test_attr = getattr(test_task_instance, task_attr)
        assert isinstance(test_attr, type(expected))

    def test_Task_instance_attributes_value(self,
                                            task_attr: str,
                                            expected: str|bool,
                                            test_task_instance: Task) -> None:
        """Test that instance attributes have the expected value."""
        test_attr = getattr(test_task_instance, task_attr)
        assert test_attr == expected


# ===========Test add_task_to_tasks============
class TestAddTaskToTasks:
    """Testing for add_task_to_tasks."""
    def test_add_task_to_tasks_returns_dict(self, test_task_instance: Task):
        """Test add_task_to_tasks returns a dictionary."""
        tasks = {"00001" : Task("admin",
                                "first task",
                                "first task in tasks.",
                                "admin",
                                "2024-10-01",
                                False,
                                "2024-02-01")}
        assert isinstance(test_task_instance.add_task_to_tasks(tasks), dict)

    def test_add_task_to_tasks_return_value_expected_length(self, test_task_instance: Task):
        """Test add_task_to_tasks return value is of expected length."""
        tasks = {"00001" : Task("admin",
                                "first task",
                                "first task in tasks.",
                                "admin",
                                "2024-10-01",
                                False,
                                "2024-02-01")}
        assert len(test_task_instance.add_task_to_tasks(tasks)) == 2

    def test_add_task_to_tasks_returns_expected_value(self, test_task_instance: Task):
        """Test add_task_to_tasks returns the expected value."""
        tasks = {"00001" : Task("admin",
                                "first task",
                                "first task in tasks.",
                                "admin",
                                "2024-10-01",
                                False,
                                "2024-02-01")}
        expected = tasks.copy()
        expected["00002"] = test_task_instance
        assert test_task_instance.add_task_to_tasks(tasks) == expected

# ===========Test amend_task============
@pytest.fixture(name="users")
def fixture_users() -> dict:
    """Returns user dictionary for testing """
    return {
        "admin": {"password": "password",
                  "role": "admin",
                  "tasks": ["00001", "00002", "00004"],
                  "sign_up_date": "2020-01-01",
                  "completed": False},
        "john": {"password": "john",
                 "role": "user",
                 "tasks": ["00003", "00005", "00006", "00007", "00008"],
                 "sign_up_date": "2020-01-01",
                 "completed": False},
        "Naomi": {"password": "mypassword",
                  "role": "user",
                  "tasks": ["00009", "00010"],
                  "sign_up_date": "2024-02-18",
                  "completed": False}
    }

@pytest.mark.parametrize(
    ("str_1", "str_2", "attribute", "expected"),
    [
        ("m", True, "completed", True),
        ("t", "test", "title", "test"),
        ("d", "test description", "description", "test description"),
        ("u", "Naomi", "username", "Naomi"),
        ("a", "2024-07-22", "due_date", date(2024, 7, 22))
    ]
)
def test_amend_task_updates_attributes(monkeypatch: pytest.MonkeyPatch,
                                       test_task_instance: Task,
                                       users, str_1: str,
                                       str_2: str|bool,
                                       attribute: str,
                                       expected: any) -> None:
    """Tests that amend_task correctly updates task attributes."""
    responses = iter([str_1, str_2])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    test_task_instance.amend_task(users, "test.json", {"00001" :{}})
    new_value = getattr(test_task_instance, attribute)
    assert new_value == expected

# ===========Test amend_task_get_user_input============
@pytest.mark.parametrize(
    ("str_1", "str_2", "expected"),
    [
        ("m", True, {"property": "completed", "data": True}),
        ("t", "test", {"property": "title", "data": "test"}),
        ("d", "test", {"property": "description", "data": "test"}),
        ("u", "john", {"property": "username", "data": "john"}),
        ("a", "2024-07-22", {"property": "due_date", "data": date(2024, 7, 22)})
    ]
)
class TestAmendTaskGetUserInputHappyPath():
    """Test amend_task_get_user_input happy path."""
    def test_amend_task_get_user_input_returns_dictionary(self,
                                                          monkeypatch: pytest.MonkeyPatch,
                                                          test_task_instance: Task,
                                                          users: dict,
                                                          str_1: str,
                                                          str_2: str,
                                                          expected: str) -> None:
        """Test amend_task_get_user_input returns a dictionary."""
        responses = iter(["u", "john"])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))

        assert isinstance(test_task_instance.amend_task_get_user_input(users), dict)


    def test_amend_task_get_user_input_returns_expected(self,
                                                        monkeypatch: pytest.MonkeyPatch,
                                                        test_task_instance: Task,
                                                        users: dict,
                                                        str_1: str,
                                                        str_2: str,
                                                        expected: str) -> None:
        """Test amend_task_get_user_input returns expected."""
        responses = iter([str_1, str_2])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))

        assert test_task_instance.amend_task_get_user_input(users) == expected


class TestAmendTaskGetUserInputHandlesIncorrectMenuInputs(TestAmendTaskGetUserInputHappyPath):
    "Ensure amend_task_get_user_input handles incorrect inputs, asking and checking until valid."
    def test_amend_task_get_user_input_handles_uppercase_menu_input(self,
                                                                    monkeypatch: pytest.MonkeyPatch,
                                                                    test_task_instance: Task,
                                                                    users: dict,
                                                                    str_1: str,
                                                                    str_2: str,
                                                                    expected: str) -> None:
        """Test amend_task_get_user_input handles upper-case 'menu' inputs."""
        responses = iter([str_1.upper(), str_2])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))

        assert test_task_instance.amend_task_get_user_input(users) == expected

    def test_amend_task_get_user_input_handles_incorrect_input(self,
                                                               monkeypatch: pytest.MonkeyPatch,
                                                               test_task_instance: Task,
                                                               users: dict,
                                                               str_1: str,
                                                               str_2: str,
                                                               expected: str) -> None:
        """Test amend_task_get_user_input handles an incorrect 'menu' input, 
        asking again until correct."""
        responses = iter(["hello", "test", str_1, str_2])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))

        assert test_task_instance.amend_task_get_user_input(users) == expected

def test_amend_task_get_user_input_handles_incorrect_username(monkeypatch: pytest.MonkeyPatch,
                                                              test_task_instance: Task,
                                                              users: dict) -> None:
    """Test amend_task_get_user_input handles an incorrect 'username' input, 
    asking again until correct."""
    responses = iter(["u", "Jane", "Atul", "john"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    expected = {'data': 'john', 'property': 'username'}

    assert test_task_instance.amend_task_get_user_input(users) == expected

def test_amend_task_get_user_input_handles_incorrect_datestring(monkeypatch: pytest.MonkeyPatch,
                                                                test_task_instance: Task,
                                                                users: dict) -> None:
    """Test amend_task_get_user_input handles an incorrect date string input, 
    asking again until correct."""
    responses = iter(["a", "24-8-40", "incorrect", "2024-07-12"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    expected = {'data': date(2024, 7, 12), 'property': 'due_date'}

    assert test_task_instance.amend_task_get_user_input(users) == expected


# ===========Test create_due_date============
def test_create_due_date_returns_date_object(test_task_instance: Task) -> None:
    """Ensure that create_due_date returns a date object."""
    assert isinstance(test_task_instance.create_due_date("2024-08-01"), date)

def test_create_due_date_returns_expected(test_task_instance :Task) -> None:
    """Test that create_due_date returns expected value."""
    assert test_task_instance.create_due_date("2024-08-01") == date(2024, 8, 1)

def test_create_due_date_handles_invalid_string(monkeypatch: pytest.MonkeyPatch,
                                                test_task_instance: Task) -> None:
    """Test that create_due_date handles invalid due_date_str."""
    responses = iter(["another test", "2024-07-01"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    assert test_task_instance.create_due_date("test") == date(2024, 7, 1)

# ===========Test create_task_id============
class TestCreateTaskId:
    """Test create_task functionality"""
    TASKS:dict = {"00001": {}}
    def test_create_task_id_returns_str(self, test_task_instance: Task) -> None:
        """Test that create_due_date returns a string."""
        assert isinstance(test_task_instance.create_task_id(self.TASKS), str)

class TestCreateTaskIdHandlesEmpty(TestCreateTaskId):
    """Tests create_task_id for empty tasks dictionary."""
    TASKS:dict = {}
    def test_create_task_id_creates_initial_id(self, test_task_instance: Task) -> None:
        """Test that create_due_date works when given an empy dictionary."""
        assert test_task_instance.create_task_id(self.TASKS) == "00001"

class TestCreateTaskIdHandlesLargerTasksDict(TestCreateTaskId):
    """Tests create_task_id for longer tasks dictionary."""
    TASKS = {"00001": {}, "00002": {}, "00003": {}, "00004": {}}
    def test_create_task_id_returns_expected(self, test_task_instance: Task) -> None:
        """Test that create_due_date works when given an empy dictionary."""
        assert test_task_instance.create_task_id(self.TASKS) == "00005"


# ===========Test create_task_id============
def test_create_task_id_returns_string(test_task_instance: dict) -> None:
    """Test create_task_id returns a string."""
    assert isinstance(test_task_instance.create_task_id({}), str)
    assert isinstance(test_task_instance.create_task_id({"00001": {}}), str)

def test_create_task_id_handles_empty_tasks_dictionary(test_task_instance: dict) -> None:
    """Test create_task_id returns '00001' when called with empty tasks dictionary."""
    assert test_task_instance.create_task_id({}) == "00001"

@pytest.mark.parametrize(
        ("tasks", "expected"),
        [
            ({"00001": {}}, "00002"),
            ({"00001": {}, "00002": {}}, "00003"),
            ({"00001": {}, "00002": {}, "00003": {}}, "00004")
        ]
)
def test_create_task_id_returns_expected(test_task_instance: dict, 
                                         tasks: dict, 
                                         expected: str) -> None:
    """Test create_task_id returns expected."""
    assert test_task_instance.create_task_id(tasks) == expected


# ===========Test create_task_str_description===========
def test_create_task_str_description_returns_str(test_task_instance: dict) -> None:
    """Test create_task_str_description returns a string."""
    assert isinstance(test_task_instance.create_task_str_description(), str)

def test_create_task_str_returns_expected() -> None:
    """Test create_task_str returns expected."""
    test_task = Task("admin", "test", "This task has a really long string. The reason it is so long is so that it ensures 'create_task_str_description' adds a newline.", "admin", "2024-12-01", False, "2024-06-01")
    assert test_task.create_task_str_description() == "This task has a really long string. The reason it is so long is so\nthat it ensures 'create_task_str_description' adds a newline."


# ===========Test create_task_str============
def test_create_task_str_returns_string(test_task_instance: Task) -> None:
    """Tests create_task_str returns a string."""
    assert isinstance(test_task_instance.create_task_str("00001", "view_all"), str)


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
                {"username": "admin",
                 "title": "Add functionality to task manager",
                 "description": "Add additional options and refactor the code.",
                 "due_date": "2024-02-18",
                 "assigned_date": date.today().strftime("%Y-%m-%d"),
                 "completed": "False",
                 "assigned_by": "admin"}
            ]
    )
    class TestWriteTasksToFileHappyPath:
        """Tests that data can be written to file and then successfully loaded."""
        def test_write_task_to_file_stores_data(self,
                                                create_file: PathLike,
                                                test_data: dict) -> None:
            """Write data to the file location initialised by 'create_file' and test."""
            # Write the test_data to temp_file
            test_task = {"00001" : Task(test_data["username"],
                                        test_data["title"],
                                        test_data["description"],
                                        test_data["assigned_by"],
                                        test_data["due_date"],
                                        test_data["completed"],
                                        test_data["assigned_date"])}
            test_task["00001"].write_tasks_to_file(create_file, test_task)

            # Open temp_file and save contents as 'data'.
            file = open(create_file, "r", encoding="UTF-8")
            with file:
                data = json.load(file)

            assert data == {"00001": test_data}

        def test_write_task_to_file_returns_success_str(self,
                                                        create_file: PathLike,
                                                        test_task_instance: Task,
                                                        test_data: dict) -> None:
            """Write data to the file location initialised by 'create_file' and data can be loaded."""
            tasks = {"00001" : Task("admin", "first task", "first task in tasks.", "admin", "2024-10-01", False, "2024-01-01")}
            assert test_task_instance.write_tasks_to_file(create_file, tasks) == f"tasks successfully written to {create_file}"

    class TestWriteTasksToFileErrors:
        """Test that write_task_to_file returns expected error strings."""
        def test_write_task_to_file_invalid_path_error(self,
                                                       create_file: PathLike,
                                                       test_task_instance: Task) -> None:
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
        def test_write_task_to_file_empty_data_error(self,
                                                     create_file: PathLike,
                                                     test_task_instance: Task,
                                                     data: any,
                                                     expected: str) -> None:
            """Test write_task_to_file returns an error when data is empty"""
            assert test_task_instance.write_tasks_to_file(create_file, data) == expected

        def test_write_task_to_file_missing_task_00001_error(self, create_file, test_task_instance):
            """Test write_task_to_file returns an error when data is missing key '00001'."""
            data = {"why is there no task 0001?" : "I don't know"}
            expected = f"ERROR! - missing data. task '00001' could not be found. Provided data is below\n{data}."
            assert test_task_instance.write_tasks_to_file(create_file, data) == expected
