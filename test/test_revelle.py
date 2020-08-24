import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, REVELLE_NAME


class RevelleTestCase(unittest.TestCase):
    """
    Revelle's credit rules are without special cases.
    The tests for Revelle verify the standard addition of credits.
    """

    def test_max_applied_credits(self):
        """
        Verifies that the maximum number of units that can be applied is correct
        :return:
        """

        credits = [
            APCredit(AP_CALC_AB, 5),  # Mathematics
            APCredit(AP_CALC_BC, 5),  # Mathematics
            APCredit(AP_STAT, 5),  # Mathematics
            APCredit(AP_BIO, 5),  # Natural Science
            APCredit(AP_CHEM, 5),  # Natural Science
            APCredit(AP_PHYS_1, 5),  # Natural Science
            APCredit(AP_PHYS_MECH, 5),  # Natural Science
            APCredit(AP_PHYS_EM, 5),  # Natural Science
            APCredit(AP_US_HIST, 5),  # Social Science
            APCredit(AP_US_GOV, 5),  # Social Science
            APCredit(AP_PSY, 5),  # Social Science
            APCredit(AP_DRAW, 5),  # Fine Arts
            APCredit(AP_SPLA, 5),  # Language
            APCredit(AP_LAT, 5),  # <-- Doesn't count for credit

        ]

        college = init_college(REVELLE_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 8 units for Mathematics
        # 16 units for Natural Science
        # 8 units for Social Science
        # 4 units for Fine Arts
        # 4 units for Language
        # = 40 units

        expected_credit_units = 40
        self.assertEqual(expected_credit_units, college.credited_units)

        # Revelle has 68 total units.
        # 44 were credited.
        # 68 - 40 = 28
        expected_net_units = 28
        self.assertEqual(expected_net_units, college.get_net_units())

    def test_calculus_ab(self):
        credits = [
            APCredit(AP_CALC_AB, 3),  # Mathematics
        ]
        college = init_college(REVELLE_NAME)
        college.apply_credits(credits)
        self.assertEqual(0, college.credited_units)

        credits[0].score = 4
        college.apply_credits(credits)
        self.assertEqual(4, college.credited_units)

    def test_calculus_ab_bc_replacement(self):
        """
        Verifies that when the AP Calculus BC score is sufficient, the Mathematics requirement is completely met
        :return:
        """
        credits = [
            APCredit(AP_CALC_AB, 3),  # Doesn't count for credit
            APCredit(AP_CALC_BC, 5),  # Counts for credit
        ]
        college = init_college(REVELLE_NAME)
        college.apply_credits(credits)
        self.assertEqual(8, college.credited_units)

    def test_lang_requirement(self):
        credits = [
            APCredit(AP_CHIN, 3)
        ]
        college = init_college(REVELLE_NAME)
        college.apply_credits(credits)
        self.assertEqual(0, college.credited_units)

        credits[0].score = 4
        college.apply_credits(credits)
        self.assertEqual(4, college.credited_units)

    def test_chem_requirement(self):
        credits = [
            APCredit(AP_CHEM, 4)
        ]
        college = init_college(REVELLE_NAME)
        college.apply_credits(credits)
        self.assertEqual(0, college.credited_units)

        credits[0].score = 5
        college.apply_credits(credits)
        self.assertEqual(4, college.credited_units)


if __name__ == '__main__':
    unittest.main()
