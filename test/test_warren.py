import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, WARREN_NAME, WARREN_MUS_AS_NAME, WARREN_PSY_AS_NAME, WARREN_ECON_POFC_NAME, \
    WARREN_MUS_POFC_NAME, WARREN_PSY_POFC_NAME, WARREN_SCI_POFC_NAME, \
    WARREN_VIS_ART_POFC_NAME, WARREN_HIST_POFC_NAME,  WARREN_LIT_POFC_NAME


class WarrenTestCase(unittest.TestCase):
    """
    Warren's credit rules have special cases for its Programs of Concentration and Area Studies requirements.

    In addition, Warren offers Specialized Humanities, Social Sciences, Area Studies, and Science SubRequirements
    that encompass APCredits in other SubRequirements. These Specialized courses are currently *NOT* used.

    In a future update, however, the implementation may report either this
    Specialized SubRequirement or another SubRequirement that shares accredited courses with the Specialization.
    """

    def test_general(self):
        """
        Verifies that the credits applied for non-PofC and non-Area-Study requirements are correct
        :return:
        """
        credits = [
            APCredit(AP_CALC_AB, 5),
            APCredit(AP_CALC_BC, 5),
        ]

        college = init_college(WARREN_NAME)
        college.apply_credits(credits)

        # Unit calculation
        # 8 units for Formal Skills

        self.assertEqual(8, college.gen_credited_units)

    def test_pofc(self):
        """
        Verifies that the credits applied for Programs of Concentration are correct
        :return:
        """

        credits = [
            APCredit(AP_MUS, 5),  # Humanities and Fine Arts - Music
            APCredit(AP_PSY, 5),  # Social Sciences - Psychology
            APCredit(AP_ENV, 5),  # Math, Natural Sciences, and Engineering
        ]

        college = init_college(WARREN_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 8 units for Humanities and Fine Arts
        # 4 units for Social Sciences
        # 4 units for Math, Natural Sciences, and Engineering

        self.assertEqual(12, college.pofc_hum_soc_credited_units)
        self.assertEqual(12, college.pofc_hum_sci_credited_units)
        self.assertEqual(8, college.pofc_soc_sci_credited_units)

        # Verify the SubRequirement names
        hum_condition = (WARREN_MUS_POFC_NAME == college.pofc_hum.name)
        soc_condition = (WARREN_PSY_POFC_NAME == college.pofc_soc.name)
        sci_condition = (WARREN_SCI_POFC_NAME == college.pofc_sci.name)

        self.assertTrue(hum_condition and soc_condition and sci_condition)

    def test_pofc_max_subrequirement(self):
        """
        Verifies that the subrequirement with the most credit units fulfilled is chosen when there is a computing
        subrequirement with fewer credit units fulfilled
        :return:
        """
        credits = [
            APCredit(AP_MACRO, 5),  # Social Sciences - Economics
            APCredit(AP_MICRO, 5),  # Social Sciences - Economics
            APCredit(AP_PSY, 5),  # Social Sciences - Psychology
        ]

        college = init_college(WARREN_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 8 units for Social Sciences

        self.assertEqual(8, college.pofc_hum_soc_credited_units)
        self.assertEqual(8, college.pofc_soc_sci_credited_units)

        # Verify the SubRequirement name
        self.assertTrue(WARREN_ECON_POFC_NAME == college.pofc_soc.name)


    def test_pofc_eight_unit_credits(self):
        """
        Verifies that, when there are 2 credits, each worth 8 units, that both courses are credited.
        :return:
        """
        credits = [
            APCredit(AP_2D, 5),  # Humanities and Fine Arts - Visual Arts
            APCredit(AP_3D, 5),  # Humanities and Fine Arts - Visual Arts
            APCredit(AP_WORLD_HIST, 5),  # Humanities and Fine Arts - History
            APCredit(AP_US_HIST, 5),  # Humanities and Fine Arts - History
            APCredit(AP_ENG_LIT, 5),  # Humanities and Fine Arts - Literature
            APCredit(AP_ENG_LANG, 5),  # Humanities and Fine Arts - Literature
        ]

        college = init_college(WARREN_NAME)
        college.apply_credits(credits)

        visart = college.get_pofc(WARREN_VIS_ART_POFC_NAME)
        self.assertEqual(12, visart.credit_units)
        hist = college.get_pofc(WARREN_HIST_POFC_NAME)
        self.assertEqual(12, hist.credit_units)
        lit = college.get_pofc(WARREN_LIT_POFC_NAME)
        self.assertEqual(12, lit.credit_units)


    def test_area_studies(self):
        """
        Verifies that the credits applied for Area Studies are correct
        :return:
        """

        credits = [
            APCredit(AP_MUS, 5),  # Humanities and Fine Arts - Music
            APCredit(AP_PSY, 5),  # Social Sciences - Psychology
        ]

        college = init_college(WARREN_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 4 units for Social Sciences
        # 4 units for Humanities and Fine Arts
        # = 8 units

        self.assertEqual(4, college.area_study_hum_credited_units)
        self.assertEqual(4, college.area_study_soc_credited_units)

        # Verify the SubRequirement names
        hum_condition = (WARREN_MUS_AS_NAME == college.area_study_hum.name)
        soc_condition = (WARREN_PSY_AS_NAME == college.area_study_soc.name)
        self.assertTrue(hum_condition and soc_condition)


if __name__ == '__main__':
    unittest.main()
