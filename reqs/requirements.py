import csv
from .requirement_constants import *

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
        :param courses: the courses that this requirement accepts
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
        return f"{self.parent_requirement.name}:{self.name} - Category: {self.category}"


def load_requirements(file):
    """
    Returns a List of Requirements from the read file.
    :param file: CSV file to load the requirements for a college from
    :return: a List of Requirement objects
    """
    requirements = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip header
        next(reader, None)
        for row in reader:
            requirements.append(Requirement(row[REQ_NAME_IDX], int(row[REQ_UNIT_TOTAL_IDX]),
                                            int(row[REQ_UNIT_LIMIT_IDX]), row[REQ_CREDIT_IDX:]))

    return requirements


def load_subrequirements(file, parent_requirements):
    """
    Returns a List of SubRequirements from the read file. The parameter
    parent_requirements must be obtained by calling the load_requirements() method first
    :param file: CSV file to load the requirements for a college from
    :param parent_requirements: List of Requirement objects
    :return: a List of Requirement objects
    :return: a List of SubRequirements
    """
    subrequirements = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip header
        next(reader, None)
        for row in reader:

            # Find the parent Requirement whose name matches the one read from the file.
            parent_name = row[SUBREQ_PARENT_IDX]
            parent = None
            for req in parent_requirements:
                if parent_name == req.name:
                    parent = req

            subrequirements.append(SubRequirement(row[SUBREQ_NAME_IDX], int(row[SUBREQ_UNIT_TOTAL_IDX]),
                                                  int(row[SUBREQ_UNIT_LIMIT_IDX]), row[SUBREQ_CREDIT_IDX:],
                                                  parent))

    return subrequirements


def load_warren_subrequirements(file, parent_requirements):
    """
    Returns a List of WarrenSubRequirements from the read file. The parameter
    parent_requirements must be obtained by calling the load_requirements() method first.
    This method is different from load_subrequirements() in that the CSV files for Warren College
    are indexed differently than the Muir College CSV files.
    :param file: CSV file to load the requirements for a college from
    :param parent_requirements: List of Requirement objects
    :return: a List of Requirement objects
    :return: a List of WarrenSubRequirements
    """
    subreqs = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip header
        next(reader, None)
        for row in reader:

            # Find the parent Requirement whose name matches the read from the file.
            parent_name = row[WARR_SUBREQ_PARENT_IDX]
            parent = None
            for req in parent_requirements:
                if parent_name == req.name:
                    parent = req

            warr = WarrenSubRequirement(row[WARR_SUBREQ_NAME_IDX], int(row[WARR_SUBREQ_UNIT_TOTAL_IDX]),
                                        int(row[WARR_SUBREQ_UNIT_LIMIT_IDX]), row[WARR_SUBREQ_CREDIT_IDX:],
                                        parent, row[WARR_SUBREQ_CATEGORY_IDX])
            subreqs.append(warr)
    return subreqs