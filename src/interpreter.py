import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.environment import Environment

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def interpret(self, ast):
        """
        Interprets and execute a list of statement (AST)

        Args:
            ast (list): List of statement from AST

        Raises:
            RuntimeError: Raises an exception if an error occurs during interpretation
        """
        try:
            for statement in ast:
                self.execute(statement)
        except RuntimeError as e:
            print(f"Runtime Error: {str(e)}")
            sys.exit(1)

    def execute(self, statement):
        """
        Execute a statement based on its type

        Args:
            statement (dict): Dictionary representing statements

        Raises:
            RuntimeError: Raise an error is statement type is not known
        """
        statementType = statement["type"]

        if (statementType == "VAR_DECL"):
            self.execute_var_decl(statement)
        elif (statementType == "PRINT"):
            self.execute_print(statement)
        elif (statementType == "CONDITIONAL"):
            self.execute_conditional(statement)
        elif (statementType == "LOOP"):
            self.execute_loop(statement)
        elif (statementType == "STRUCT_DECL"):
            self.execute_struct_decl(statement)
        elif (statementType == "STRUCT_INSTANCE"):
            self.execute_struct_instance(statement)
        elif (statementType == "FILE_OPEN"):
            self.execute_file_open(statement)
        elif (statementType == "FILE_CLOSE"):
            self.execute_file_close(statement)
        else:
            raise RuntimeError(f"Unknown statement type: {statementType}")

    def execute_var_decl(self, statement):
        """
        Execute a variable declaration statement

        Args:
            statement (dict): A dictionary representing variable declaration
        """
        var = statement["variable"]
        value = self.evaluate(statement["value"]) if statement["value"] else None
        self.env.set_variable(var, value)

    def execute_print(self, statement):
        """
        Executes a print statement

        Args:
            statement (dict): A dictionary representing print statement
        """
        value = self.evaluate(statement["value"])
        print(value)

    def execute_conditional(self, statement):
        """
        Execute conditional if - else statement

        Args:
            statement (dict): A dictionary representing conditional statement

        Raises:
            RuntimeError: If the "if" branch is missing when the condition evaluates to True.
        """
        condition = self.evaluate(statement["condition"])
        if (condition):
            if ("if" in statement and statement["if"]):
                for s in statement["if"]:
                    self.execute(s)
            else:
                raise RuntimeError("Missing 'if' branch in conditional.")
        elif ("else" in statement and statement["else"]):
            for s in statement["else"]:
                self.execute(s)
        else:
            pass

    def execute_loop(self, statement):
        """
        execute a loop statement

        Args:
            statement (dict): A dictionary representing loop statement
        """
        var = statement["variable"]
        start = self.evaluate(statement["start"])
        end = self.evaluate(statement["end"])
        increment = statement.get("increment", 1)

        self.env.set_variable(var, start)
        if (increment > 0):
            while (self.env.get_variable(var) <= end):
                for s in statement["body"]:
                    self.execute(s)
                self.env.set_variable(var, self.env.get_variable(var) + increment)
        else:
            while (self.env.get_variable(var) >= end):
                for s in statement["body"]:
                    self.execute(s)
                self.env.set_variable(var, self.env.get_variable(var) + increment)

    def execute_struct_decl(self, statement):
        """
        Execute struct declatation statement

        Args:
            statement (dict): A dictionary representing struct declaration
        """
        name = statement["struct_details"]
        fields = statement["members"]
        self.env.set_struct(name, fields)

    def execute_struct_instance(self, statement):
        """
        Execute the creation of the struct instance

        Args:
            statement (dict): A dictionary representing struct instance
                            creation
        Raises:
            RuntimeError: Raise an exception of undefined struct
        """
        instanceName = statement["instance_name"]
        structType = statement["struct_type"]

        structFields = self.env.get_struct(structType)

        if (structFields is None):
            raise RuntimeError(f"Struct '{structType}' is not defined.")

        instance = {field: None for field in structFields}
        self.env.set_variable(instanceName, instance)

    def execute_file_open(self, statement):
        """
        Executes the file open statement

        Args:
            statement (dict): A dictionary representing file open ops

        Raises:
            RuntimeError: If the file does not exist.
            RuntimeError: If the alias is already in use or any other environment-related error occurs.
        """
        fileName = statement["file_name"]
        alias = statement["alias"]
        try:
            self.env.open_file(alias, fileName)
        except FileNotFoundError:
            raise RuntimeError(f"File '{fileName}' not found.")
        except RuntimeError as e:
            raise RuntimeError(str(e))

    def execute_file_close(self, statement):
        """
        Executes a file close ops

        Args:
            statement (dict): A dictionary representing file close ops

        Raises:
            RuntimeError: If the alias is not associated with an open file.
        """
        alias = statement["alias"]
        try:
            self.env.close_file(alias)
        except RuntimeError as e:
            raise RuntimeError(str(e))

    def evaluate(self, expression):
        """
        This function evaluates a given expression and returns the result

        Args:
            expression (dict): A dictionary representing the expression

        Raises:
            RuntimeError: Expression type is unknown
            RuntimeError: If division by 0 occurs

        Returns:
            Any: Result of evaluated expressions
        """
        if (not expression):
            return None

        if ("left" in expression and "operator" in expression and "right" in expression):
            left = self.evaluate(expression["left"])
            right = self.evaluate(expression["right"])
            operator = expression["operator"]

            if (operator == "bada hai"):
                return left > right
            elif (operator == "chota hai"):
                return left < right
            elif (operator == "barabar hai"):
                return left == right
            elif (operator == "alag hai"):
                return left != right
            elif (operator == "bada ya barabar hai"):
                return left >= right
            elif (operator == "chota ya barabar hai"):
                return left <= right
            else:
                raise RuntimeError(f"Unknown operator: {operator}")

        exprType = expression["type"]
        if (exprType == "NUMBER"):
            return expression["value"]
        elif (exprType == "STRING"):
            return expression["value"]
        elif (exprType == "IDENTIFIER"):
            return self.env.get_variable(expression["name"])
        elif (exprType == "BINARY_EXPRESSION"):
            left = self.evaluate(expression["left"])
            right = self.evaluate(expression["right"])
            operator = expression["operator"]

            if (operator == "me jodo"):
                return left + right
            elif (operator == "se ghatao"):
                return left - right
            elif (operator == "me guna karo"):
                return left * right
            elif (operator == "ka bhag karo"):
                if (right == 0):
                    raise RuntimeError("Division by zero.")
                return left / right
        else:
            raise RuntimeError(f"Unknown expression type: {exprType}")


if __name__ == "__main__":
    ast = ast = [
        {"type": "VAR_DECL", "variable": "x", "value": {"type": "NUMBER", "value": 10}},
        {"type": "VAR_DECL", "variable": "y", "value": {"type": "NUMBER", "value": 0}},
        {"type": "CONDITIONAL",
            "condition": {"left": {"type": "IDENTIFIER", "name": "x"}, "operator": "chota hai", "right": {"type": "NUMBER", "value": 5}},
            "if": [{"type": "PRINT", "value": {"type": "STRING", "value": "x is less than 5"}}],
            "else": [{"type": "PRINT", "value": {"type": "STRING", "value": "x is not less than 5"}}]
        },
        {"type": "LOOP",
            "variable": "i",
            "start": {"type": "NUMBER", "value": 1},
            "end": {"type": "NUMBER", "value": 5},
            "increment": 1,
            "body": [{"type": "PRINT", "value": {"type": "IDENTIFIER", "name": "i"}}]
        },
        {"type": "STRUCT_DECL", "struct_details": "Person", "members": ["name", "age"]},
        {"type": "STRUCT_INSTANCE", "instance_name": "p1", "struct_type": "Person"}
    ]

    interpreter = Interpreter()
    interpreter.interpret(ast)