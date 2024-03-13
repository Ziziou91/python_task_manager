import pytest
from task_manager import create_data, edit_tasks
from task import Task
from user import User

@pytest.fixture(name="tasks")
def fixture_tasks() -> dict:
    """Create dictionary of tasks for testing.""" 
    return create_data("tests/tasks_test.json", "tasks")

@pytest.fixture(name="users")
def fixture_users() -> dict:
    """Create dictionary of tasks for testing.""" 
    return create_data("tests/users_test.json", "users")

# ============Test create_tasks============
def test_create_data_returns_dictionary(tasks: dict, users: dict) -> None:
    """Checks that create_data returns a dictionary."""
    assert isinstance(tasks, dict)
    assert isinstance(users, dict)

def test_create_data_return_dictionary_has_expected_length(tasks: dict, users: dict) -> None:
    """Checks that create_data returns a dict of of the expected length."""
    assert len(tasks) == 10
    assert len(users) == 3

def test_create_data_returns_task_instances(tasks: dict) -> None:
    """Checks that create_data returns a dictionary of task instances."""
    for task in tasks:
        assert isinstance(tasks[task], Task)

def test_create_data_returns_user_instances(users: dict) -> None:
    """Checks that create_data returns a dictionary of task instances."""
    for user in users:
        assert isinstance(users[user], User)

@pytest.mark.parametrize(
       ("task_id"),
       ["00001", "00002", "00003", "00004", "00005", "00006", "00007", "00008", "00009", "00010"]
)
def test_tasks_contains_expected_task_ids(tasks: dict, task_id: str) -> None:
    """Checks that task in create_tasks return value has expected properties."""
    assert task_id in tasks

@pytest.mark.parametrize(
       ("user"),
       ["admin", "john", "Naomi"]
)
def test_tasks_contains_expected_user_ids(users: dict, user: str) -> None:
    """Checks that task in create_tasks return value has expected properties."""
    assert user in users

@pytest.mark.parametrize(
       ("task_property"),
       [("username"),("title"),("description"),("due_date"),("assigned_by"),("completed")] 
)
def test_each_task_has_expected_properties(tasks: dict, task_property: str) -> None:
    """Checks that task in create_tasks return value has expected properties."""
    for task in tasks:
        assert hasattr(tasks[task], task_property)

# ============Test edit_tasks============
class TestEditTasks:
    """Test edit_tasks."""

    @pytest.fixture(name="users")
    def fixture_users(self) -> dict:
        """Create dictionary of users for testing.""" 
        return {"admin": {"tasks" :["00001", "00002", "00004"]}}
    def test_edit_tasks_returns_string(self,
                                       monkeypatch: pytest.MonkeyPatch,
                                       tasks: dict,
                                       users: dict) -> None:
        "Test that edit_tasks returns a string."
        responses = iter(["00001", "d", "test"])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))

        assert isinstance(edit_tasks(tasks, users, "admin", "view_all"), str)
