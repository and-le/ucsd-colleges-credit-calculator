class College:
    """
    Base class for each UCSD college. A College contains a list of Requirements. It can take a list of APCredits
    and return how many units were applied.
    """

    def __init__(self, name, requirements):
        """
        The requirements for each college are loaded in from a CSV file. 
        :param name:
        :param requirements:
        """
        self.name = name
        self.requirements = requirements

        # Add up the requirement units
        self.unit_total = 0
        self.compute_unit_total(requirements)

        # Name of the subrequirement, if this college has one
        self.subrequirement_name = None

        # Total credited units
        self.credited_units = 0

    def __repr__(self):
        return f"{self.name} College"

    def apply_credits(self, credits):
        """
        Determines which of the given APCredits can be applied for this college, and updates the College's
        fields accordingly. This method must be overridden by the sub-class.
        :param credits: List of APCredits
        :return:
        """
        pass

    def get_requirement(self, name):
        """
        Returns the Requirement with the specified name. This method can be used to access a Requirement object
        so that its credits and credited units can be verified.
        :param: name: the name of the requirement to return
        :return: the Requirement with the specified name; None if no such Requirement exists
        """
        for req in self.requirements:
            if name == req.name:
                return req

        return None

    def compute_unit_total(self, requirements):
        # Compute total number of units
        self.unit_total = 0
        for req in self.requirements:
            self.unit_total += req.unit_total

    def get_unit_total(self):
        return self.unit_total

    def compute_credited_units(self):
        for req in self.requirements:
            self.credited_units += req.credit_units

    def get_credited_units(self):
        return self.credited_units

    def get_net_units(self):
        return self.unit_total - self.credited_units

    def display_requirements(self):
        for r in self.requirements:
            print(r)

    def display_credited_units(self):
        for req in self.requirements:
            if req.credit_units > 0:
                print(f"{req.name} - Applied Credits: {req.credits} - Credited Units: {req.credit_units}")

    def display_results(self):
        print(f"Results for {self}:")
        print(f"{self} has a total of {self.get_unit_total()} units.\n")
        print(f"The following AP Courses were used toward {self} requirements:")
        self.display_credited_units()
        print(f"\n{self.get_credited_units()} units of AP Credit were applied.")
        print(f"\nAfter applying AP Credit, the remaining amount of units is {self.get_net_units()}.")

    def get_credited_units_str(self):
        credited_units_str = ""
        for req in self.requirements:
            if req.credit_units > 0:
                credited_units_str += f"{req.name} - {req.credits} - Credited Units: {req.credit_units}\n"

        return credited_units_str





    def get_results_str(self):
        result_str = ""
        result_str += f"Results for {self}:\n"
        result_str += f"{self} has a total of {self.get_unit_total()} units.\n"
        result_str += f"The following AP Courses were used toward {self} requirements:\n"
        result_str += self.get_credited_units_str()
        result_str += f"\n{self.get_credited_units()} units of AP Credit were applied."
        result_str += f"\nAfter applying AP Credit, the remaining amount of units is {self.get_net_units()}."
        return result_str