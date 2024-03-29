from .college import College
from .ap_constants import *

SEVENTH_8_UNIT_ART_COURSES = {AP_DRAW, AP_2D, AP_3D, AP_MUS, AP_ART_HIST}
SEVENTH_8_UNIT_HUMANITIES_COURSES = {AP_US_HIST, AP_CHIN, AP_FREN, AP_GER, AP_ITA, AP_JAP, AP_SPLA, AP_SPLI}
SEVENTH_8_UNIT_SCIENCE_COURSES = {AP_BIO, AP_CHEM, AP_PHYS_1, AP_PHYS_2}
SEVENTH_8_UNIT_QUANT_COURSES = {AP_CALC_BC, AP_CSA, AP_CSP}
SEVENTH_SCORE_OF_FOUR_COURSES = {AP_CALC_AB}

class SeventhCollege(College):

    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        """
        Seventh College has 4 different categories of courses for which each APCredit is worth 8 units.
        Aside from this, there are no special cases.
        :param credits:
        :return:
        """
        # Reset credited units
        self.credited_units = 0

        for cred in credits:
            for req in self.requirements:
                if cred.course in req.courses and cred.score >= AP_SCORE_3:

                    if cred.course in SEVENTH_8_UNIT_ART_COURSES:
                        req.add_credit(cred.course, EIGHT_UNITS)
                    elif cred.course in SEVENTH_8_UNIT_HUMANITIES_COURSES:
                        # A score >= 4 meets the whole requirement. A score of 3 meets 1 course.
                        if cred.score >= AP_SCORE_4:
                            req.clear_credits()
                            req.add_credit(cred.course, EIGHT_UNITS)
                        else:
                            req.add_credit(cred.course, FOUR_UNITS)
                    elif cred.course in SEVENTH_8_UNIT_SCIENCE_COURSES:
                        req.add_credit(cred.course, EIGHT_UNITS)
                    elif cred.course in SEVENTH_8_UNIT_QUANT_COURSES:
                        if cred.course == AP_CALC_BC:
                            if cred.score >= AP_SCORE_4:
                                req.add_credit(cred.course, EIGHT_UNITS)
                            else:
                                continue
                        else:
                            req.add_credit(cred.course, EIGHT_UNITS)
                    elif cred.course in SEVENTH_SCORE_OF_FOUR_COURSES:
                        if cred.score >= 4:
                            req.add_credit(cred.course, FOUR_UNITS)
                        else:
                            continue
                    else:
                        req.add_credit(cred.course, FOUR_UNITS)

        # Update the number of credited units
        self.compute_credited_units()