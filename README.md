# python_task_manager

Task management system for a small business. Designed to assign and manage tasks given to a team of employees. Users can create new users, create and assign tasks, mark tasks as complete and edit all properties of incomplete tasks.

Application is built with vanilla Python and uses CLI to interact with user. Recent improvements has focused on adopting OOP design pattern for tasks, users and testing - the intent behind this being to create an app that is easily maintainable and extendable. Coding best practices have been applied throughout. 

Particular attention has been paid to testing. TDD has been utilised extensively to create and ensure functionality of the app. User inputs have been mocked, and temporary files to test functionality reliant on reading and writing files has been used extensively to provide comprehensive test coverage. More details on how this was achieved, as well as how to use the test suite, can be found below.   


## How to install and run the project

### Installation

This application requires `python3` to run. The following command will check if it's installed:

    python3 --version

Output should look something like `Python 3.8.4`. If not you have a couple of options:

1) Install using homebrew. If homebrew is already installed this is as simple as running `brew install`

2) Install using the official installer. You can find your required version at Python.org

### Running the app

Start with the following command in the apps root directory:

    python3 task_manager.py

You can then interact with the application by using the following commands:

    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    s - Stastics
    e - Exit

Additional inputs are required to register users, add tasks and view tasks. Menus and instruction are provided in the app.

### Testing

This app relies on [pytest](https://docs.pytest.org/en/stable/) for testing functionality. In the apps root directory type:

    pytest

You can check if pytest is installed with:

    pytest --version

If this command fails, you might need to install pytest using:

    pip install -U pytest

More details about pip (python package installer) can be found [here](https://pypi.org/project/pip/)

Pytest functionality has been used to mock user inputs, as well as create temporary files to test that app correctly reads and writes to file:
- Mocking of user inputs that would usually be provided in CLI has been achieved with using [monkeypatch](https://docs.pytest.org/en/4.6.x/monkeypatch.html) to patch the builtin `input` function. Where multiple inputs are required to test nested menus, or ensure the app handles incorrect inputs, an interable is passed to `monkeypatch.setattr`.   
- Where I've wanted to test functions that read and write files I've used the [tmp_path fixture](https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html), providing a temporary directory to the test function. Using `tmp_path` has allowed me to paramterize functionality, isolate tests and avoid any side effects of testing. 

## Intent

Purpose of this project is to practice working with and refactoring code. All code in task_manager.py as of initial commit was already provided. I haved extended the functionality of this system, and refactored where appropiate, to improve readability and adopt best practices. TDD approach has been adopted to ensure code quality and behaviour.

## Credits

Code for this application was created by me. Thanks to [Hyperiondev](https://www.hyperiondev.com/) for the project suggestion.

## License

Project is covered by GPL License. Please feel free to modify and use this application.

Thanks for checking out my app! 