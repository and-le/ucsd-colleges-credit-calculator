import unittest

from ..ap_constants import *
from ...reqs.requirements import load_requirements
from ..revelle import RevelleCollege

class RevelleTestCase(unittest.TestCase):
    def test_max_applied_credits(self):
        credits = [
            AP_CALC_AB,
            AP_CALC_BC,
            AP_STAT,
            AP_BIO,
            AP_CHEM,
            AP_PHYS_1,
            AP_PHYS_MECH,
            AP_PHYS_EM,
            AP_US_HIST,
            AP_US_GOV,
            AP_PSY,
            AP_DRAW,
            AP_SPLA,
        ]

        # req = load_requirements("...reqs/requirement_files/revelle_requirements.csv")
        # revelle = RevelleCollege("Revelle", )
        # expected_credit_units = 44
        # self.assertEqual(expected_credit_units, False)


if __name__ == '__main__':
    unittest.main()
