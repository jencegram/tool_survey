from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "5300749"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/completion')
def completion_page():
    return render_template('completion.html')

# Define the route for handling questions and the corresponding view function
@app.route('/questions/<int:question_index>', methods=['GET'])
def question(question_index):
    # Checks if the user is trying to go out of order
    if question_index != len(responses):
        flash('You are trying to access an invalid question!')
        return redirect(f'/questions/{len(responses)}')
    # Checks if the user has answered all the questions in survey
    if len(responses)== len(satisfaction_survey.questions):
        return redirect(('/completion'))

    # Gets current question from the satisfaction_survey instance
    current_question = satisfaction_survey.questions[question_index]
    # Render the template and pass the current question and question index as variables
    return render_template('question.html', question=current_question, question_index=question_index)

@app.route('/answer', methods=['POST'])
def answer():
    # Get the selected answer from the form data
    selected_answer = request.form.get('answer')

    # Store the user's answer in the responses list
    responses.append(selected_answer)

    # Determine the index of the next  question
    next_question_index = len(responses)

    # Check if there are more questions remaining
    if next_question_index < len(satisfaction_survey.questions):
        # Redirect to the next question
        return redirect(f'/questions/{next_question_index}')
    else:
        # Redirect to the completion page
        return redirect('/completion')
    
