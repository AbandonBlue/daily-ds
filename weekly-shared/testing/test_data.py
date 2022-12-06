import unittest
from unittest import mock
from tests.module import math123

# from importlib import reload
# reload(math)

# 為了要使用 unittest, 需要去繼承 unittest.TestCase


# def square(x):
#     return x ** 2

def cube(x):
    return x ** 4 # 故意寫錯，當作識別

class TestSampleFeatures(unittest.TestCase):
    """
        測試例子。
    """
    def test_square(self):
        """
            test square function.
        """
        x = 3
        result = math123.square(x)
        self.assertEqual(result, 9)

    def test_cube(self):
        """
            test cube function(當錯誤時，顯示於cmd上)
        """
        x = 3
        result = cube(x)
        self.assertEqual(result, 27)


class TestSampleFeaturesMock(unittest.TestCase):
    def test_square(self):
        x = 3
        result = math123.square(x)
        self.assertEqual(result, 9)
    
    @mock.patch("math123.transform_square", return_value=10)
    def test_transform_square(self, mock_square):
        x = 9
        result = math123.transform_square(x)
        self.assertEqual(result, 100)