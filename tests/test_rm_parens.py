import unittest
import rm_parens


class TestRmParens(unittest.TestCase):

    def test_get_open_parens_index(self):
        """
        _get_open_parens_index is a private function that is only to be used for
        a string has an 'if' or 'while' followed by an open parens, thus error
        checking for a strings without this assumption is not implemented.
        """
        for check in ['if', 'while']:
            res = rm_parens._get_open_parens_index(check + ' (')
            self.assertEqual(res, len(check) + 1)
            # get_open_parens_index inserts a space between 'if' or 'while', and
            # '(' if a space does not exist
            res = rm_parens._get_open_parens_index(check + '(')
            self.assertEqual(res, len(check) + 1)

            res = rm_parens._get_open_parens_index(check + ' (condition)')
            self.assertEqual(res, len(check) + 1)

            res = rm_parens._get_open_parens_index(5 * ' ' + check + ' (')
            self.assertEqual(res, len(check) + 6)

            res = rm_parens._get_open_parens_index(5 * ' ' + check + '(')
            self.assertEqual(res, len(check) + 6)

            res = rm_parens._get_open_parens_index(
                '{}(condition_{}(_unique)'.format(check, check))
            self.assertEqual(res, len(check) + 1)

            res = rm_parens._get_open_parens_index(
                check + '(((some nest) and (another)))')
            self.assertEqual(res, len(check) + 1)

    def test_get_close_parens_index(self):
        """
        This private function assumes only that a closing parens exists
        """
        res = rm_parens._get_close_parens_index(')')
        self.assertEqual(res, 0)
        res = rm_parens._get_close_parens_index('()')
        self.assertEqual(res, 1)
        string = 'if (condition)'
        res = rm_parens._get_close_parens_index(string)
        self.assertEqual(res, len(string) - 1)
        string = 'while(condition)'
        res = rm_parens._get_close_parens_index(string)
        self.assertEqual(res, len('while(condition)') - 1)
        string = '(()())()))(()()(('
        res = rm_parens._get_close_parens_index(string)
        self.assertEqual(res, len(string) - 3)

    def test_unnecessary_parens(self):
        """
        This private function returns True if the string is an 'if' or 'while'
        statement, followed by a condition surrounded by parens that do not
        contribute to the correctness of the conditional.
        """
        res = rm_parens._unnecessary_parens('if (condition):')
        self.assertEqual(res, True)
        res = rm_parens._unnecessary_parens('if condition:')
        self.assertEqual(res, False)
        res = rm_parens._unnecessary_parens('if (condition:')
        self.assertEqual(res, False)
        res = rm_parens._unnecessary_parens('if ((condition)):')
        self.assertEqual(res, True)
        res = rm_parens._unnecessary_parens('if ((condition) and (another)):')
        self.assertEqual(res, True)
        res = rm_parens._unnecessary_parens('if (condition) and (another):')
        self.assertEqual(res, False)
        res = rm_parens._unnecessary_parens(
            'some comment ->>> (condition without if or while)')
        self.assertEqual(res, False)
        res = rm_parens._unnecessary_parens('(condtion)')
        self.assertEqual(res, False)

    def test_remove_parens(self):
        """
        Test the only public function, removes unnecessary parens around if and
        while conditionals, returns result.
        """
        string = 'if (condition):'
        res = rm_parens.remove_parens(string)
        self.assertEqual(res, 'if condition:')

        string = 'if ((condition)):'
        res = rm_parens.remove_parens(string)
        self.assertEqual(res, 'if (condition):')

        string = 'if (condition) and (another):'
        res = rm_parens.remove_parens(string)
        self.assertEqual(res, string)

        string = '(hello, world) just some text ())()('
        res = rm_parens.remove_parens(string)
        self.assertEqual(res, string)

        string = 'if (condition) or ((another) and (nest)):'
        res = rm_parens.remove_parens(string)
        self.assertEqual(res, string)

        string = 'if ((condition) or ((another) and (nest))):'
        res = rm_parens.remove_parens(string)
        self.assertEqual(res, 'if (condition) or ((another) and (nest)):')
