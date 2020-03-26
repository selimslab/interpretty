import argparse


def cli():
    arg_parser = argparse.ArgumentParser(
        description='SPI - Simple Pascal Interpreter'
    )
    arg_parser.add_argument('inputfile', help='Pascal source file')
    arg_parser.add_argument(
        '--scope',
        help='Print scope information',
        action='store_true',
    )
    arg_parser.add_argument(
        '--stack',
        help='Print call stack',
        action='store_true',
    )
    args = arg_parser.parse_args()

    global _SHOULD_LOG_SCOPE, _SHOULD_LOG_STACK
    _SHOULD_LOG_SCOPE, _SHOULD_LOG_STACK = args.scope, args.stack

    text = open(args.inputfile, 'r').read()



