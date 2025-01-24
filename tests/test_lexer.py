import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.lexer import lexer

class TestLexer (unittest.TestCase):

    def test_user_input(self):
        code = """
            pucho age
        """
        expected_tokens = [
            ('INPUT', 'pucho'),
            ('IDENTIFIER', 'age')
        ]
        self.assertEqual(lexer(code), expected_tokens)

    def test_variable_declaration(self):
        code = """
            likho salary 500000
        """
        expectedTokens = [
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'salary'),
            ('NUMBER', 500000)
        ]

        self.assertEqual(lexer(code), expectedTokens)

    def test_struct_declatation(self):
        code = """
            dhacha banao TaxPayer {
                likho name;
                likho age;
                likho salary;
            }
        """
        expectedTokens = [
            ('STRUCT_DECL', 'dhacha banao'),
            ('STRUCT_TYPE', 'TaxPayer'),
            ('LBRACE', '{'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'name'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'age'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'salary'),
            ('RBRACE', '}')
        ]

        self.assertEqual(lexer(code), expectedTokens)

    def test_struct_instantiation(self):
        code = """
            dhacha banao TaxPayer {
                likho name;
                likho age;
                likho salary;
            }
            likho tp aur usko banao TaxPayer
        """
        expectedTokens = [
            ('STRUCT_DECL', 'dhacha banao'),
            ('STRUCT_TYPE', 'TaxPayer'),
            ('LBRACE', '{'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'name'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'age'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'salary'),
            ('RBRACE', '}'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'tp'),
            ('STRUCT_INSTANCE', 'aur usko banao'),
            ('STRUCT_TYPE', 'TaxPayer')
        ]
        print(lexer(code))
        self.assertEqual(lexer(code), expectedTokens)

    def test_arithmetic_operations(self):
        code = "likho c 10 me jodo 5"
        expectedTokens = [
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 10),
            ('OPERATOR', 'me jodo'),
            ('NUMBER', 5)
        ]

        self.assertEqual(lexer(code), expectedTokens)

        code = "likho c 10 se ghatao 5"
        expectedTokens = [
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 10),
            ('OPERATOR', 'se ghatao'),
            ('NUMBER', 5)
        ]

        self.assertEqual(lexer(code), expectedTokens)

        code = "likho c 10 me guna karo 5"
        expectedTokens = [
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 10),
            ('OPERATOR', 'me guna karo'),
            ('NUMBER', 5)
        ]

        self.assertEqual(lexer(code), expectedTokens)

        code = "likho c 10 ka bhag karo 5"
        expectedTokens = [
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 10),
            ('OPERATOR', 'ka bhag karo'),
            ('NUMBER', 5)
        ]

        self.assertEqual(lexer(code), expectedTokens)

        code = "likho c 10 ka shesh bhag karo 5"
        expectedTokens = [
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 10),
            ('OPERATOR', 'ka shesh bhag karo'),
            ('NUMBER', 5)
        ]

        self.assertEqual(lexer(code), expectedTokens)

    def test_conditional_statement(self):
        code = """
            agar a bada hai 5 se toh {
                likho c 6
            }
            warna {
                agar a chota hai 5 se toh  {
                    likho c 4
                }
                warna {
                    likho c 5
                }
            }
        """
        expectedTokens = [
            ('CONDITIONAL', 'agar'),
            ('IDENTIFIER', 'a'),
            ('COMPARISON', 'bada hai'),
            ('NUMBER', 5),
            ('LBRACE', '{'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 6),
            ('RBRACE', '}'),
            ('CONDITIONAL', 'warna'),
            ('LBRACE', '{'),
            ('CONDITIONAL', 'agar'),
            ('IDENTIFIER', 'a'),
            ('COMPARISON', 'chota hai'),
            ('NUMBER', 5),
            ('LBRACE', '{'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 4),
            ('RBRACE', '}'),
            ('CONDITIONAL', 'warna'),
            ('LBRACE', '{'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'c'),
            ('NUMBER', 5),
            ('RBRACE', '}'),
            ('RBRACE', '}'),
        ]

        self.assertEqual(lexer(code), expectedTokens)

    def test_break_and_return(self):
        code = """
            bijli chali gayi
            sarkar gir gayi
        """

        expectedTokens = [
            ('BREAK', 'bijli chali gayi'),
            ('RETURN', 'sarkar gir gayi')
        ]

        self.assertEqual(lexer(code), expectedTokens)

    def test_print_statement(self):
        code = """
            ghoshna "Hello World" me jodo c me jodo "times"
        """
        expectedTokens = [
            ('PRINT', 'ghoshna'),
            ('STRING', 'Hello World'),
            ('OPERATOR', 'me jodo'),
            ('IDENTIFIER', 'c'),
            ('OPERATOR', 'me jodo'),
            ('STRING', 'times')
        ]

        self.assertEqual(lexer(code), expectedTokens)

    def test_file_operations(self):
        code = """
            file kholo "taxreport.txt" aur naam do taxdata
            taxdata band karo
        """
        expected_tokens = [
            ('FILE', 'file kholo'),
            ('STRING', 'taxreport.txt'),
            ('FILE_DECL', 'aur naam do'),
            ('IDENTIFIER', 'taxdata'),
            ('IDENTIFIER', 'taxdata'),
            ('FILE', 'band karo')
        ]

        self.assertEqual(lexer(code), expected_tokens)

    def test_loops(self):
        code = """
        ginti karo i 1 se 10 tak
            likho i
        ginti band
        """
        expected_tokens = [
            ('LOOP', 'ginti karo'),
            ('IDENTIFIER', 'i'),
            ('NUMBER', 1),
            ('NUMBER', 10),
            ('IDENTIFIER', 'tak'),
            ('VAR_DECL', 'likho'),
            ('IDENTIFIER', 'i'),
            ('LOOP', 'ginti band')
        ]
        self.assertEqual(lexer(code), expected_tokens)

    def test_mismatched_characters(self):
        code = "dhacha banao TaxPayer { ! }"
        with self.assertRaises(SyntaxError):
            lexer(code)

if __name__ == "__main__":
    unittest.main()