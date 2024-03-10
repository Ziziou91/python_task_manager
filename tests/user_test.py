"""Tests User class and Admin subclass functionality."""
import json
from os import path, PathLike
import pytest
from user import User

@pytest.fixture(name="test_user_instance")
def fixure_test_user_instance() -> User:
    """Create an instance of Task to run tests on."""
    return User("Joy", "changeme", ["00004"], "2024-04-01")

# ============User instance tests============
def test_User_creates_working_instance(test_user_instance:User) -> None:
    """Test that Task can be called to create new isntance"""
    assert isinstance(test_user_instance, User)

@pytest.mark.parametrize(
        ("user_attr", "expected"),
        [
            ("username", "Joy"),
            ("password", "changeme"),
            ("tasks", ["00004"]),
            ("sign_up_date", "2024-04-01"),
        ]
)
class TestUserInstanceAttributes:
    """Test instance of User has expected instance attributes."""
    def test_Task_class_attributes(self, test_user_instance:User, user_attr: str, expected:str|list) -> None:
        """Tests that instance attributes have correct type."""
        test_attr = getattr(test_user_instance, user_attr)
        assert isinstance(test_attr, type(expected))

    def test_Task_instance_attributes_value(self, test_user_instance:User, user_attr:str, expected:str|list) -> None:
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
    def test_create_file(self, create_file:PathLike) -> None:
        """Test 'create_file' fixture correctly creates a file at the provided path."""
        assert isinstance(create_file, PathLike)
        assert create_file.is_file()

    
