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


class InterpreterError(Exception):
    pass

class NodeVisitorError(Exception):
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


class ASTNode:
    pass


class BinaryOperator(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            raise ParserError("invalid input")

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.parse()
            self.eat(RPAREN)
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinaryOperator(left=node, op=token, right=self.factor())

        return node

    def parse(self):
        """
        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinaryOperator(left=node, op=token, right=self.term())

        return node


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NodeVisitorError(f'No method to visit {type(node).__name__}')


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryOperator(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def eval(self):
        tree = self.parser.parse()
        return self.visit(tree)


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
            interpreter = Interpreter(parser)
            result = interpreter.eval()
            print(result)
        except (ParserError, TokenizerError, InterpreterError, NodeVisitorError) as e:
            print(e)


if __name__ == '__main__':
    repl()
