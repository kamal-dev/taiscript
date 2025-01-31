import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import lexer
from src.parser import Parser
from src.interpreter import Interpreter


def run_taiscript_from_string(input_text):
    """
    Runs TaiScript code from a string input by tokenizing, parsing, and interpreting the code.

    Args:
        input_text (str): TaiScript code as a string.
    """
    try:
        # Tokenize the input text
        tokens = lexer(input_text)

        # Parse the tokens into an Abstract Syntax Tree (AST)
        parser = Parser(tokens)
        ast = parser.parse()

        # Interpret the AST
        interpreter = Interpreter()
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)