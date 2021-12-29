from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys
 
app = Flask(__name__)
app.config['SECRET_KEY'] = "bunnyrabbit"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def home():
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions
    if not len(responses) == 0:
        responses.clear()
    return render_template("base.html", title = title, instructions=instructions)

@app.route("/session", methods=["POST"])
def sessions():
    session['responses'] = []
    length = len(responses)
    if not length == 4:
        return redirect(f"/questions/{length}")
    else:
        return redirect("/survey-end")

@app.route("/questions/<num>")
def redirection(num):
    length = len(responses)
    if length == 4:
        return redirect(f"/survey-end")
    else:
        flash("You are trying to access an invalid question")
        return redirect(f"/questions/{length}")

@app.route("/questions/0")
def question_zero():
    question = surveys.satisfaction_survey.questions[0].question
    num = len(responses)
    if not num == 0:
        flash("You are trying to access an invalid question")
        return redirect(f"/questions/{num}")
    else:
        return render_template("question_zero.html", question=question, responses=responses)

@app.route("/questions/1")
def question_one():
    question = surveys.satisfaction_survey.questions[1].question
    num = len(responses)
    if not num == 1:
        flash("You are trying to access an invalid question")
        return redirect(f"/questions/{num}")
    else:
        return render_template("question_one.html", question=question, responses=responses)

@app.route("/questions/2")
def question_two():
    question = surveys.satisfaction_survey.questions[2].question
    less = surveys.satisfaction_survey.questions[2].choices[0]
    more = surveys.satisfaction_survey.questions[2].choices[1]
    num = len(responses)
    if not num == 2:
        flash("You are trying to access an invalid question")
        return redirect(f"/questions/{num}")
    else:
        return render_template("question_two.html",question=question,less=less,more=more, responses=responses)

@app.route("/questions/3")
def question_three():
    question = surveys.satisfaction_survey.questions[3].question
    num = len(responses)
    if not num == 3:
        flash("You are trying to access an invalid question")
        return redirect(f"/questions/{num}")
    else:
        return render_template("question_three.html",question=question, responses=responses)

@app.route("/answers", methods=["POST"])
def answers():
    answer = request.form["answer"]
    responses.append(answer)
    session["answer"] = responses
    num = len(responses)
    if len(responses) < 4:
        return redirect(f"/questions/{num}")
    else:
        return redirect("/survey-end")

@app.route("/survey-end")
def thank_you():
    return "Thank You!"
