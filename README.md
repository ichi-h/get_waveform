# py_init2

This template uses [pipenv](https://pipenv.pypa.io/en/latest/) and assumes that it will be used with VSCode.  
Also, install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) beforehand.

## Usage

### 1. Clone repository

```
git clone https://github.com/ippee/py_init.git project_name
```

### 2. Initialize repository

Delete the Git repository that already exists and create a new one.

```
cd ./project_name

# Windows
Remove-Item -Recurse -Force ./.git

# Linux/Mac
rm -rf ./.git

git init
```

### 3. Create virtual environment

```
pipenv --python 3.9 # set your python version
```

Then, open the project using VSCode.

```
code .
```

### 4. Select interpreter

Open the command palette (Win/Linux: "Ctrl + Shift + P", Mac: "Command + Shift + P") and select `Python: Select Interpreter`, then select the recommended interpreter. (If it is not exist, enter the path of the interpreter in the virtual environment.)

### 5. Install packages

Install the packages you need in the working directory.

`pipenv install [package_name]`

## Tasks

In this template, the frequently used commands are registered in tasks.json.

- Install
  - Install all the packages written in the Pipfile.
- Run
  - Run ./src/main.py.
- Test
  - Runs all the tests in the tests directory.

## License

This repository is published under CC0 1.0 Universal.  
When you start your project from this repository, replace the license with the one you like.
