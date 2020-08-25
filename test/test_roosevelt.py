import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, ROOSEVELT_NAME


class RooseveltTestCase(unittest.TestCase):
    """
    Roosevelt's credit rules have 1 special case for 8-unit science courses.
    The tests for Roosevelt verify the standard addition of credits.
    """

    def test_max_applied_credits(self):
        """
        Verifies that the maximum number of units that can be applied is correct
        :return:
        """
        credits = [
            APCredit(AP_CALC_AB, 5),  # Quantitative and Formal Skills
            APCredit(AP_CALC_BC, 5),  # Quantitative and Formal Skills
            APCredit(AP_BIO, 5),  # Natural Science
            APCredit(AP_SPLA, 5),  # Language
            APCredit(AP_DRAW, 5),  # Fine Arts
            APCredit(AP_EURO_HIST, 5),  # Regional Specialization
            APCredit(AP_US_HIST, 5),             # <-- Doesn't count for credit
        ]

        college = init_college(ROOSEVELT_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 8 units for Quantitative and Formal Skills
        # 8 units for Natural Science
        # 4 units for Language
        # 4 units for Fine Arts
        # 4 units for Regional Specialization
        # = 28 units
        expected_credit_units = 28
        self.assertEqual(expected_credit_units, college.credited_units)

        # Roosevelt has 64 total units
        # 28 were applied.
        # 64 - 28 = 36
        expected_net_units = 36
        self.assertEqual(expected_net_units, college.get_net_units())


    def test_math_score_requirement(self):
        college = init_college(ROOSEVELT_NAME)
        credits = [
            APCredit(AP_CALC_AB, 3),
            APCredit(AP_CALC_BC, 3),
        ]
        college.apply_credits(credits)
        self.assertEqual(0, college.credited_units)

    def test_lang_score_requirement(self):
        college = init_college(ROOSEVELT_NAME)
        credits = [
            APCredit(AP_CHIN, 3),
        ]
        college.apply_credits(credits)
        self.assertEqual(0, college.credited_units)

        credits = [
            APCredit(AP_CHIN, 4),
        ]

        college.apply_credits(credits)
        self.assertEqual(4, college.credited_units)


if __name__ == '__main__':
    unittest.main()
