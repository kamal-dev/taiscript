import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.token_utils import TokenUtils

class Parser:
    def __init__(self, tokens):
        self.utils = TokenUtils(tokens)

    def parse(self):
        """
        This is the entry point for parsing TaiScript program.

        Returns:
            list: This code returns an Abstract Syntax Tree.

        Raises:
            SyntaxError: If program ends without 'yojna band'
        """
        ast = []

        if (self.utils.match("YOJNA_START")):
            program_name = self.utils.consume("STRING", "Expected program name after 'yojna shuru'.")
            ast.append({"type": "PROGRAM_START", "name": program_name})

        while (not self.utils.is_at_end()):
            ast.append(self.parse_statement())

        if (not any(node["type"] == "PROGRAM_END" for node in ast)):
            raise SyntaxError("Program must end with 'yojna band'.")

        return ast

    def parse_statement(self):
        """
        This function parses the statement based on the current token.

        This method identifies the type of statement (e.g., variable
        declaration, conditional, loop) and delegates further parsing
        to the appropriate method.

        Raises:
            SyntaxError: In case if there are any unexpected tokens,
                        raise a Syntax error

        Returns:
            dict: This funtion returns a dictionary where the 'type' key
                is the type of statement and other key store details
                like related to the statement type.
        """
        if (self.utils.match("STRUCT_DECL")):
            return self.parse_struct_declaration()
        elif self.utils.match("VAR_DECL"):
            if (self.utils.check_next("STRUCT_INSTANCE")):
                return self.parse_struct_instance()
            else:
                return self.parse_variable_declaration()
        elif (self.utils.check("IDENTIFIER") and self.utils.check_next("FILE_WRITE")):
            return self.parse_file_write()
        elif (self.utils.match("INPUT")):
            return self.parse_input()
        elif (self.utils.match("FILE_OPEN") or self.utils.match("FILE_CLOSE")):
            return self.parse_file_operation()
        elif (self.utils.match("PARICHAY")):
            return self.parse_parichay()
        elif (self.utils.match("BRIBE")):
            return self.parse_bribe()
        elif (self.utils.match("PRINT")):
            return self.parse_print_statement()
        elif (self.utils.match("CONDITIONAL")):
            return self.parse_conditional()
        elif (self.utils.match("LOOP_START")):
            return self.parse_loop()
        elif (self.utils.match("BREAK")):
            return {"type": "BREAK"}
        elif (self.utils.match("RETURN")):
            return {"type", "RETURN"}
        elif self.utils.match("YOJNA_END"):
            return {"type": "PROGRAM_END"}
        else:
            raise SyntaxError(f'Unexpected token: {self.utils.peek()}')

    def parse_variable_declaration(self):
        """
        Extracts the variable name from variable declaration and
        assigns value if any.

        Returns:
            dict: Returns dictionary containing type, variable and value
        """
        variable = self.utils.consume("IDENTIFIER", "Expected variable name after 'likho'.")[1]
        value = None
        if (not self.utils.is_at_end()):
            value = self.parse_expression()

        return {"type": "VAR_DECL", "variable": variable, "value": value}

    def parse_struct_declaration(self):
        """
        Extracts the structure's name and its members (fields).

        Returns:
            dict: Returns a dictionary containing type, name of the
            structure and its members
        """
        structDetails = self.utils.consume("STRUCT_TYPE", "Expected structure name.")[1]
        self.utils.consume("LCBRACE", "Expected '{' after structure name.")
        members = []
        while (not self.utils.check("RCBRACE") and not self.utils.is_at_end()):
            self.utils.consume("VAR_DECL", "Expected a variable declaration keywork")
            members.append(self.utils.consume("IDENTIFIER", "Expected field name.")[1])
        self.utils.consume("RCBRACE", "Expected '}' after structure fields.")

        return {"type": "STRUCT_DECL", "struct_details": structDetails, "members": members}

    def parse_struct_instance(self):
        """
        Extracts the instance name and the type of structure being instantiated.

        Returns:
            dict: Returns type, name of the instance and name of the struct
        """
        instanceName = self.utils.consume("IDENTIFIER", "Expected variable name for the instance.")[1]
        self.utils.consume("STRUCT_INSTANCE", "Expected 'aur usko banao' for structure instantiation.")
        structType = self.utils.consume("STRUCT_TYPE", "Expected structure type after 'aur usko banao'.")[1]

        return {
            "type": "STRUCT_INSTANCE",
            "instance_name": instanceName,
            "struct_type": structType
        }

    def parse_input(self):
        """
        Associates a variable for a user provided input.

        Returns:
            dict: Returns type and name of the variable
        """
        name = self.utils.consume("IDENTIFIER", "Expected a variable name for input.")[1]
        return {"type": "INPUT", "name": name}

    def parse_file_operation(self):
        """
        Parses file opening and file closing operations.

        For file opening, it extracts the file name and alias.
        For file closing, it extracts the alias of the file to be closed.

        Returns:
            dict: Returns type of operation, file name (only in case of file opening), alias
        """
        operation = self.utils.previous()[1]
        if (operation == "file kholo"):
            fileName = self.utils.consume("STRING", "Expected a file name after 'file kholo'.")[1]
            self.utils.consume("FILE_DECL", "Expected 'aur naam do' for file declaration.")
            alias = self.utils.consume("IDENTIFIER", "Expected file alias for this file.")[1]
            return {"type": "FILE_OPEN", "file_name": fileName, "alias": alias}
        elif (operation == "band karo"):
            alias = self.utils.consume("IDENTIFIER", "Expected file alias to close.")[1]
            return {"type": "FILE_CLOSE", "alias": alias}

    def parse_file_write(self):
        """
        Parses a file write statement

        Returns:
            dict: Returns the type of operation, alias of the file and the value to be written.
        """
        alias = self.utils.consume("IDENTIFIER", "Expected file alias before 'me likho'.")[1]
        self.utils.consume("FILE_WRITE", "Expected 'me likho'.")
        value = self.parse_expression()
        return {"type": "FILE_WRITE", "alias": alias, "value": value}

    def parse_parichay(self):
        """
        Parses the parichay string

        Returns:
            dict: Returns the type of operation, and profile type
        """
        profile = self.utils.consume("STRING", "Expected parichay description.")[1]
        return {"type": "PARICHAY", "profile": profile}

    def parse_bribe(self):
        """
        Extracts the amount of bribe

        Returns:
            dict: Returns type of operation and bribe amount
        """
        amount = self.utils.consume("NUMBER", "Expected bribe amount after 'ghoos lo'.")
        return {
            "type": "BRIBE",
            "amount": amount,
        }

    def parse_expression(self):
        """
        Supports numbers, strings, identifiers, and binary operations.
        Handles operators and evaluates expressions in a
        left to right order.

        Raises:
            SyntaxError: Operator found without a preceding operand.
            SyntaxError: Unexpected token in the expression
            SyntaxError: Unexpected end after the given operator

        Returns:
            dict: A dictionary containing type, value, name and details of binary
                expressions
        """
        left = None
        if (self.utils.match("NUMBER")):
            left = {"type": "NUMBER", "value": self.utils.previous()[1]}
        elif (self.utils.match("STRING")):
            left = {"type": "STRING", "value": self.utils.previous()[1]}
        elif (self.utils.match("IDENTIFIER")):
            left = {"type": "IDENTIFIER", "name": self.utils.previous()[1]}
        elif self.utils.check("OPERATOR"):
            raise SyntaxError("Operator found without a preceding operand.")
        else:
            if self.utils.check("RCBRACE"):
                return None
            raise SyntaxError(f"Unexpected token in expression: {self.utils.peek()}")

        while self.utils.match("OPERATOR"):
            operator = self.utils.previous()[1]

            if self.utils.is_at_end() or self.utils.check("RCBRACE") or self.utils.check("LOOP"):
                raise SyntaxError(f"Unexpected end of expression after operator '{operator}'.")

            right = self.parse_expression()
            left = {
                "type": "BINARY_EXPRESSION",
                "operator": operator,
                "left": left,
                "right": right,
            }

        return left

    def parse_print_statement(self):
        """
        Extracts the expression to be printed.

        Returns:
            dict: Returns type of operation and the value to be printed
        """
        value = self.parse_expression()
        newline = True
        if (self.utils.match("NO_NEWLINE")):
            newline = False

        return {"type": "PRINT", "value": value, "newline": newline}

    def parse_conditional(self):
        """
        Extracts the if-else branch

        Returns:
            dict: Returns type of operation, condition, if branch and else branch.
        """
        left = self.parse_expression()
        operator = self.utils.consume("COMPARISON", "Expected a comparison operator.")[1]
        right = self.parse_expression()

        condition = {"left": left, "operator": operator, "right": right}

        self.utils.consume("LCBRACE", "Expected '{' after condition.")
        ifBranch = []
        while (not self.utils.check("RCBRACE") and not self.utils.is_at_end()):
            ifBranch.append(self.parse_statement())

        self.utils.consume("RCBRACE", "Expected '}' after if branch.")

        elseBranch = None
        if (self.utils.match("CONDITIONAL") and self.utils.previous()[1] == "warna"):
            self.utils.consume("LCBRACE", "Expected '{' after 'warna'.")
            elseBranch = []
            while (not self.utils.check("RCBRACE") and not self.utils.is_at_end()):
                elseBranch.append(self.parse_statement())

            self.utils.consume("RCBRACE", "Expected '}' after else branch.")

        return {
            "type": "CONDITIONAL",
            "condition": condition,
            "if": ifBranch,
            "else": elseBranch
        }

    def parse_loop(self):
        """
        Extracts the loop variable, range (start, end, increment), and body.

        Raises:
            SyntaxError: Expected end value

        Returns:
            dict: Returns type of op, loop variable, start, end, increement
                and body of loop
        """
        loopVariable = self.utils.consume("IDENTIFIER", "Expected a loop variable")[1]
        start = {"type": "NUMBER", "value": self.utils.consume("NUMBER", "Expected start value")[1]}

        if (self.utils.match("NUMBER")):
            end = {"type": "NUMBER", "value": self.utils.previous()[1]}
        elif (self.utils.match("IDENTIFIER")):
            end = {"type": "IDENTIFIER", "name": self.utils.previous()[1]}
        else:
            raise SyntaxError("Expected end value (number or identifier).")

        increment = {"type": "NUMBER", "value": 1}
        if (self.utils.match("INCREMENT")):
            increment = {"type": "NUMBER", "value": self.utils.consume("NUMBER", "Expected increment value")[1]}
        elif (self.utils.match("DECREMENT")):
            increment = {"type": "NUMBER", "value": (-1*self.utils.consume("NUMBER", "Expected increment value")[1])}

        self.utils.consume("LCBRACE", "Expected '{' for loop body.")
        body = []
        while not self.utils.check("RCBRACE") and not self.utils.is_at_end():
            body.append(self.parse_statement())
        self.utils.consume("RCBRACE", "Expected '}' after loop body.")
        self.utils.consume("LOOP_END", "Expected 'ginti band' after loop body.")

        return {
            "type": "LOOP",
            "variable": loopVariable,
            "start": start,
            "end": end,
            "increment": increment,
            "body": body,
        }

if __name__ == "__main__":
    tokens = [
            ('FILE_OPEN', 'file kholo'),
            ('STRING', 'taxreport.txt'),
            ('FILE_DECL', 'aur naam do'),
            ('IDENTIFIER', 'taxdata'),
            ('FILE_CLOSE', 'band karo'),
            ('IDENTIFIER', 'taxdata')
        ]
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)