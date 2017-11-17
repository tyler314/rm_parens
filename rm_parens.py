#!/usr/bin/env python
"""
Takes a Python file in as an argument and removes unnecessary parenthesis used in 'if'
and 'while' blocks. It could be any file type, but the file is assumed to have Python
code and the proper syntax.
"""
from __future__ import print_function
import sys
import re
import six


def remove_parens(string):
    """
    Takes a string in and removes the unnecessary parenthesis, returns the result. Returns
    the same input if no unnecessary parenthesis exist.
    """

    def get_open_parens_index(string):
        """
        Return the index of the first open paren in the string.
        """
        if 'if(' in string:
            index = string.index('if(') + 2
            string = string[:index] + ' ' + string[index:]
        elif 'while(' in string:
            index = string.index('while(') + 5
            string = string[:index] + ' ' + string[index:]
        # Set index to be placed at the opening paren
        match = re.match(r'[ \t]*(if|while)[ \t]*\(', string)
        open_paren_match = match[0] if six.PY3 else match.group(0)
        return string.index(open_paren_match) + len(open_paren_match) - 1

    def unnecessary_parens(string):
        """
        Returns True if 'string' is an if or while statement, that has unnecessary
        parentheses aorund its conditional. Returns False otherwise.
        """
        # Check if string has an outside parenthesis
        if re.match(r'[ \t]*(if|while)[ \t]*\(.*\)[ \t]*:', string):
            open_parens_index = get_open_parens_index(string)
            close_parens_index = len(string) - string[::-1].index(')')
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

    if unnecessary_parens(string):
        return string[:get_open_parens_index(string)] + string[get_open_parens_index(
            string) + 1:get_close_parens_index(string)] + string[get_close_parens_index(string)\
             + 1:]
    return string


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Need to pass at least one file to edit as an argument')
        sys.exit(1)
    for j in range(1, len(sys.argv)):
        fileLines = open(sys.argv[j], 'r').readlines()
        newFileLines = []
        updatedLine = None
        with open(sys.argv[j], 'w') as f:
            try:
                for line in fileLines:
                    newFileLines.append(remove_parens(line))
                f.write(''.join(newFileLines))
            # If something goes wrong, write the file to it's original state
            except BaseException:
                f.write(''.join(fileLines))
