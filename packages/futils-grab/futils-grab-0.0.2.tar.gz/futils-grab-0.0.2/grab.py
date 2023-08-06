#! /usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

PATTERNS = {
    'd': r'[0-9]+',
    'i': r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
    'a': r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:["
         r"a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]["
         r"0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\["
         r"\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
    'e': r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|" r'"(?:['
         r'\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:['
         r'a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){'
         r'3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:['
         r'\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])',
    'q': r"'(?:[^'\\]|\\.)*'",
    'Q': r'"(?:[^"\\]|\\.)*"',
    'w': r'\S+',
    '[': r'\[[^\]]*\]',
}

PATTERNS_HELP = {
    'd': 'integer',
    'i': 'IPv4 address',
    'a': 'Address (hostname or IP',
    'e': 'Email address',
    'q': "'-quoted string",
    'Q': '"-quoted string',
    'w': r'"word" (\S+)',
    '[': 'Square bracketed text'
}


def list_of_ints(digits):
    return [int(digit) for digit in digits]


def grab_tokens(line, command, patterns, projection):
    tokens = []
    for c in command:
        pattern = patterns[c]
        match = re.search(pattern, line)
        if match:
            begin, end = match.span()
            tokens.append(line[begin: end])
            line = line[end:]

    if projection:
        tokens = [tokens[i] for i in projection if i < len(tokens)]

    return tokens


def main():
    patterns = PATTERNS
    additional_patterns = Path.home().joinpath('.grabrc')
    if additional_patterns.is_file():
        patterns = {**PATTERNS, **json.load(additional_patterns.open())}

    parser = argparse.ArgumentParser(
        description='grabs and prints specified tokens from lines in stdin (e.g. `grab qdd 13 <README`)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'command',
        action='store',
        help='specifies what tokens to grab as a string of single-character token names',
    )
    parser.add_argument(
        'projection',
        nargs='?',
        help='projection of grabbed tokens to output as a string of indices (0 through 9), defaults to all tokens',
        type=list_of_ints
    )
    parser.epilog = 'Known token types:\n'
    for pattern in patterns:
        parser.epilog += f'  {pattern}: {PATTERNS_HELP.get(pattern, "")}\n'
    parser.epilog += '\nOverride or add new tokens with ~/.grabrc (JSON: { "a": "someregex" }'
    args = parser.parse_args()

    try:
        for line in sys.stdin.buffer.raw:
            try:
                line = line.decode()
                tokens = grab_tokens(line, args.command, patterns, args.projection)
            except UnicodeDecodeError:
                pass

            if tokens:
                print(*tokens, sep='\t', flush=True)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
