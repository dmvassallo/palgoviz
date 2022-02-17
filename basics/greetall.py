#!/usr/bin/env python

"""
Greets multiple users from a file.

Usage:

    greetall FILENAME [LANG]

Test (not exhaustive, and assumes names.txt and names2.txt are present):

>>> import subprocess
>>> print(subprocess.getoutput('python greetall.py names.txt'))
Hello, Eliah!
Hello, David!
Hello, Dr. Evil!
>>> print(subprocess.getoutput('python greetall.py names2.txt'))
Hello, Eliah!
Hello, David!
Hello, Dr. Evil!
Hello, Stalin!
"""

import sys

from greet import hello, FORMATS


def pmessage(prefix, message):
    """Print a message. Helper for perror and pwarn."""
    print(f'{prefix} in {sys.argv[0]}: {message}', file=sys.stderr)


def perror(message):
    """Print an error message."""
    pmessage('ERROR', message)


def pwarn(message):
    """Print a warning message."""
    pmessage('WARNING', message)


def greet_all(path, lang):
    """Greet all in a file given the path and language."""
    with open(path, encoding='utf-8') as file:
        names = set()
        for line in file:
            name = line.strip()
            if name and name not in names:
                hello(name, lang)
                names.add(name)


def greet_all_try(path, lang):
    """
    Greet all in a file given the path and language.

    Uses an explicit try-finally instead of a with statement.
    """
    file = open(path, encoding='utf-8')
    try:
        names = set()
        for line in file:
            name = line.strip()
            if name and name not in names:
                hello(name, lang)
                names.add(name)
    finally:
        file.close()


def run():
    """Run the script."""
    # Uses LBYL (look before you leap).
    # block comments, (VSCODE) control + K + C, uncomment control + K + U
    match sys.argv:
        case [_]:
            perror('Did not pass a filename')
            return 1
        case [_, path]:
            lang = 'en'
        case [_, path, lang]:
            pass
        case [_, path, lang, *_]:
            pwarn('Too many arguments, see docstring for usage')

    if lang not in FORMATS:
        perror('Did not pass a valid language code')
        return 1

    # Uses EAFP (easier to ask forgiveness than permission).
    try:
        greet_all_try(path, lang)
    except OSError as error:
        # Something went wrong opening or reading (or closing) the file.
        perror(error)
        return 1
    return 0


if __name__ == '__main__':  # If we are running this module as a script.
    sys.exit(run()) # for exit codes in powershell, $LASTEXITCODE
