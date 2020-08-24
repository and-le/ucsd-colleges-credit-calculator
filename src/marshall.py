from .college import College
from .ap_constants import *

MARSHALL_PHYS_COURSES = {AP_PHYS_1, AP_PHYS_2, AP_PHYS_MECH, AP_PHYS_EM}
MARSHALL_8_UNIT_BREADTH_COURSES = {AP_DRAW, AP_2D, AP_3D, AP_MUS, AP_US_HIST, AP_EURO_HIST, AP_WORLD_HIST,
                                   AP_CHIN, AP_FREN, AP_GER, AP_ITA, AP_JAP, AP_SPLA, AP_SPLI}

MARSHALL_SCORE_OF_FOUR_COURSES = {AP_CALC_AB, AP_CALC_BC}

class MarshallCollege(College):

    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        """
        Marshall only credits 1 AP Physics Course. In addition, some courses count for 8 units.
        IMPORTANT: Marshall requires each of the breadth courses to be outside of the field of study of the major.
        The code for Marshall does not consider this when applying credit.
        Aside from these cases, there are no special exceptions.
        :param credits:
        :return:
        """
        # Reset credited units
        self.credited_units = 0

        for cred in credits:
            for req in self.requirements:
                if cred.course in req.courses and cred.score >= AP_SCORE_3:

                    if cred.course in MARSHALL_SCORE_OF_FOUR_COURSES:
                        if cred.score >= AP_SCORE_4:
                            if cred.course == AP_CALC_BC:
                                req.clear_credits()
                                req.add_credit(cred.course, EIGHT_UNITS)
                            else:
                                req.add_credit(cred.course, FOUR_UNITS)

                    # Only 1 physics credit allowed; skip additional physics credits
                    elif (cred.course == AP_PHYS_1) and \
                            (AP_PHYS_2 in req.credits or AP_PHYS_MECH in req.credits or AP_PHYS_EM in req.credits):
                        continue
                    elif (cred.course == AP_PHYS_2) and \
                            (AP_PHYS_1 in req.credits or AP_PHYS_MECH in req.credits or AP_PHYS_EM in req.credits):
                        continue
                    elif (cred.course == AP_PHYS_MECH) and \
                            (AP_PHYS_1 in req.credits or AP_PHYS_2 in req.credits or AP_PHYS_EM in req.credits):
                        continue
                    elif (cred.course == AP_PHYS_EM) and \
                            (AP_PHYS_1 in req.credits or AP_PHYS_2 in req.credits or AP_PHYS_MECH in req.credits):
                        continue

                    # Some AP courses count for 8 units of discplinary breadth.
                    elif cred.course in MARSHALL_8_UNIT_BREADTH_COURSES:
                        req.add_credit(cred.course, EIGHT_UNITS)

                    else:
                        req.add_credit(cred.course, FOUR_UNITS)

        # Update the number of credited units
        self.compute_credited_units()