import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.parser import Parser

class TestParser(unittest.TestCase):
    def test_variable_declaration(self):
        tokens = [
            ('VAR_DECL', 'likho'), ('IDENTIFIER', 'salary'), ('NUMBER', 500000)
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {'type': 'VAR_DECL', 'variable': 'salary', 'value': {'type': 'NUMBER', 'value': 500000}}
        ])

    def test_struct_declaration(self):
        tokens = [
            ('STRUCT_DECL', 'dhacha banao'), ('STRUCT_TYPE', 'TaxPayer'), ('LCBRACE', '{'),
            ('VAR_DECL', 'likho'), ('IDENTIFIER', 'name'),
            ('VAR_DECL', 'likho'), ('IDENTIFIER', 'age'),
            ('RCBRACE', '}')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {
                'type': 'STRUCT_DECL',
                'struct_details': 'TaxPayer',
                'members': ['name', 'age']
            }
        ])

    def test_struct_instance(self):
        tokens = [
            ('VAR_DECL', 'likho'), ('IDENTIFIER', 'tp'),
            ('STRUCT_INSTANCE', 'aur usko banao'), ('STRUCT_TYPE', 'TaxPayer')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {
                'type': 'STRUCT_INSTANCE',
                'instance_name': 'tp',
                'struct_type': 'TaxPayer'
            }
        ])

    def test_print_statement(self):
        tokens = [
            ('PRINT', 'ghoshna'), ('STRING', 'Hello, World!')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {'type': 'PRINT', 'value': {'type': 'STRING', 'value': 'Hello, World!'}}
        ])

    def test_conditional_statement(self):
        tokens = [
            ('CONDITIONAL', 'agar'), ('IDENTIFIER', 'salary'), ('COMPARISON', 'bada hai'), ('NUMBER', 500000),
            ('LCBRACE', '{'),
            ('PRINT', 'ghoshna'), ('STRING', 'Rich person detected!'),
            ('RCBRACE', '}'),
            ('CONDITIONAL', 'warna'), ('LCBRACE', '{'),
            ('PRINT', 'ghoshna'), ('STRING', 'Not rich!'),
            ('RCBRACE', '}')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {
                'type': 'CONDITIONAL',
                'condition': {
                    'left': {'type': 'IDENTIFIER', 'name': 'salary'},
                    'operator': 'bada hai',
                    'right': {'type': 'NUMBER', 'value': 500000}
                },
                'if': [
                    {'type': 'PRINT', 'value': {'type': 'STRING', 'value': 'Rich person detected!'}}
                ],
                'else': [
                    {'type': 'PRINT', 'value': {'type': 'STRING', 'value': 'Not rich!'}}
                ]
            }
        ])

    def test_loop(self):
        tokens = [
            ('LOOP_START', 'ginti karo'), ('IDENTIFIER', 'i'), ('NUMBER', 1), ('NUMBER', 10),
            ('LCBRACE', '{'),
            ('PRINT', 'ghoshna'), ('IDENTIFIER', 'i'),
            ('RCBRACE', '}'),
            ('LOOP_END', 'ginti band')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {
                'type': 'LOOP',
                'variable': 'i',
                'start': 1,
                'end': 10,
                'increment': 1,
                'body': [
                    {'type': 'PRINT', 'value': {'type': 'IDENTIFIER', 'name': 'i'}}
                ]
            }
        ])

    def test_file_operations(self):
        tokens = [
            ('FILE_OPEN', 'file kholo'), ('STRING', 'data.txt'),
            ('FILE_DECL', 'aur naam do'), ('IDENTIFIER', 'file_data'),
            ('FILE_CLOSE', 'band karo'), ('IDENTIFIER', 'file_data')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {'type': 'FILE_OPEN', 'file_name': 'data.txt', 'alias': 'file_data'},
            {'type': 'FILE_CLOSE', 'alias': 'file_data'}
        ])

    def test_user_input(self):
        tokens = [
            ('INPUT', 'pucho'), ('IDENTIFIER', 'user_input')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast, [
            {'type': 'INPUT', 'name': 'user_input'}
        ])

if __name__ == "__main__":
    unittest.main()