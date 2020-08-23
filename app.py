from flask import Flask, render_template, request, jsonify

from calculate_credits import calculate_credits
from src.error_handling import is_valid_exam_score
from src.requirements import APCredit

app = Flask(__name__)

@app.route("/")
def main():

    # results = calculate_credits(credits)
    # # Return the results as a string
    # return "^".join(results)

    return render_template("index.html")


@app.route('/data')
def data():
    # Parse the Course Name - Score pairs
    num_courses = int(len(request.args) / 2)
    course_names = []
    course_scores = []
    for i in range(num_courses):
        # Validate the score input. If the score is invalid, do not count the corresponding AP course
        score = request.args.get(f"courses[{i}][score]")
        if is_valid_exam_score(score):
            course_names.append(request.args.get(f"courses[{i}][course]"))
            course_scores.append(request.args.get(f"courses[{i}][score]"))

    # Create the APCredits
    credits = [APCredit(name, score) for (name, score) in zip(course_names, course_scores)]

    # Apply the credits to each college
    results = calculate_credits(credits)
    data = {"results" : results}
    return data


if __name__ == "__main__":
    app.run(debug=True)
