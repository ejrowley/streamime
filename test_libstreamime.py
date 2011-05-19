import email
import email.parser
import unittest

class TestSimple(unittest.TestCase):

    def setUp(self):
        self.f = file('tests/simple.cgi', 'rb')
        self.p = email.parser.Parser()
        self.r = self.p.parse(self.f)
        self.f.seek(109) # Skip header
        self.boundary = self.r.get_boundary()

    def test_example_is_actually_valid(self):
        self.assertEqual("This is a straightforward test\ndocument which spans several lines.\n", self.r.get_payload()[0].get_payload())

if __name__ == '__main__':
    unittest.main()
