#!/usr/bin/env python
"""
Takes a Python file in as an argument and removes unnecessary parenthesis used in 'if'
and 'while' blocks. It could be any file type, but the file is assumed to have Python
code and the proper syntax.
"""
from __future__ import print_function
import sys
import re


def _get_open_parens_index(string):
    """
    Return the index of the first open paren in the string.
    """
    # Set index to be placed at the opening paren
    match = re.match(r'[ \t]*(if|while)[ \t]*\(', string)
    open_paren_match = match.group(0)
    return string.index(open_paren_match) + len(open_paren_match) - 1


def _get_close_parens_index(string):
    """
    Return the index of the last close paren in the string.
    """
    return len(string) - string[::-1].index(')') - 1


def _unnecessary_parens(string):
    """
    Returns True if 'string' is an if or while statement, that has unnecessary
    parentheses aorund its conditional. Returns False otherwise.
    """
    # Check if string has outside parentheses
    if re.match(r'[ \t]*(if|while)[ \t]*\(.*\)[ \t]*:', string):
        open_parens_index = _get_open_parens_index(string)
        close_parens_index = _get_close_parens_index(string)
        # Ensure that nested parens are not dependent on the outer parens
        cnt_matching_parens = 0
        for i in range(open_parens_index + 1, close_parens_index):
            if string[i] == '(':
                cnt_matching_parens += 1
            elif string[i] == ')':
                cnt_matching_parens -= 1
                if cnt_matching_parens < 0:
                    return False
        if cnt_matching_parens == 0:
            return True
    return False


def _add_space_buffer(string):
    """
    Adds a space character between the if or while statement, and the '('
    character if one does not exist.
    """
    if 'if(' in string:
        index = string.index('if(') + 2
        string = string[:index] + ' ' + string[index:]
    elif 'while(' in string:
        index = string.index('while(') + 5
        string = string[:index] + ' ' + string[index:]
    return string


def remove_parens(string):
    """
    Takes a string in and removes the unnecessary parenthesis, returns the result. Returns
    the same input if no unnecessary parenthesis exist.
    """
    if _unnecessary_parens(string):
        string = _add_space_buffer(string)
        return string[:_get_open_parens_index(string)] + string[_get_open_parens_index(
            string) + 1:_get_close_parens_index(string)] + string[_get_close_parens_index(string) + 1:]
    return string


def main():
    """
    Used as the entry point for the package
    """
    if len(sys.argv) < 2:
        print('Need to pass at least one file to edit as an argument')
        sys.exit(1)
    for j in range(1, len(sys.argv)):
        fileLines = open(sys.argv[j], 'r').readlines()
        newFileLines = []
        with open(sys.argv[j], 'w') as f:
            try:
                for line in fileLines:
                    newFileLines.append(remove_parens(line))
                f.write(''.join(newFileLines))
            # If something goes wrong, write the file to it's original state
            except BaseException:
                f.write(''.join(fileLines))


if __name__ == '__main__':
    main()
