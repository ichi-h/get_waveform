# coding: UTF-8

import unittest
from src.main import calc

class Test(unittest.TestCase):

  def test_calc(self):
    self.assertEqual(3, calc(1, 2))

if __name__ == "__main__":
  unittest.main()
