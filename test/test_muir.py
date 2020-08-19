import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, MUIR_NAME, MUIR_SOC_REQ_NAME, MUIR_POLI_SUBREQ_NAME, \
    MUIR_SCI_REQ_NAME, MUIR_CHEM_SUBREQ_NAME


class MuirTestCase(unittest.TestCase):
    """
    Muir's credit rules have special cases for its Social Sciences and Math or Natural Sciences requirements
    Specifically, no mixing and matching of credit is allowed.
    This Test Case also verifies that, when there are multiple AP Credits in different Subrequirements, the
    SubRequirement that qualifies for the most credit is chosen.
    """

    def test_max_applied_credits(self):
        """
        Verifies that the maximum number of units that can be applied is correct
        :return:
        """
        credits = [
            APCredit(AP_MACRO, 5),  # Social Science
            APCredit(AP_MICRO, 5),  # Social Science
            APCredit(AP_CHEM, 5),  # Math or Natural Science
            APCredit(AP_LAT, 5),  # Foreign Language
        ]

        college = init_college(MUIR_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 8 units for Social Science
        # 12 units for Math or Natural Sciences
        # 12 units for Foreign Language
        # = 32 units
        expected_credit_units = 32
        self.assertEqual(expected_credit_units, college.credited_units)

        # Muir has 56 total units
        # 32 were applied.
        # 56 - 32 = 24
        expected_net_units = 24
        self.assertEqual(expected_net_units, college.get_net_units())


    def test_social_science(self):
        """
        Verifies that the mix-and-match rule for Social Science works correctly
        :return:
        """
        credits = [
            APCredit(AP_MACRO, 5),
            APCredit(AP_US_GOV, 5),
            APCredit(AP_PSY, 5),
        ]

        college = init_college(MUIR_NAME)
        college.apply_credits(credits)

        # Only 1 of the Social Science Credits may be used, because they are all from
        # different subrequirement groups.
        expected_credit_units = 4
        self.assertEqual(expected_credit_units, college.credited_units)

    def test_social_science_max_subrequirement(self):
        """
        Verifies that the subrequirement with the maximal number of units is chosen among all other subrequirements for
        the Social Science Requirement
        :return:
        """
        credits = [
            APCredit(AP_MACRO, 5),
            APCredit(AP_US_GOV, 5),
            APCredit(AP_COMP_GOV, 5),
            APCredit(AP_PSY, 5),
        ]

        college = init_college(MUIR_NAME)
        college.apply_credits(credits)

        # The Political Science subrequirement has the most units: 8. Therefore, it should be the
        # subrequirement reported by the implementation.
        expected_credit_units = 8
        self.assertEqual(expected_credit_units, college.credited_units)

        # Verify that the correct SubRequirement is reported
        req = college.get_requirement(MUIR_SOC_REQ_NAME)
        self.assertEqual(MUIR_POLI_SUBREQ_NAME, req.subrequirement_name)
        self.assertIn(AP_US_GOV, req.credits)
        self.assertIn(AP_COMP_GOV, req.credits)


    def test_math_science(self):
        """
        Verifies that the mix-and-match rule for Math or Natural Science works correctly
        :return:
        """
        credits = [
            APCredit(AP_BIO, 5),
            APCredit(AP_CALC_AB, 5),
            APCredit(AP_PHYS_1, 5),
        ]

        college = init_college(MUIR_NAME)
        college.apply_credits(credits)

        # Only 1 of the Math or Natural Science credits may be used, because they are all from
        # different subrequirement groups.
        expected_credit_units = 4
        self.assertEqual(expected_credit_units, college.credited_units)


    def test_math_science_max_subrequirement(self):
        """
        Verifies that the subrequirement with the maximal number of units is chosen among all other subrequirements for
        the Math or Natural Science Requirement
        :return:
        """
        credits = [
            APCredit(AP_BIO, 5),
            APCredit(AP_PHYS_1, 5),
            APCredit(AP_CALC_AB, 5),
            APCredit(AP_CALC_BC, 5),
            APCredit(AP_PHYS_EM, 5),
            APCredit(AP_PHYS_MECH, 5),
            APCredit(AP_CHEM, 5),
        ]

        college = init_college(MUIR_NAME)
        college.apply_credits(credits)

        # AP Biology contributes 4 units to the Biology SubRequirement
        # AP Calculus AB and BC contribute 58units to the Math SubRequirement
        # AP Physics 1 contributes 4 units to the Algebra-Based Physics SubRequirement
        # AP Physics C: E & M and Mechanics contribute 8 units to the Calculus-Based Physics SubRequirement
        # AP Chemistry contributes 12 units to the Chemistry SubRequirement
        # AP Chemistry has the most units applied, 12.
        expected_credit_units = 12
        self.assertEqual(expected_credit_units, college.credited_units)

        # # Verify that the correct SubRequirement is reported
        req = college.get_requirement(MUIR_SCI_REQ_NAME)
        self.assertEqual(MUIR_CHEM_SUBREQ_NAME, req.subrequirement_name)
        self.assertIn(AP_CHEM, req.credits)

    def test_physics_algebra(self):
        """
        Verifies that the unit limit on AP Physics 1 and 2 works correctly
        :return:
        """
        credits = [
            APCredit(AP_PHYS_1, 5),
            APCredit(AP_PHYS_2, 5),
        ]

        college = init_college(MUIR_NAME)
        college.apply_credits(credits)

        # Only 1 of the Algebra-Based Physics credits may be used.
        expected_credit_units = 4
        self.assertEqual(expected_credit_units, college.credited_units)

    def test_foreign_language(self):
        """
        Verifies that the limit on foreign language courses for non-AP-Latin courses works correctly
        :return:
        """

        credits = [
            APCredit(AP_SPLA, 5),
            APCredit(AP_FREN, 5),
        ]

        college = init_college(MUIR_NAME)
        college.apply_credits(credits)

        # Each language course counts for 2 courses, or 8 units. However, multiple language courses
        # may not be applied together. If the implementation were wrong, it would credit 12 units instead of 8
        expected_credit_units = 8
        self.assertEqual(expected_credit_units, college.credited_units)


if __name__ == '__main__':
    unittest.main()
