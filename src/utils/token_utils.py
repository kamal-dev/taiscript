class TokenUtils:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, *types):
        """
        Check if the current token matches any of the given 
        type and advance.

        Returns:
            bool: Returns whether match is found or not.
        """
        for t in types:
            if (self.check(t)):
                self.advance()
                return True
        return False

    def check(self, type_):
        """
        Check if current token matches the given token type.

        Args:
            type_ (str): Token type to check.

        Returns:
            bool: Returns current token matches the given
                token type or not.
        """
        if (self.is_at_end()):
            return False
        return self.peek()[0] == type_
    
    def check_next(self, type_):
        """
        Check if next token matches the given token type.

        Args:
            type_ (str): Token type to check

        Returns:
            bool: Returns next token matches the given
                token type or not.
        """
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1][0] == type_


    def advance(self):
        """
        This func just moves to the next code

        Returns:
            tuple: Returns the previous token.
        """
        if (not self.is_at_end()):
            self.current += 1
        return self.previous()

    def is_at_end(self):
        """
        Checks if token pointer has reached the end of the token list.

        Returns:
            bool: Returns whether token pointer has reached the end
                of the token list.
        """
        return self.current >= len(self.tokens)

    def previous(self):
        """
        Returns the previous token.

        Returns:
            tuple: The previous token.
        """
        return self.tokens[self.current - 1]

    def consume(self, type_, message):
        """
        Consume the token if it matches the given token type.

        Args:
            type_ (str): Expected token type
            message (str): Error message if the token doesn't match.

        Raises:
            SyntaxError: Raise syntax error (message) if the token
                        doesn't match the expected type.

        Returns:
            tuple: The consumed token
        """
        if (self.check(type_)):
            return self.advance()
        
        raise SyntaxError(message)

    def peek(self):
        """
        Return the current token without advancing.

        Returns:
            tuple: Current token
        """
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current]