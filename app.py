from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load schemes
with open("schemes.json", "r") as file:
    schemes = json.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():

    age = int(request.form["age"])
    income = int(request.form["income"])
    category = request.form["category"]
    gender = request.form["gender"]
    residency = request.form["residency"]
    education = request.form["education"]
    employment = request.form["employment"]
    disability = request.form["disability"]

    results = []
    eligible_count = 0
    rejected_count = 0

    for scheme_name, scheme in schemes.items():
        reasons = []

        if "min_age" in scheme and age < scheme["min_age"]:
            reasons.append("Age is below minimum requirement.")
        if "max_age" in scheme and age > scheme["max_age"]:
            reasons.append("Age exceeds maximum limit.")

        if "income_limit" in scheme and income > scheme["income_limit"]:
            reasons.append("Income exceeds allowed limit.")
        if "max_income" in scheme and income > scheme["max_income"]:
            reasons.append("Income exceeds allowed limit.")

        if "allowed_categories" in scheme:
            if category not in scheme["allowed_categories"]:
                reasons.append("Category not eligible.")

        if "gender_required" in scheme:
            if gender != scheme["gender_required"]:
                reasons.append("Only " + scheme["gender_required"] + " applicants allowed.")

        if "disability_required" in scheme:
            if disability != scheme["disability_required"]:
                reasons.append("Applicant must have disability.")

        if len(reasons) == 0:
            status = "Eligible"
            eligible_count += 1
        else:
            status = "Rejected"
            rejected_count += 1

        results.append({
            "name": scheme_name.replace("_", " "),
            "status": status,
            "reasons": reasons,
            "documents": scheme.get("required_documents", [])
        })

    return render_template(
        "result.html",
        results=results,
        eligible_count=eligible_count,
        rejected_count=rejected_count
    )

if __name__ == "__main__":
    app.run(debug=True)