#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import lexer
from src.parser import Parser
from src.interpreter import Interpreter


def run_taiscript(file_path):
    """
    Runs a TaiScript file by tokenizing, parsing, and interpreting the code.

    Args:
        file_path (str): Path to the TaiScript file.
    """
    if (not os.path.exists(file_path)):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    with open(file_path, 'r') as file:
        code = file.read()

    try:
        tokens = lexer(code)
 #       print("\nTokens:")
 #       for token in tokens:
 #           print(token)

        parser = Parser(tokens)
        ast = parser.parse()
#        print("\nAbstract Syntax Tree (AST):")
#        for node in ast:
#            print(node)

#        print("\nOutput:")
        interpreter = Interpreter()
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: ./scripts/run_taiscript <path_to_file.tai>")
        sys.exit(1)

    run_taiscript(sys.argv[1])
