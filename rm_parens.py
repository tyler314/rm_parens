#!/usr/bin/env python
"""
Takes a Python file in as an argument and removes unnecessary parenthesis use in if and
while blocks. It could be an file type, but the file is assumed to have Python code and
proper syntax.
"""

import sys
import re
import six


class RemoveParens(object):
    """
    Takes a string in and removes the unnecessary parenthesis, set the line class variable
    to the updated string. The line class variable will remain unchanged if no unnecessary
    parenthesis exist.
    """
    def __init__(self, line):
        self.line = line
        self._open_paren_index = None
        self._close_paren_index = None
        self._remove_parens()

    def _set_open_parens_index(self):
        if 'if(' in self.line:
            index = self.line.index('if(') + 2
            self.line = self.line[:index] + ' ' + self.line[index:]
        elif 'while(' in self.line:
            index = self.line.index('while(') + 5
            self.line = self.line[:index] + ' ' + self.line[index:]
        # Set index to be placed at the paren
        match = re.match('[ \t]*(if|while)[ \t]*\(', self.line)
        open_paren_match = match[0] if six.PY3 else match.group(0)
        self._open_paren_index = self.line.index(
            open_paren_match) + len(open_paren_match) - 1

    def _set_close_parens_index(self):
        for char_i in range(len(self.line) - 1, -1, -1):
            if self.line[char_i] == ')':
                self._close_paren_index = char_i
                break

    def _unnecessary_parens(self):
        if self._outside_parens():
            self._set_open_parens_index()
            self._set_close_parens_index()
            cnt_matching_parens = 0
            for i in range(self._open_paren_index + 1, self._close_paren_index):
                if self.line[i] == '(':
                    cnt_matching_parens += 1
                elif self.line[i] == ')':
                    cnt_matching_parens -= 1
                    if cnt_matching_parens < 0:
                        return False
            if cnt_matching_parens == 0:
                return True
        return False

    def _outside_parens(self):
        if re.match('[ \t]*(if|while)[ \t]*\(.*\)[ \t]*:', self.line):
            return True
        return False

    def _remove_parens(self):
        if self._unnecessary_parens():
            self.line = self.line[:self._open_paren_index] + self.line[self._open_paren_index + \
                1:self._close_paren_index] + self.line[self._close_paren_index + 1:]


if __name__ == '__main__':
    fileLines = open(sys.argv[1], 'r').readlines()
    newFileLines = []
    updatedLine = None
    with open(sys.argv[1], 'w') as f:
        try:
            for line in fileLines:
                updatedLine = RemoveParens(line)
                newFileLines.append(updatedLine.line)
            f.write(''.join(newFileLines))
        # If something goes wrong, write the file to it's original state
        except BaseException:
            f.write(''.join(fileLines))
