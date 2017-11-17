import unittest
import rm_parens

class TestRmParens(unittest.TestCase):
    
    def test_remove_parens(self):
        res = rm_parens('')
        self.assertEqual(res, '')