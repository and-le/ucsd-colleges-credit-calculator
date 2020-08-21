from flask import Flask, render_template, request, jsonify

from calculate_credits import calculate_credits

app = Flask(__name__)

@app.route("/")
def main():

    # results = calculate_credits(credits)
    # # Return the results as a string
    # return "^".join(results)

    return render_template("index.html")


@app.route('/data')
def data():
    courses = request.args.getlist("courses[]")
    results = calculate_credits(courses)
    data = {"results": results}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
