from flask import Flask, render_template, request, jsonify

from calculate_credits import calculate_credits
from src.is_valid_exam_score import is_valid_exam_score

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

    # results = calculate_credits(courses)
    # data = {"results" : results}
    return "Plaaceholder"

if __name__ == "__main__":
    app.run(debug=True)
