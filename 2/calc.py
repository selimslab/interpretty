from enum import Enum


class TokenType(Enum):
    PLUS = '+'
    MINUS = "-"
    INTEGER = 'INTEGER'
    EOF = 'EOF'


class Token:
    def __init__(self, type: TokenType, value):
        self.type = type
        self.value = value


class TokenizerError(Exception):
    pass


class ParserError(Exception):
    pass


class Tokenizer:
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            raise TokenizerError("invalid input")

        return Token(TokenType.EOF, None)


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = None

    def verify(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            raise ParserError("invalid input")

    def term(self):
        """Return an INTEGER token value."""
        token = self.current_token
        self.verify(TokenType.INTEGER)
        return token.value

    def parse(self):
        self.current_token = self.tokenizer.get_next_token()

        result = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.verify(TokenType.PLUS)
                result = result + self.term()
            elif token.type == TokenType.MINUS:
                self.verify(TokenType.MINUS)
                result = result - self.term()

        return result


class Interpreter:
    pass


def repl():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        try:
            tokenizer = Tokenizer(text)
            parser = Parser(tokenizer)
            result = parser.parse()
            print(result)
        except (ParserError, TokenizerError) as e:
            print(e)


if __name__ == '__main__':
    repl()
