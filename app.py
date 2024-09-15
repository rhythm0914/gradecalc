from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_required_grades(prelim_grade):
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0, 100)

    # Validate preliminary grade
    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 and 100."

    # Calculate required average for midterms and finals
    current_total = prelim_grade * prelim_weight
    required_total = passing_grade - current_total
    min_required_average = required_total / (midterm_weight + final_weight)

    # Check if the user has already passed
    if prelim_grade >= passing_grade:
        return f"Keep working hard and stay focused. You can do it! Required Grade for Midterms and Finals: {min_required_average:.2f}%"

    # Check if the required average exceeds 100
    if min_required_average > 100:
        return "Error: It is not possible to achieve the passing grade with this preliminary score."

    # Ensure the required average is not below 0
    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]
    
    return f"Required Grade for Midterms and Finals: {min_required_average:.2f}%"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            prelim_grade = float(request.form['prelim_grade'])
            result = calculate_required_grades(prelim_grade)
        except ValueError:
            result = "Error: Invalid input. Please enter a valid number."
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
