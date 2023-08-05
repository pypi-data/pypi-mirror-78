"""
Home to the entry point for ConWech's command line interface.
"""

# future imports
from __future__ import print_function

# built-in modules
import re
import enum
import colorama
import argparse

# project modules
import conwech


# because Windows is just the wrong kind of special
colorama.init()


class Colors(enum.Enum):
    numeral = colorama.Fore.LIGHTBLACK_EX
    numeric = colorama.Fore.CYAN
    other = colorama.Fore.YELLOW
    reset = colorama.Style.RESET_ALL


def paint(numeral):
    """ For internal use only! """
    result = []
    for word in numeral.split(' '):
        if word in ('hundred', ) + conwech.NATURAL_NUMBERS_LT_100:
            result.append(Colors.numeral.value + word)
        elif word in ('negative', 'and'):
            result.append(Colors.other.value + word)
        elif re.match(r'(.+illion|thousand)(ths?)?', word):
            result.append(Colors.other.value + word)
        elif word.isdigit():
            result.append(Colors.numeric.value + word)
        else:
            result.append(Colors.reset.value + word)
    return ' '.join(result)


def four(number):
    """ For internal use only! """
    spelling = ''
    while spelling != 'four':
        spelling = conwech.number2text(number)
        number = len(spelling.replace('-', '').replace(' ', ''))
        print(paint('There are {} letters in {}'.format(number, spelling)))


parser = argparse.ArgumentParser()
commands = parser.add_subparsers(metavar='SUBCOMMAND')

read_command = commands.add_parser(
    'read',
    help='convert text to number')
read_command.add_argument(
    'text', type=str,
    help='text of a number to read')
read_command.set_defaults(
    func=lambda text: print(conwech.text2number(text)))

spell_command = commands.add_parser(
    'spell',
    help='convert number to text')
spell_command.add_argument(
    'number', type=str,
    help='a number to be spelled')
spell_command.add_argument(
    '-r', '--recursive', action='store_const', const=four, dest='func',
    help="spell recursively to 'four'")
spell_command.set_defaults(
    func=lambda number: print(paint(conwech.number2text(number))))


def main():
    """ For internal use only! """
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs) # noqa


if __name__ == '__main__':
    main()
