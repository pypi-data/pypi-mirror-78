import os

def read_version():
    with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as file:
        return file.read().strip()

__version__ = read_version()
__app_name__ = "sila2codegenerator"
