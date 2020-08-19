import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, SEVENTH_NAME


class SeventhTestCase(unittest.TestCase):
    """
    Seventh's credit rules have several special case for 8-unit courses.
    The tests for Seventh verify the standard addition of credits.
    """

    def test_max_applied_credits(self):
        """
        Verifies that the maximum number of units that can be applied is correct
        :return:
        """
        credits = [
            APCredit(AP_DRAW, 5),  # Arts
            APCredit(AP_US_HIST, 5),  # Humanities
            APCredit(AP_BIO, 5),  # Natural Sciences and Engineering
            APCredit(AP_CSA, 5),  # Quantitative Reasoning
            APCredit(AP_MACRO, 5),  # Social Sciences
            APCredit(AP_MICRO, 5),  # Social Sciences
        ]

        college = init_college(SEVENTH_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 8 units for Arts
        # 8 units for Humanities
        # 8 units for Natural Sciences and Engineering
        # 8 units for Quantitative Reasoning
        # 8 units for Social Sciences
        # = 40 units
        expected_credit_units = 40
        self.assertEqual(expected_credit_units, college.credited_units)

        # Seventh has 56 total units
        # 40 were applied.
        # 56 - 40 = 16
        expected_net_units = 16
        self.assertEqual(expected_net_units, college.get_net_units())


if __name__ == '__main__':
    unittest.main()
