from err import SemanticError, LexerError, ParserError
from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter
from semantic_analysis import SemanticAnalyzer


def repl(prompt='pas.py> '):
    "A prompt-read-eval-print loop."
    semantic_analyzer = SemanticAnalyzer()

    while True:
        statement = str(input(prompt))
        program = f"PROGRAM TEST; BEGIN {statement} END."

        tokenizer = Tokenizer(program)
        try:
            parser = Parser(tokenizer)
            tree = parser.parse()
            print(tree)
            try:
                semantic_analyzer.visit(tree)
            except SemanticError as e:
                print(e.message)

            interpreter = Interpreter(tree)
            result = interpreter.interpret()
            print(result)
        except (LexerError, ParserError) as e:
            print(e.message)


if __name__ == '__main__':
    repl()
