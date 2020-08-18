from .college import College
from .ap_constants import *

SIXTH_8_UNIT_SCIENCE_COURSES = {AP_BIO, AP_CHEM, AP_PHYS_1, AP_PHYS_2}
SIXTH_8_UNIT_ART_COURSES = {AP_DRAW, AP_2D, AP_3D, AP_MUS, AP_ART_HIST}

class SixthCollege(College):

    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        """
        Sixth College has 2 categories for which APCredits count as 8 units. In addition, its Social Sciences
        requirement only allows 1 each of the AP Economics and Government courses to be used.

        For the remainder of the requirements, the rules for Sixth don't have any special cases.
        :param credits:
        :return:
        """
        for cred in credits:
            for req in self.requirements:
                if cred.course in req.courses:
                    # Special cases:

                    # A - Social Sciences
                    # Pick at most 1 from each of the following
                    # 1. Only one of {AP Macroeconomics, AP Microeconomics}
                    # 2. Only one of {AP Comparative Government and Politics, AP United States Government and Politics}
                    if \
                            (cred.course == AP_MACRO and AP_MICRO in req.courses) or \
                                    (cred.course == AP_MICRO and AP_MACRO in req.courses) or \
                                    (cred.course == AP_COMP_GOV and AP_US_GOV in req.courses) or \
                                    (cred.course == AP_US_GOV and AP_COMP_GOV in req.courses):
                        continue

                    # B - Science
                    elif cred.course in SIXTH_8_UNIT_SCIENCE_COURSES:
                        req.add_credit(cred.course, LARGER_UNIT_QTY)

                    # C - Art
                    elif cred.course in SIXTH_8_UNIT_ART_COURSES:
                        req.add_credit(cred.course, LARGER_UNIT_QTY)

                    # Standard case : course isn't one of the above
                    else:
                        req.add_credit(cred.course, BASE_UNIT_QTY)

        # Update the number of credited units
        self.compute_credited_units()
