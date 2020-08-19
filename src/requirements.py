class APCredit:
    """
    An AP Course paired with an exam score. The college classes
    use APCredit to determine how many credits can be applied.
    """

    def __init__(self, course, score):
        self.course = course
        self.score = score

    def __repr__(self):
        return f"Course: {self.course} - Exam score: {self.score}"


class Requirement:
    """
    A requirement posed by a college. It contains a list of
    AP courses that it accepts for credit and keeps track
    of which credits have been applied.
    """

    def __init__(self, name, unit_total, unit_limit, courses):
        """

        :param name: the name of the requirement
        :param unit_total: the total amount of units in the requirement
        :param unit_limit: the maximum amount of credit units that can be applied for this requirement
        :param courses: List of the courses that this requirement accepts
        """
        self.name = name
        self.unit_total = unit_total
        self.unit_limit = unit_limit
        self.courses = courses

        self.credits = set()
        self.credit_units = 0

    def __repr__(self):
        return f"{self.name} - Unit total: {self.unit_total} - Unit limit: {self.unit_limit} - Courses: {self.courses}"

    def add_credit(self, credit, units):
        """

        :param credit: the APCredit to add
        :param units: the amount of units this APCredit is worth
        :return:
        """
        if self.credit_units + units <= self.unit_limit:
            self.credits.add(credit)
            self.credit_units += units

    def clear_credits(self):
        """
        Resets this requirement's credited courses and units. Used for cases in which
        there are limits on the number of applicable credit units and clearing the credits
        is a simple way to meet the limit.
        :return:
        """
        self.credits.clear()
        self.credit_units = 0


class SubRequirement(Requirement):
    """
    A sub-class of the Requirement class, used by Muir College. A SubRequirement represents a
    special stipulation for a base Requirement. For example, Muir College requires students to
    choose one of 12 different focus areas for the Social Sciences requirement. This "1 out of 12"
    is a SubRequirement.
    """
    def __init__(self, name, unit_total, unit_limit, courses, parent_requirement):
        """

        :param name: name of the subrequirement
        :param unit_total: the total amount of units in the requirement
        :param unit_limit: the maximum amount of credit units that can be applied for this requirement
        :param courses: the courses that this requirement accepts
        :param parent_requirement: a reference to the Requirement object that encompasses this SubRequirement
        """
        super().__init__(name, unit_total, unit_limit, courses)
        self.parent_requirement = parent_requirement

    def __repr__(self):
        return f"Parent: {self.parent_requirement.name} - SubRequirement: {self.name} - Courses: {self.courses}"


class WarrenSubRequirement(SubRequirement):
    """
    A special kind of SubRequirement, used by Warren College. Like a regular SubRequirement, it contains
    a parent Requirement. In addition, however, it contains a category attribute that represents the different
    types of Programs of Concentration and Area Studies of Warren College.
    """
    def __init__(self, name, unit_total, unit_limit, courses, parent_requirement, category):
        """

        :param name: name of the subrequirement
        :param unit_total: the total amount of units in the requirement
        :param unit_limit: the maximum amount of credit units that can be applied for this requirement
        :param courses: the courses that this requirement accepts
        :param parent_requirement: a reference to the Requirement object that encompasses this SubRequirement
        :param category: this subrequirement's category
        """
        super().__init__(name, unit_total, unit_limit, courses, parent_requirement)
        self.parent_requirement = parent_requirement
        self.category = category

    def __repr__(self):
        return f"{self.parent_requirement.name}: {self.name} - Category: {self.category}"


