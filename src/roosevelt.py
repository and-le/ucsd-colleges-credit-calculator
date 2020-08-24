from .college import College
from .ap_constants import *

ROOSEVELT_8_UNIT_SCIENCE_COURSES = {AP_BIO, AP_CHEM, AP_PHYS_1, AP_PHYS_2}
ROOSEVELT_SCORE_OF_4_COURSES = {AP_CHIN, AP_FREN, AP_GER, AP_ITA, AP_JAP, AP_SPLA, AP_CALC_AB, AP_CALC_BC}

class RooseveltCollege(College):

    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        """
        The rules for determining credit for Roosevelt are simpler than some of the other src.
        The only special cases are for certain science courses: these ones count for 8 units rather than 4.
        :param credits:
        :return:
        """
        # Reset credited units
        self.credited_units = 0

        for cred in credits:
            for req in self.requirements:
                if cred.course in req.courses and cred.score >= AP_SCORE_3:

                    if cred.course in ROOSEVELT_SCORE_OF_4_COURSES:
                        if cred.score >= AP_SCORE_4:
                            if cred.course == AP_CALC_BC:
                                req.clear_credits()
                                req.add_credit(cred.course, EIGHT_UNITS)
                            else:
                                req.add_credit(cred.course, 4)
                        # Score < 4
                        else:
                            continue

                    elif cred.course in ROOSEVELT_8_UNIT_SCIENCE_COURSES:
                        # Clear out any potential 4-unit courses
                        req.clear_credits()
                        req.add_credit(cred.course, EIGHT_UNITS)

                    else:
                        req.add_credit(cred.course, FOUR_UNITS)

        # Update the number of credited units
        self.compute_credited_units()