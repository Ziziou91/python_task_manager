import pytest
from task_manager import create_tasks

@pytest.fixture(name="tasks")
def fixture_tasks() -> dict:
    """Create dictionary of tasks for testing.""" 
    return create_tasks("tasks.json")

# ============Test create_tasks============
def test_create_task_returns_dictionary(tasks:dict) -> None:
    """Checks that create_tasks returns a dictionary."""
    assert isinstance(tasks, dict)

def test_create_task_return_dictionary_has_expected_length(tasks:dict) -> None:
    """Checks that create_tasks returns a dictionary."""
    assert len(tasks) == 10

@pytest.mark.parametrize(
       ("property"),
       [("username"),("title"),("description"),("due_date"),("assigned_by"),("completed")] 
)
def test_each_task_has_expected_properties(tasks:dict, property:str) -> None:
    """Checks that task in create_tasks return value has expected properties."""
    for task in tasks:
        assert hasattr(tasks[task], property)

