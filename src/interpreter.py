import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.environment import Environment
from src.utils.bribe_manager import BribeManager

class Interpreter:
    def __init__(self):
        self.env = Environment()
        self.bribeManager = BribeManager()
        self.outputLog = []

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
            self.outputLog.append(f"\nRuntime exception: {e}")
            return "\n".join(self.outputLog)

        return "\n".join(self.outputLog)

    def execute(self, statement):
        """
        Execute a statement based on its type

        Args:
            statement (dict): Dictionary representing statements

        Raises:
            RuntimeError: Raise an error is statement type is not known
        """
        statementType = statement["type"]

        if (statement["type"] not in ["PARICHAY", "BRIBE", "PROGRAM_START", "PROGRAM_END", "INPUT"]):
            self.bribeManager.validate_bribe(statement)

        if (statementType == "PROGRAM_START"):
            pass
        elif (statementType == "PROGRAM_END"):
            pass
        elif (statementType == "INPUT"):
            pass
        elif (statementType == "VAR_DECL"):
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
        elif (statementType == "FILE_WRITE"):
            self.execute_file_write(statement)
        elif statementType == "PARICHAY":
            self.execute_parichay(statement)
        elif statementType == "BRIBE":
            self.execute_bribe(statement)
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

        Raises:
            RuntimeError: File alias is not open
        """
        value = self.evaluate(statement["value"])
        newline = statement.get("newline", True)

        if ("file" in statement):
            fileAlias = statement["file"]
            try:
                fileObject = self.env.files[fileAlias]
                if newline:
                    fileObject.write(value + "\n")
                else:
                    fileObject.write(value)
            except KeyError:
                raise RuntimeError(f"File alias '{fileAlias}' is not open.")
        else:
            if newline:
                self.outputLog.append(value)
            else:
                if (self.outputLog):
                    self.outputLog[-1] += value
                else:
                    self.outputLog.append(value)

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
        self.bribeManager.loop_inc()

        var = statement["variable"]
        start = self.evaluate(statement["start"])
        end = self.evaluate(statement["end"])
        increment = statement.get("increment", 1)
        if (isinstance(increment, dict)):
            increment = self.evaluate(increment)

        if (not isinstance(start, int) or not isinstance(end, int) or not isinstance(increment, int)):
            raise RuntimeError(f"Loop boundaries and increment must be integers. Got: start={start}, end={end}, increment={increment}")

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

        self.bribeManager.loop_dec()

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

    def execute_file_write(self, statement):
        """
        Executes a file write ops

        Args:
            statement (dict): A dictionary representing file write

        Raises:
            RuntimeError: Raise an exception if file alias is not open
        """
        alias = statement["alias"]
        value = self.evaluate(statement["value"])

        try:
            fileObject = self.env.files[alias]
            fileObject.write(value + "\n")
        except KeyError:
            raise RuntimeError(f"File alias '{alias}' is not open.")

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
            RuntimeError: Operator type is unknown

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
            elif (operator == "me jodo"):
                if isinstance(left, str) and not isinstance(right, str):
                    right = str(right)
                elif isinstance(right, str) and not isinstance(left, str):
                    left = str(left)
                return left + right
            elif (operator == "se ghatao"):
                return left - right
            elif (operator == "me guna karo"):
                return left * right
            elif (operator == "ka bhag karo"):
                if (right == 0):
                    raise RuntimeError("Division by zero.")
                return left / right
            elif (operator == "ka shesh bhag karo"):
                if (right == 0):
                    raise RuntimeError("Division by zero.")
                return left % right
            else:
                raise RuntimeError(f"Unknown operator: {operator}")

        exprType = expression["type"]
        if (exprType == "NUMBER"):
            return expression["value"]
        elif (exprType == "STRING"):
            raw_string = expression["value"]

            def replace_placeholder(match):
                var_name = match.group(1)
                return str(self.env.get_variable(var_name))

            import re
            interpolated_string = re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", replace_placeholder, raw_string)
            return interpolated_string
        elif (exprType == "IDENTIFIER"):
            return self.env.get_variable(expression["name"])
        else:
            raise RuntimeError(f"Unknown expression type: {exprType}")

    def execute_parichay(self, statement):
        """
        This function evaluates the parichay or profile of the user
        and updates the required bribe based on parichay.

        Args:
            statement (dict): A dictionary representing the parichay
        """
        profile = statement["profile"]
        self.bribeManager.set_parichay(profile)
        self.bribeManager.update_required_bribe()

    def execute_bribe(self, statement):
        """
        This function evaluates teh bribe amount to be collected

        Args:
            statement (dict): A dictionary representing the bribe amount
        """
        bribeAmount = statement["amount"][1]
        self.bribeManager.collect_bribe(bribeAmount)

if __name__ == "__main__":
    ast = [
        # Variable declaration
        {"type": "VAR_DECL", "variable": "salary", "value": {"type": "NUMBER", "value": 700000}},

        # Nested conditional
        {
            "type": "CONDITIONAL",
            "condition": {
                "left": {"type": "IDENTIFIER", "name": "salary"},
                "operator": "bada hai",
                "right": {"type": "NUMBER", "value": 500000}
            },
            "if": [
                {
                    "type": "CONDITIONAL",
                    "condition": {
                        "left": {"type": "IDENTIFIER", "name": "salary"},
                        "operator": "bada hai",
                        "right": {"type": "NUMBER", "value": 1000000}
                    },
                    "if": [
                        {"type": "PRINT", "value": {"type": "STRING", "value": "Extremely rich!"}}
                    ],
                    "else": [
                        {"type": "PRINT", "value": {"type": "STRING", "value": "Moderately rich."}}
                    ]
                }
            ],
            "else": [
                {"type": "PRINT", "value": {"type": "STRING", "value": "Not rich."}}
            ]
        },

        # Crazyyy loop
        {
            "type": "LOOP",
            "variable": "i",
            "start": {"type": "NUMBER", "value": 1},
            "end": {"type": "NUMBER", "value": 10},
            "increment": 1,
            "body": [
                {
                    "type": "CONDITIONAL",
                    "condition": {
                        "left": {"type": "BINARY_EXPRESSION", 
                                "left": {"type": "IDENTIFIER", "name": "i"},
                                "operator": "ka shesh bhag karo", 
                                "right": {"type": "NUMBER", "value": 2}},
                        "operator": "barabar hai",
                        "right": {"type": "NUMBER", "value": 0}
                    },
                    "if": [
                        {
                            "type": "PRINT",
                            "value": {"type": "STRING", "value": "{i} is even."}
                        }
                    ],
                    "else": [
                        {
                            "type": "PRINT",
                            "value": {"type": "STRING", "value": "{i} is odd."}
                        }
                    ]
                }
            ]
        },

        # File operations
        {"type": "FILE_OPEN", "file_name": "report.txt", "alias": "report"},
        {"type": "PRINT", "value": {"type": "STRING", "value": "Final salary is: 500000"}, "file": "report"},
        {"type": "FILE_CLOSE", "alias": "report"}
    ]

    interpreter = Interpreter()
    interpreter.interpret(ast)