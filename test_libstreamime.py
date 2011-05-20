import email
import email.parser
import unittest
from libstreamime import Streamime

class TestSimple(unittest.TestCase):

    def setUp(self):
        self.f = file('tests/simple.cgi', 'rb')
        self.p = email.parser.Parser()
        self.r = self.p.parse(self.f)
        self.f.seek(109) # Skip header
        self.boundary = self.r.get_boundary()

    def test_example_is_actually_valid(self):
        self.assertEqual("This is a straightforward test\ndocument which spans several lines.\n", self.r.get_payload()[0].get_payload())

    def test_rigged_body_test(self):
        streamime = Streamime(self.boundary)
        streamime.stop_after = 1
        streamime.push(self.f.read())
        self.assertEqual("This is a straightforward test\ndocument which spans several lines.\n", streamime.last_body)

    def test_rigged_body_test_partial(self):
        streamime = Streamime(self.boundary)
        streamime.stop_after = 1
        streamime.push(self.f.read(180))
        self.assertEqual("This is a stra", streamime.get_body())

if __name__ == '__main__':
    unittest.main()
