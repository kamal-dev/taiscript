import re

TOKEN_SPECIFICATION = [
    ('YOJNA_START', r'yojna shuru'),            # Start of the program
    ('YOJNA_END', r'yojna band'),               # End of the program
    ('NUMBER', r'\d+'),                         # Integer Numbers
    ('STRING', r'".*?"'),                       # Strings inside double quotes
    ('INPUT', r'pucho'),                        # User Input Operation
    ('VAR_DECL', r'likho'),                     # Variable Declaration
    ('BRIBE', r'ghoos lo'),                     # Bribe Statement
    ('PRINT', r'ghoshna'),                      # Print Statement
    ('NO_NEWLINE', r'lagatar'),                 # Modifier for no newline
    ('OPERATOR', r'me jodo|se ghatao|me guna karo|ka bhag karo|ka shesh bhag karo'), # Arithmetic Operators
    ('INCREMENT', r'badhao'),                   # Increment Operator
    ('DECREMENT', r'ghatao'),                   # Decrement Operator
    ('COMPARISON', r'barabar hai|alag hai|bada hai|chota hai|bada ya barabar hai|chota ya barabar hai'),    # Comparison Operator
    ('CONDITIONAL', r'agar|warna'),             # Conditional Statements
    ('LOOP_START', r'ginti karo'),              # Loop Start
    ('LOOP_END', r'ginti band'),                # Loop End
    ('FILE_OPEN', r'file kholo'),               # File Operations
    ('FILE_CLOSE', r'band karo'),               # File Operations
    ('FILE_WRITE', r'me likho'),                # File Write Operation
    ('FILE_DECL', r'aur naam do'),              # File Instance Creation
    ('STRUCT_DECL', r'dhacha banao'),           # Structure declaration
    ('STRUCT_INSTANCE', r'aur usko banao'),     # Structure Instance Creation
    ('STRUCT_ACCESS', r'ka'),                   # Access structure properties
    ('BREAK', r'bijli chali gayi'),             # Break statement
    ('RETURN', r'sarkar gir gayi'),             # Return statement
    ('LCBRACE', r'\{'),                         # Left curly brace `{`
    ('RCBRACE', r'\}'),                         # Right curly brace `}`
    ('LRBRACE', r'\('),                         # Left round brace `(`
    ('RRBRACE', r'\)'),                         # Right roundbrace `)`
    ('SKIP_WORD', r'se|toh|tak|aur'),           # Fancy unnecessary words
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
    ('NEWLINE', r';'),                          # Line Break
    ('SKIP', r'[ \t]+'),                        # Skip spaces and tabs
    ('MISMATCH', r'.')                          # Any other character (invalid)
]

tokenRegex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

def lexer(code):
    """
    This function is used to tokenize the input tai code.

    Args:
        code (str): The tai code is taken as string by the lexer()

    Raises:
        SyntaxError: In case if there are any unwanted characters in
                    the code, it raises a Syntax Error exception.

    Returns:
        list: Returns a 2D list containing the kind of
            token and the token.
    """
    tokens = []
    structTypes = set()
    tokenIter = re.finditer(tokenRegex, code)
    tokenList = list(tokenIter)
    i = 0

    while i < len(tokenList):
        kind = tokenList[i].lastgroup
        value = tokenList[i].group(kind)
        if (kind == 'NUMBER'):
            value = int(value)
        elif (kind == 'STRING'):
            value = value.strip('"')
        elif (kind in ('SKIP', 'NEWLINE', 'SKIP_WORD')):
            i += 1
            continue
        elif (kind == 'MISMATCH'):
            raise SyntaxError(f'Unexpected character: {value}')

        if (kind == 'STRUCT_DECL' and (i+1) < len(tokenList)):
            nextIndex = i + 1
            while nextIndex < len(tokenList) and tokenList[nextIndex].lastgroup in ('SKIP', 'NEWLINE', 'SKIP_WORD'):
                nextIndex += 1
            next_token = tokenList[i + 1]

            if (nextIndex < len(tokenList) and tokenList[nextIndex].lastgroup == 'IDENTIFIER'):
                structName = tokenList[nextIndex].group('IDENTIFIER')
                structTypes.add(structName)
                tokens.append((kind, value))
                tokens.append(('STRUCT_TYPE', structName))
                i = nextIndex + 1
                continue

        if (kind == 'STRUCT_INSTANCE' and (i + 1) < len(tokenList)):
            nextIndex = i + 1
            while nextIndex < len(tokenList) and tokenList[nextIndex].lastgroup in ('SKIP', 'NEWLINE', 'SKIP_WORD'):
                nextIndex += 1
            if nextIndex < len(tokenList) and tokenList[nextIndex].lastgroup == 'IDENTIFIER':
                structName = tokenList[nextIndex].group('IDENTIFIER')
                if structName in structTypes:
                    tokens.append((kind, value))
                    tokens.append(('STRUCT_TYPE', structName))
                    i = nextIndex + 1
                    continue

        tokens.append((kind, value))
        i += 1
    
    return tokens

if __name__ == '__main__':
    sampleCode = """
            dhacha banao TaxPayer {
                likho name;
                likho age;
                likho salary;
            }
            likho tp aur usko banao TaxPayer
        """
    print(lexer(sampleCode))
