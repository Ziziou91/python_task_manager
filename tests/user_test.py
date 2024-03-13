"""Tests User class and Admin subclass functionality."""
import json
from os import path, PathLike
import pytest
from user import User

@pytest.fixture(name="test_user_instance")
def fixure_test_user_instance() -> User:
    """Create an instance of Task to run tests on."""
    return User("Joy", "changeme", ["00024"], "2024-04-01")

# ============User instance tests============
def test_User_creates_working_instance(test_user_instance:User) -> None:
    """Test that Task can be called to create new isntance"""
    assert isinstance(test_user_instance, User)

@pytest.mark.parametrize(
        ("user_attr", "expected"),
        [
            ("username", "Joy"),
            ("password", "changeme"),
            ("tasks", ["00024"]),
            ("sign_up_date", "2024-04-01"),
        ]
)
class TestUserInstanceAttributes:
    """Test instance of User has expected instance attributes."""
    def test_Task_class_attributes(self, test_user_instance: User,
                                   user_attr: str,
                                   expected:str|list) -> None:
        """Tests that instance attributes have correct type."""
        test_attr = getattr(test_user_instance, user_attr)
        assert isinstance(test_attr, type(expected))

    def test_Task_instance_attributes_value(self,
                                            test_user_instance: User,
                                            user_attr: str,
                                            expected: str|list) -> None:
        """Test that instance attributes have the expected value."""
        test_attr = getattr(test_user_instance, user_attr)
        assert test_attr == expected

# ============Test write_users_to_file============
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
class TestWriteUsersToFile():
    """Class to test write_tasks_to_file with provided fixture"""
    def test_create_file(self, create_file: PathLike) -> None:
        """Test 'create_file' fixture correctly creates a file at the provided path."""
        assert isinstance(create_file, PathLike)
        assert create_file.is_file()


    @pytest.mark.parametrize(
            "test_data",
            [
                {"username": "Lisa",
                 "password": "newpassword",
                 "tasks": ["00018", "00022"],
                 "sign_up_date": "2024-02-18"}
            ]
    )
    class TestWriteUsersToFileHappyPath:
        """Tests that data can be written to file and then successfully loaded."""
        def test_write_users_to_file_stores_data(self,
                                                 create_file: PathLike,
                                                 test_data: dict) -> None:
            """Write data to the file location initialised by 'create_file'."""
            # Write the test_data to temp_file
            users = {test_data["username"] : User(test_data["username"],
                                                  test_data["password"],
                                                  test_data["tasks"],
                                                  test_data["sign_up_date"])}
            users["Lisa"].write_users_to_file(create_file, users)

            # Open temp_file and save contents as 'data'.
            file = open(create_file, "r", encoding="UTF-8")
            with file:
                data = json.load(file)

            assert data == {"Lisa": test_data}

        def test_write_users_to_file_returns_success_str(self, 
                                                         create_file: PathLike,
                                                         test_data: dict) -> None:
            """Write data to the file location initialised by 'create_file'."""
            users = {test_data["username"] : User(test_data["username"],
                                                  test_data["password"],
                                                  test_data["tasks"],
                                                  test_data["sign_up_date"])}
            assert users["Lisa"].write_users_to_file(create_file, users) == f"tasks successfully written to {create_file}"

    class TestWriteTasksToFileErrors:
        """Test that write_user_to_file returns expected error strings."""
        def test_write_task_to_file_invalid_path_error(self,
                                                       create_file: PathLike,
                                                       test_user_instance: User) -> None:
            """Test write_user_to_file returns an error string."""
            invalid_path = "wrong_path"
            assert test_user_instance.write_users_to_file(invalid_path, {"Lisa": {}}) == f"ERROR! - '{invalid_path}' is not a valid path."
