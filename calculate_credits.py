from flask import Flask
from src.requirements import APCredit
from src.init_college import init_colleges


def calculate_credits(courses):
    """
    Applies the given List of credits to each undergraduate college. Returns a List of strings
    describing which credits were applied for each college.
    :param courses: List of names of AP Courses
    :return: a List of strings describing which credits were applied for each college.
    """

    # Create the List of APCredits: assume a score of 5 for all exams
    ap_credits = [APCredit(course, 5) for course in courses]

    # Initialize the colleges
    colleges = init_colleges()

    # Apply credits for each college and collect results
    results = []
    for college in colleges:
        college.apply_credits(ap_credits)
        results.append(college.get_results_str())

    # Return the list of results
    return results


app = Flask(__name__)

@app.route("/")
def main():
    credits = ["AP Calculus AB", "AP Psychology"]
    results = calculate_credits(credits)
    return results[0]


if __name__ == "__main__":
    app.run()
