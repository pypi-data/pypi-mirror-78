import unittest

from ezbuild.common import unity


class TestUnity(unittest.TestCase):
    def test_get_unity_path(self):

        unity_version = ''
        path = unity.get_unity_path(unity_version)

        print(path)


if __name__ == '__main__':
    unittest.main()
