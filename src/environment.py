import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Environment:
    def __init__(self):
        self.variables = {}
        self.structs = {}
        self.files = {}

    def set_variable(self, name, value):
        """
        Sets a variable in the environment

        Args:
            name (str): Name of the variable
            value (Any): value to be assigned to the variable
        """
        self.variables[name] = value

    def get_variable(self, name):
        """
        Find the value of the variable

        Args:
            name (str): Name of the variable

        Raises:
            RuntimeError: Runtime error if variable is not defined

        Returns:
            Any: Return the value of the variable
        """
        if (name not in self.variables):
            raise RuntimeError(f"Variable '{name}' is not defined.")

        return self.variables[name]

    def set_struct(self, name, members):
        """
        Define a new structure

        Args:
            name (str): Name of the structure
            members (dict): A dictionary containing the members of
                            the structure.
        """
        self.structs[name] = members;

    def get_struct(self, name):
        """
        Finds the members of the structure from the environment

        Args:
            name (str): Name of the struct

        Raises:
            RuntimeError: Throws the error if structure is not defined.

        Returns:
            dict: Returns the members of the struct
        """
        if (name not in self.structs):
            raise RuntimeError(f"Struct '{name}' is not defined.")

        return self.structs[name]

    def open_file(self, alias, file_name):
        """
        Open a file and associate it with an alias

        Args:
            alias (str): Alias for the file
            file_name (str): Path of the file

        Raises:
            RuntimeError: Raise an error if alias is already in use
        """
        if (alias in self.files):
            raise RuntimeError(f"File alias '{alias}' is already in use.")

        # TODO: Check if file exists else raise an exception

        self.files[alias] = open(file_name, 'w')

    def close_file(self, alias):
        """
        Close the mentioned file

        Args:
            alias (str): Alias for the file

        Raises:
            RuntimeError: If the alias is not associated with file
        """
        if (alias not in self.files):
            raise RuntimeError(f"File alias '{alias}' is not open.")

        self.files[alias].close()
        del self.files[alias]