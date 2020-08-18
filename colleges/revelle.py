from .college import College
from.college_constants import BASE_UNIT_QTY


class RevelleCollege(College):
    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        """
        Revelle College has simpler rules for determining credit than some of the other
        colleges. The general process for applying credit is shown in this method.
        :param credits:
        :return:
        """
        # Iterate over the AP Credits
        for cred in credits:
            # Iterate over the college's reqs
            for req in self.requirements:
                # If this AP course fulfills by a college requirement
                if cred.course in req.courses:
                    req.add_credit(cred.course, BASE_UNIT_QTY)

        # Update the number of credited units
        self.compute_credited_units()
