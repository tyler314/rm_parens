#!/usr/bin/env python

import sys
import re
import six

def unnecessary_parens(line):
    if re.match('[ \t]*(if|while)[ \t]*\(.*\)[ \t]*:', line):
        return True
    return False
    
def remove_parens(line):
    if 'if(' in line:
        index = line.index('if(') + 2
        line = line[:index] + ' ' + line[index:]
    elif 'while(' in line:
        index = line.index('while(') + 5
        line = line[:index] + ' ' + line[index:]
    # Set index to be placed at the paren
    match = re.match('[ \t]*(if|while)[ \t]*\(', line)
    open_paren_match = match[0] if six.PY3 else match.group(0)
    open_paren_index = line.index(open_paren_match) + len(open_paren_match) - 1
    close_paren_index = None
    for char_i in range(len(line)-1, -1, -1):
        if line[char_i] == ')':
            close_paren_index = char_i
            break
    line = line[:open_paren_index] + line[open_paren_index+1:close_paren_index] + line[close_paren_index+1:]
    return line

if __name__ == '__main__':
    file_lines = open(sys.argv[1], 'r').readlines()
    new_file_lines = []
    with open(sys.argv[1], 'w') as file:
        try:
            for line in file_lines:
                if unnecessary_parens(line):
                    new_file_lines.append(remove_parens(line))
                else:
                    new_file_lines.append(line)
            file.write(''.join(new_file_lines))
        # If something goes wrong, write the file to it's original state
        except:
            file.write(''.join(file_lines))
