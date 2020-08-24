from src.init_college import init_colleges
from src.requirements import APCredit


def calculate_credits(credits):
    """
    Applies the given List of credits to each undergraduate college. Returns a List of objects
    describing which credits were applied for each college.
    :param credits: List of APCredits
    :return: a List of strings describing which credits were applied for each college.
    """

    # Initialize the colleges
    colleges = init_colleges()

    # Apply credits for each college and collect results
    results = []
    for college in colleges:
        college.apply_credits(credits)
        result = college.get_college_result()
        results.append(result)

    # Return the list of results
    return results
