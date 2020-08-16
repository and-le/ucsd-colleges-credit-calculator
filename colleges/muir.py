from .college import College
from .college_constants import BASE_UNIT_QTY, LARGER_UNIT_QTY, AP_CHEM


class MuirCollege(College):

    def __init__(self, name, requirements, subrequirements):
        super().__init__(name, requirements)
        self.subrequirements = subrequirements

    def compute_unit_total(self, requirements):
        # Compute total number of units
        self.unit_total = 0
        for r in self.requirements:
            self.unit_total += r.unit_total

        # Out of the Fine Arts, Foreign Language, and Humanities categories, only 2 are chosen.
        # Each category contains 12 units
        self.unit_total -= 12

    def apply_credits(self, credits):
        # Iterate over AP Credits
        for cred in credits:
            # Iterate over college Requirements
            for req in self.requirements:
                # If the APCredit fulfills a Requirement
                if cred.course in req.courses:
                    # Iterate over SubRequirements
                    for subreq in self.subrequirements:
                        is_subreq = False
                        # If the AP Credit fulfills a SubRequirement
                        if cred.course in subreq.courses:

                            # Special case: AP Chemistry fulfills the entire Math or Natural Sciences Requirement
                            if cred.course == AP_CHEM:
                                subreq.add_credit(cred.course, LARGER_UNIT_QTY)
                            else:
                                subreq.add_credit(cred.course, BASE_UNIT_QTY)

                            is_subreq = True

                    # If the APCredit does not fulfill a subrequirement,
                    # then it fulfills only a Requirement
                    if not is_subreq:
                        req.add_credit(cred.course, BASE_UNIT_QTY)

                        # For Requirements that have SubRequirements, choose the SubRequirement
        # that maximizes the number of credits applied

        max_subreqs = {subreq.parent_requirement.name: None for subreq in self.subrequirements}
        for subreq in self.subrequirements:
            parent_name = subreq.parent_requirement.name

            # Initialize the max subrequirement
            if not max_subreqs.get(parent_name):
                max_subreqs[parent_name] = subreq

            else:
                # If a SubRequirement with more applied credits is found
                if subreq.credit_units > max_subreqs[parent_name].credit_units:
                    max_subreqs[parent_name] = subreq

        # Replace the Requirement credits with the maximizing SubRequirement's credits
        for req in self.requirements:
            # Only check Requirements with SubRequirements
            if max_subreqs.get(req.name):
                req.credits = max_subreqs[req.name].credits
                req.credit_units = max_subreqs[req.name].credit_units

        # Update the number of credited units
        self.compute_credited_units()