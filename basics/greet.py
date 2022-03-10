#!/usr/bin/env python

"""Hello world example."""

FORMATS = {
    'en': 'Hello, {}!',
    'es': '¡Hola, {}!',
}


def make_greeter(lang):
    """
    Make a greeter function that greets the user in the language passed by lang

    >>> greet = make_greeter('es')
    >>> greet('David')
    ¡Hola, David!
    >>> greet('Eliah')
    ¡Hola, Eliah!
    >>> make_greeter('en')('Stalin')  # But we greet Stalin in English???
    Hello, Stalin!
    """
    if lang not in FORMATS:
        raise ValueError(f'{lang} is an unrecognized language code.')

    def greeter(name):
        print(FORMATS[lang].format(name))   # dictionary test

    return greeter


def hello(name, lang='en'):
    """
    Greet the user.

    >>> hello('Eliah')
    Hello, Eliah!
    >>> hello('Eliah','en')
    Hello, Eliah!
    >>> hello('Eliah','es')
    ¡Hola, Eliah!
    >>> hello('Eliah','el')
    Traceback (most recent call last):
      ...
    ValueError: el is an unrecognized language code.
    """
    greeter = make_greeter(lang)
    greeter(name)


def run():
    """Run the doctests."""
    import doctest
    doctest.testmod()


if __name__ == '__main__':  # If we are running this module as a script.
    run()
