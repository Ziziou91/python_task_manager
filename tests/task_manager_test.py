import pytest
from task_manager import create_tasks, edit_tasks
from task import Task

@pytest.fixture(name="tasks")
def fixture_tasks() -> dict:
    """Create dictionary of tasks for testing.""" 
    return create_tasks("tests/tasks_test.json")

# ============Test create_tasks============
def test_create_task_returns_dictionary(tasks:dict) -> None:
    """Checks that create_tasks returns a dictionary."""
    assert isinstance(tasks, dict)

def test_create_task_return_dictionary_has_expected_length(tasks:dict) -> None:
    """Checks that create_tasks returns a dictionary."""
    assert len(tasks) == 10

def test_create_task_returns_task_instances(tasks:dict) -> None:
    """Checks that create_tasks returns a dictionary of task instances."""
    for task in tasks:
        assert isinstance(tasks[task], Task)

@pytest.mark.parametrize(
       ("task_id"),
       ["00001", "00002", "00003", "00004", "00005", "00006", "00007", "00008", "00009", "00010"]
)
def test_tasks_contains_expected_task_ids(tasks:dict, task_id:str) -> None:
    """Checks that task in create_tasks return value has expected properties."""
    assert task_id in tasks

@pytest.mark.parametrize(
       ("task_property"),
       [("username"),("title"),("description"),("due_date"),("assigned_by"),("completed")] 
)
def test_each_task_has_expected_properties(tasks:dict, task_property:str) -> None:
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


   
    def test_edit_tasks_returns_string(self, monkeypatch:pytest.MonkeyPatch, tasks:dict, users) -> None:
        "Test that edit_tasks returns a string."
        responses = iter(["00001", "d", "test"])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))

        assert isinstance(edit_tasks(tasks, users, "admin", "view_all"), str)

class TestEditTasksViewAll(TestEditTasks):
    def test_edit_tasks_handles_view_all(self, tasks:dict) -> None:
        "TODO"
        pass
