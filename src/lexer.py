import re

TOKEN_SPECIFICATION = [
    ('NUMBER', r'\d+'),                         # Integer Numbers
    ('STRING', r'".*?"'),                       # Strings inside double quotes
    ('INPUT', r'pucho'),                        # User Input Operation
    ('VAR_DECL', r'likho'),                     # Variable Declaration
    ('BRIBE', r'ghoos lo'),                     # Bribe Statement
    ('PRINT', r'ghoshna'),                      # Print Statement
    ('OPERATOR', r'me jodo|se ghatao|me guna karo|ka bhag karo|ka shesh bhag karo'), # Arithmetic Operators
    ('INCREMENT', r'badhao'),                   # Increment Operator
    ('DECREMENT', r'ghatao'),                   # Decrement Operator
    ('COMPARISON', r'barabar hai|alag hai|bada hai|chota hai|bada ya barabar hai|chota ya barabar hai'),    # Comparison Operator
    ('CONDITIONAL', r'agar|warna'),             # Conditional Statements
    ('LOOP', r'ginti karo|ginti band'),         # Loops
    ('FILE', r'file kholo|band karo'),          # File Operations
    ('FILE_DECL', r'aur naam do'),              # File Instance Creation
    ('STRUCT_DECL', r'dhacha banao'),           # Structure declaration
    ('STRUCT_INSTANCE', r'aur usko banao'),     # Structure Instance Creation
    ('STRUCT_ACCESS', r'ka'),                   # Access structure properties
    ('BREAK', r'bijli chali gayi'),             # Break statement
    ('RETURN', r'sarkar gir gayi'),             # Return statement
    ('LBRACE', r'\{'),                          # Left brace `{`
    ('RBRACE', r'\}'),                          # Right brace `}`
    ('SKIP_WORD', r'se|toh'),                    # Fancy unnecessary words
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
    ('NEWLINE', r';'),                          # Line Break
    ('SKIP', r'[ \t]+'),                        # Skip spaces and tabs
    ('MISMATCH', r'.')                          # Any other character (invalid)
]

tokenRegex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

def lexer(code):
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
            next_index = i + 1
            while next_index < len(tokenList) and tokenList[next_index].lastgroup in ('SKIP', 'NEWLINE', 'SKIP_WORD'):
                next_index += 1
            next_token = tokenList[i + 1]

            if (next_index < len(tokenList) and tokenList[next_index].lastgroup == 'IDENTIFIER'):
                structName = tokenList[next_index].group('IDENTIFIER')
                structTypes.add(structName)
                tokens.append((kind, value))
                tokens.append(('STRUCT_TYPE', structName))
                i = next_index + 1
                continue

        if (kind == 'STRUCT_INSTANCE' and (i + 1) < len(tokenList)):
            next_index = i + 1
            while next_index < len(tokenList) and tokenList[next_index].lastgroup in ('SKIP', 'NEWLINE', 'SKIP_WORD'):
                next_index += 1
            if next_index < len(tokenList) and tokenList[next_index].lastgroup == 'IDENTIFIER':
                structName = tokenList[next_index].group('IDENTIFIER')
                if structName in structTypes:
                    tokens.append((kind, value))
                    tokens.append(('STRUCT_TYPE', structName))
                    print(f"Instantiating Struct: {structName}")
                    i = next_index + 1
                    continue

        tokens.append((kind, value))
        i += 1
    
    return tokens

if __name__ == '__main__':
    sample_code = """
            dhacha banao TaxPayer {
                likho name;
                likho age;
                likho salary;
            }
            likho tp aur usko banao TaxPayer
        """
    print(lexer(sample_code))
