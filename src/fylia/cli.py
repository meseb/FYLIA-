import argparse
from .tui import run_tui

def main():
    parser = argparse.ArgumentParser(description='FYLIA: AI-powered code generation tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Chat command
    subparsers.add_parser('chat', help='Start the chat interface')

    args = parser.parse_args()

    if args.command == 'chat':
        run_tui()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()