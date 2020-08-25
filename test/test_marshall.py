import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, MARSHALL_NAME


class MarshallTestCase(unittest.TestCase):
    """
    Marshall's credit rules have special case for disciplinary breadth science courses, depending
    on the student's major. The implementation and tests do not account for this.
    """

    def test_max_applied_credits(self):
        """
        Verifies that the maximum number of units that can be applied is correct
        :return:
        """
        credits = [
            APCredit(AP_BIO, 5),  # Natural Science
            APCredit(AP_CHEM, 5),  # Natural Science
            APCredit(AP_PHYS_1, 5),  # Natural Science
            APCredit(AP_CALC_AB, 5),  # Mathematics, Statistics, and Logic
            APCredit(AP_CALC_BC, 5),  # Mathematics, Statistics, and Logic
            APCredit(AP_ENV, 5),  # Disciplinary Breadth
            APCredit(AP_DRAW, 5),  # Disciplinary Breadth
            APCredit(AP_LAT, 5),  # Disciplinary Breadth <-- Doesn't count toward credits; limit of 8 units exceeded
        ]

        college = init_college(MARSHALL_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 12 units for Natural Science
        # 8 units for Mathematics, Statistics, and Logic
        # 8 units for Disciplinary Breadth
        # = 28 units
        expected_credit_units = 28
        self.assertEqual(expected_credit_units, college.credited_units)

        # Marshall has 64 total units
        # 28 were applied.
        # 64 - 28 = 36
        expected_net_units = 36
        self.assertEqual(expected_net_units, college.get_net_units())

    def test_math_score_requirement(self):
        college = init_college(MARSHALL_NAME)
        credits = [
            APCredit(AP_CALC_AB, 3),
            APCredit(AP_CALC_BC, 3),
        ]
        college.apply_credits(credits)
        self.assertEqual(0, college.credited_units)


if __name__ == '__main__':
    unittest.main()
