#!/usr/bin/env python
"""
Takes a Python file in as an argument and removes unnecessary parenthesis used in 'if'
and 'while' blocks. It could be any file type, but the file is assumed to have Python
code and the proper syntax.
"""

import sys
import re
import six


def removeParens(line):
    """
    Takes a string in and removes the unnecessary parenthesis, set the line class variable
    to the updated string. The line class variable will remain unchanged if no unnecessary
    parenthesis exist.
    """

    def get_open_parens_index(line):
        """
        Get the index of the first open paren in the string, line.
        """
        if 'if(' in line:
            index = line.index('if(') + 2
            line = line[:index] + ' ' + line[index:]
        elif 'while(' in line:
            index = line.index('while(') + 5
            line = line[:index] + ' ' + line[index:]
        # Set index to be placed at the opening paren
        match = re.match('[ \t]*(if|while)[ \t]*\(', line)
        open_paren_match = match[0] if six.PY3 else match.group(0)
        return line.index(open_paren_match) + len(open_paren_match) - 1

    def get_close_parens_index(line):
        """
        Get the index of the last close paren in the string, 'line'.
        """
        for char_i in range(len(line) - 1, -1, -1):
            if line[char_i] == ')':
                return char_i

    def has_outside_parens(line):
        """
        Returns true if 'line' is an if or while statement, that has parentheses on the
        outside of its conditional.
        """
        if re.match('[ \t]*(if|while)[ \t]*\(.*\)[ \t]*:', line):
            return True
        return False

    def unnecessary_parens(line):
        """
        Returns True if 'line' is an if or while statement, that has unnecessary
        parentheses aorund its conditional. Returns False otherwise.
        """
        if has_outside_parens(line):
            open_parens_index = get_open_parens_index(line)
            close_parens_index = get_close_parens_index(line)
            # Ensure that nested parens are not dependent on the outer parens
            cnt_matching_parens = 0
            for i in range(open_parens_index + 1, close_parens_index):
                if line[i] == '(':
                    cnt_matching_parens += 1
                elif line[i] == ')':
                    cnt_matching_parens -= 1
                    if cnt_matching_parens < 0:
                        return False
            if cnt_matching_parens == 0:
                return True
        return False

    if unnecessary_parens(line):
        return line[:get_open_parens_index(line)] + line[get_open_parens_index(line) + 1:get_close_parens_index(line)] + line[get_close_parens_index(line) + 1:]
    else:
        return line


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Need to pass at least one file to edit as an argument')
        sys.exit(1)
    for i in range(1, len(sys.argv)):
        fileLines = open(sys.argv[i], 'r').readlines()
        newFileLines = []
        updatedLine = None
        with open(sys.argv[i], 'w') as f:
            try:
                for line in fileLines:
                    newFileLines.append(removeParens(line))
                f.write(''.join(newFileLines))
            # If something goes wrong, write the file to it's original state
            except BaseException:
                f.write(''.join(fileLines))
