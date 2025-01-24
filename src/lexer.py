import re

TOKEN_SPECIFICATION = [
    ('NUMBER', r'\d+'),                         # Integer Numbers
    ('STRING', r'".*?"'),                       # Strings inside double quotes
    ('VAR_DECL', r'likho'),                     # Variable Declaration
    ('BRIBE', r'ghoos lo'),                     # Bribe Statement
    ('PRINT', r'ghoshna'),                      # Print Statement
    ('OPERATOR', r'me jodo|se ghatao|me guna karo|ka shesh bhag karo'), # Arithmetic Operators
    ('INCREMENT', r'badhao'),                   # Increment Operator
    ('DECREMENT', r'ghatao'),                   # Decrement Operator
    ('COMPARISON', r'barabar hai|alag hai|bada hai|chota hai|bada ya barabar hai|chota ya barabar hai'),    # Comparison Operator
    ('CONDITIONAL', r'alag|warna'),             # Conditional Statements
    ('LOOP', r'ginti karo|ginti band'),         # Loops
    ('FILE', r'file kholo|band karo'),          # File Operations
    ('STRUCT_DECL', r'dhacha banao'),           # Structure declaration
    ('STRUCT_INSTANCE', r'aur usko banao'),     # Structure Instance Creation
    ('STRUCT_ACCESS', r'ka'),                   # Access structure properties
    ('BREAK', r'bijli chali gayi'),             # Break statement
    ('RETURN', r'sarkar gir gayi'),             # Return statement
    ('LBRACE', r'\{'),                          # Left brace `{`
    ('RBRACE', r'\}'),                          # Right brace `}`
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
    ('NEWLINE', r';'),                          # Line Break
    ('SKIP_WORD', r'se|toh'),                    # Fancy unnecessary words
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
        elif (kind == 'SKIP' or kind == 'NEWLINE'):
            i += 1
            continue
        elif (kind == 'SKIP_WORD'):
            i += 1
        elif (kind == 'MISMATCH'):
            raise SyntaxError(f'Unexpected character: {value}')
        
        # For Tracking structure declaration
        if (kind == 'STRUCT_DECL' and (i+1) < len(tokenList)):
            structName = tokenList[i+1].group('IDENTIFIER')
            if (structName):
                structTypes.add(structName)
                tokens.append((kind,value))
                tokens.append(('STRUCT_TYPE', structName))
                i += 2
                continue

        # For Handling struct instantiation
        if (kind == 'STRUCT_INSTANCE' and (i + 1) < len(tokenList)):
            structName = tokenList[i+1].group('IDENTIFIER')
            if (structName in structTypes):
                tokens.append((kind,value))
                tokens.append(('STRUCT_TYPE', structName))
                i += 2

        tokens.append((kind, value))
        i += 1
    
    return tokens

if __name__ == '__main__':
    sample_code = """
        dhacha banao TaxPayer {
            likho name;
            likho age;
        }
        likho tp aur usko banao TaxPayer
        likho tp ka name "Samar"
        likho a 10
        agar a bada hai 5 se toh
            bijli chali gayi
        sarkar gir gayi
    """
    print(lexer(sample_code))
