import unittest

from src.requirements import APCredit
from src.init_college import *


class CollegeResultsTestCase(unittest.TestCase):
    def test_revelle(self):
        credits = [
            APCredit("AP Calculus AB", 5),
            APCredit("AP Spanish Language and Culture", 5),
            APCredit("AP Macroeconomics", 5),
        ]

        revelle = init_college(REVELLE_NAME)
        revelle.apply_credits(credits)
        results = revelle.get_college_result
        self.assertEqual(68, results["unit_total"])
        self.assertEqual(["AP"], results["applied_credits"])
        self.assertEqual(12, results["credited_units"])
        self.assertEqual(56, results["net_units"])




if __name__ == '__main__':
    unittest.main()
