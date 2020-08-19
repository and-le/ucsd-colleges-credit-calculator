import unittest

from src.ap_constants import *
from src.requirements import APCredit
from src.init_college import init_college, WARREN_NAME, WARREN_HUM_AS_NAME, WARREN_SOC_AS_NAME, \
    WARREN_MUS_AS_NAME, WARREN_PSY_AS_NAME


class WarrenTestCase(unittest.TestCase):
    """
    Warren's credit rules have special cases for its Programs of Concentration and Area Studies requirements.
    In addition, Warren offers Specialized Humanities, Social Sciences, Area Studies, and Science SubRequirements
    that encompass APCredits in other SubRequirements. Consequently, the implementation may report either this
    Specialized SubRequirement or another SubRequirement that shares accredited courses with the Specialization.
    """

    def test_area_studies(self):
        """
        Verifies that the credits applied for Area Studies are correct
        :return:
        """

        credits = [
            APCredit(AP_PSY, 5),  # Social Sciences
            APCredit(AP_MUS, 5),  # Humanities and Fine Arts
        ]

        college = init_college(WARREN_NAME)
        college.apply_credits(credits)

        # Unit calculation:
        # 4 units for Social Sciences
        # 4 units for Humanities and Fine Arts
        # = 8 units
        self.assertEqual(4, college.area_study_hum_credited_units)
        self.assertEqual(4, college.area_study_soc_credited_units)

        # Verify the SubRequirement name
        hum_condition = (WARREN_HUM_AS_NAME == college.area_study_hum.name) or \
                        (WARREN_MUS_AS_NAME == college.area_study_hum.name)
        soc_condition = (WARREN_SOC_AS_NAME == college.area_study_soc.name) or \
                        (WARREN_PSY_AS_NAME == college.area_study_soc.name)
        self.assertTrue(hum_condition and soc_condition)


if __name__ == '__main__':
    unittest.main()
