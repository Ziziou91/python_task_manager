"""Tests for fctns in unit_functions."""
import pytest
from datetime import datetime
from utility_functions import load_json, difference_between_dates, color

# load_json tests
def test_load_json_returns_dictionary():
    """ensures that load_json returns a dictionary"""
    assert isinstance(load_json("tasks.json"), dict)

def test_load_json_FileNotFoundError_error():
    """checks load_json raises a FileNotFoundError when given an invalid path."""
    with pytest.raises(FileNotFoundError) as excinfo:
        load_json("test")
    assert str(excinfo.value) == "Error! test is an invalid path."

def test_load_json_returns_expected_value():
    """ensures that load_json correctly loads json"""
    expected_dict = {"hello" : "world"}
    assert  load_json("tests/test_data.json") == expected_dict

# difference_between_dates tests
def test_difference_between_dates_returns_string():
    """Ensures that difference_between_dates returns a string."""
    current_date = datetime.now().date()
    due_date = datetime.strptime("2024-02-02", "%Y-%m-%d").date()
    assert isinstance(difference_between_dates(current_date, due_date), str)

def test_difference_between_dates_returns_expected_value():
    """difference_between_dates returns a green or yellow string when appropiate."""
    date_1 = datetime.strptime("2024-02-02", "%Y-%m-%d").date()
    date_2 = datetime.strptime("2024-02-04", "%Y-%m-%d").date()
    date_3 = datetime.strptime("2025-02-02", "%Y-%m-%d").date()
    assert difference_between_dates(date_1, date_2) == f"{color.yellow}2 days{color.end}"
    assert difference_between_dates(date_1, date_3) == f"{color.green}366 days{color.end}"
    assert difference_between_dates(date_2, date_3) == f"{color.green}364 days{color.end}"

def test_difference_between_dates_returns_expected_value_when_overdue():
    """difference_between_dates returns a red string and adds overdue suffix when appropiate."""
    date_1 = datetime.strptime("2024-02-02", "%Y-%m-%d").date()
    date_2 = datetime.strptime("2024-02-04", "%Y-%m-%d").date()
    date_3 = datetime.strptime("2025-02-02", "%Y-%m-%d").date()
    assert difference_between_dates(date_2, date_1) == f"{color.red}2 days overdue{color.end}"
    assert difference_between_dates(date_3, date_1) == f"{color.red}366 days overdue{color.end}"
    assert difference_between_dates(date_3, date_2) == f"{color.red}364 days overdue{color.end}"


