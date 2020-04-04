INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS = '+'
MINUS = "-"
MUL = "*"
DIV = "/"
LPAREN = "("
RPAREN = ")"


class Token:
    def __init__(self, type, value):
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
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            raise TokenizerError("invalid input")

        return Token(EOF, None)


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def verify(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            raise ParserError("invalid input")

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.verify(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.verify(LPAREN)
            result = self.parse()
            self.verify(RPAREN)
            return result

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.verify(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.verify(DIV)
                result = result // self.factor()

        return result

    def parse(self):
        """
        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22
        """
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.verify(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.verify(MINUS)
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
