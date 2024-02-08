"""Tests for fctns in unit_functions."""
import pytest
from unit_functions import load_json

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
