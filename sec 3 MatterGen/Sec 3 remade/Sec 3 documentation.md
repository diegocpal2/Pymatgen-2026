# Sec 3 Documentation

# Virtual environment installation instructions

## Step 1

Install Python 3.12 with you preferred method of choice. You may use the [Python Release Links](https://www.python.org/downloads/release/python-3120/) to download the desired version such as using the Windows installer or macOS installers within the link, or for UNIX-based systems you may use the corresponding command. The specific version used in development was 3.12.14, but any stable release should work. 

The following is an example for Ubuntu:
```
sudo apt install python3.12
```

## Step 2

Open the IDE of your preference (VS Code recommended) and create a virtual environment for the project using Python 3.12 as the version with which this is initialized. This may be done within the IDE's functions, such as using Ctrl+Shift+P for VSCode, and searching for the "Python: Create Environment..." option. Find the correct python version and create it. If using this method, it is preferred that one opens the folder that you will be working on ('Sec 3 Remade' for now) before doing this process. If using the terminal window, also open the folder directory where the virtual environment will be initialized and run the correct command for initializing the virtual environment. 

An example for initializing the environment, the 'Sec3venv' name after the dot can be changed:
```
python3.12 -m venv .Sec3venv
```

## Step 3

Activate the virtual environment. This may be done opening an instance of the environment from the run button, but this may cause issues if there is a default Python version installed. It is preferred if this step is done from the command line. Navigate to the folder where your virtual environment is held (the parent folder of the .Sec3venv folder) and run the correct command as below. (NEEDS TESTING ON OTHER USERS TO SEE IF THEY CAN FOLLOW PROCEDURE)

For Windows:
```
.Sec3venv/Source/activate
```

For POSIX-compliant systems:
```
source .Sec3venv/bin/activate
```

## Step 4

With this virtual environment activated (you should see a .Sec3venv in front of the path in the terminal) you may run the script_execution.py script from this instance. Navegate to the directory where this script is held (currently inside: "sec 3 mattergen/Sec 3 Remade/script_execution.py"). Examples below:

For Windows:
```
script_execution.py
```
or maybe:
```
.\script_execution.py
```

For POSIX-based:
```
python script_execution.py
```

Please investigate what works. This should run a list of commands to finish the last of the setup for you.

## Documentation of last setup script

### main

```
if __name__ == "__main__":
    """
    Run processes that uninstall and reinstall specific dependencies 
    because the versioning of these must be corrected to avoid issues.
            
    Returns:
        None
    """
```

### SectionCommands

__init__
```
    def __init__(self):
        """
        Initialize a parser object for usage in parsing command line arguments.
        """
```

### CMD_Scripts class

__init__
```
def __init__(self) -> None:
        """
        Initialize list-of-strings values for all commands to be run for 
        project setup. 
        """
```

```
    def install_pymatgen(self) -> None:
        """
        Run a process to install the following dependencies:
        install
        pymatgen
        mp_api
        emmet-core
        py3Dmol
        hydra-core
        pytorch-lightning==2.0.6
        fire 
        ase
        numpy==1.26.4 

        Returns:
            None
        """
```

```
    def uninstall_reinstall_modules(self) -> None:
        """
        Run processes that uninstall and reinstall specific dependencies 
        because the versioning of these must be corrected to avoid issues.

        Returns:
            None
        """
```

```
    def clone_and_install_mattergen(self) -> None:
        """
        Run processes that copy the mattergen repository from github
        and modify the installation to reflect changes in editable format.
            
        Returns:
            None
        """
```

```

```


# Documentation of tutorial

## aqui va lo que se haga de completar el tutorial