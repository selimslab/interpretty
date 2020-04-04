from enum import Enum


class TokenType(Enum):
    PLUS = '+'
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

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(TokenType.EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(TokenType.INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(TokenType.PLUS, current_char)
            self.pos += 1
            return token

        raise TokenizerError("invalid input")


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = None

    def verify(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            raise ParserError("invalid input")

    def parse(self):
        self.current_token = self.tokenizer.get_next_token()

        left = self.current_token
        self.verify(TokenType.INTEGER)

        op = self.current_token
        self.verify(TokenType.PLUS)

        right = self.current_token
        self.verify(TokenType.INTEGER)

        result = left.value + right.value
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
