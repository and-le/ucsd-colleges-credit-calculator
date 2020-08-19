import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, SIXTH_NAME


class SixthTestCase(unittest.TestCase):
    """
    Sixth's credit rules have several special case for 8-unit courses.
    Sixth also has a special case for its Social Analysis requirement, in which the APCredits
    cannot be mixed and matched.
    The tests for Sixth verify the standard addition of credits.
    """

    def test_max_applied_credits(self):
        """
        Verifies that the maximum number of units that can be applied is correct
        :return:
        """
        credits = [
            APCredit(AP_CSA, 5),   # Information Technology Fluency
            APCredit(AP_MACRO, 5),  # Social Analysis
            APCredit(AP_US_GOV, 5),  # Social Analysis
            APCredit(AP_US_HIST, 5),  # Narrative, Aesthetic, and Historical Reasoning
            APCredit(AP_WORLD_HIST, 5),  # Narrative, Aesthetic, and Historical Reasoning
            APCredit(AP_BIO, 5),  # Analytical and Scientific Methods
            APCredit(AP_STAT, 5),  # Exploring Data
            APCredit(AP_CALC_AB, 5),  # Structured Reasoning
            APCredit(AP_DRAW, 5),  # Art Making
        ]

        college = init_college(SIXTH_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 4 units for Information Technology Fluency
        # 8 units for Social Analysis
        # 8 units for Narrative, Aesthetic, and Historical Reasoning
        # 8 units for Analytical and Scientific Methods
        # 4 units for Exploring Data
        # 4 units for Structured Reasoning
        # 8 units for Art Making
        # = 44 units
        expected_credit_units = 44
        self.assertEqual(expected_credit_units, college.credited_units)

        # Sixth has 68 total units
        # 44 were applied.
        # 68 - 44 = 24
        expected_net_units = 24
        self.assertEqual(expected_net_units, college.get_net_units())



    def test_social_analysis_econ(self):
        """
        Verifies that only one each of the AP Economics courses is applied for credit
        :return:
        """
        credits = [
            APCredit(AP_MACRO, 5),
            APCredit(AP_MICRO, 5),
        ]

        college = init_college(SIXTH_NAME)
        college.apply_credits(credits)

        expected_credit_units = 4
        self.assertEqual(expected_credit_units, college.credited_units)


    def test_social_analysis_gov(self):
        """
        Verifies that only one each of the AP Government courses is applied for credit
        :return:
        """
        credits = [
            APCredit(AP_US_GOV, 5),
            APCredit(AP_COMP_GOV, 5),
        ]

        college = init_college(SIXTH_NAME)
        college.apply_credits(credits)

        expected_credit_units = 4
        self.assertEqual(expected_credit_units, college.credited_units)


if __name__ == '__main__':
    unittest.main()
