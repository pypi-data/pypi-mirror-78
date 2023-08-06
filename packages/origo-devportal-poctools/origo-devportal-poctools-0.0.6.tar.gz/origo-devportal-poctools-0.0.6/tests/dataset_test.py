import unittest

from origo.devportal.poctools.models import Dataset

class TestAll(unittest.TestCase):

    def test_serialization(self):
        d = Dataset()
        d.identifier = "id"
        d.title = "title"
        d.description = "description"
        # Don't set publisher field, to test that nothing crashes if it is missing
        # d.publisher = "publisher"

        # Nothing should crash
        d.serialize()

if __name__ == '__main__':
    unittest.main()
