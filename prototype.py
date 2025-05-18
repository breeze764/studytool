#prototype website for the study habits website (very bad)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Question:
    def __init__(self,id,text,correct_answer,answer_explanation):
        self.id = id
        self.text = text
        self.correct_answer = correct_answer #true or false
        self.answer_explanation = text #a message to flash up and explain the correct answer
    
    def is_correct(self,answer):
        return answer.lower() == self.correct_answer.lower()
    
questions = [
    Question(1,"There is no such thing as a visual learner","true","This is true! Everyone learns best using a variety of methods. Don't believe me?..."),
    Question(3,"Re-reading your notes is a good way to study","false","info"),
    Question(4,"Some people are naturally better at certain subjects","false","info"),
    Question(5,"You can improve your exam results by learning studying techniques","true","info"),
]


#renders the home page when you launch the website
@app.route('/')
def index():
    return render_template('index.html')

#renders the first tutorial page when clicked in the navbar
@app.route('/tutorial1')
def myths():
    return render_template('tutorial1.html',questions=questions)

#renders the second tutorial page when clicked
@app.route('/tutorial2')
def plan():
    return render_template('tutorial2.html')
    
#renders the third tutorial page when clicked
@app.route('/tutorial3')
def how_to():
    return render_template('tutorial3.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    #gets the info from our form about how long they want to study
    days = int(request.form.get('days'))
    hours = int(request.form.get('hours'))
    max_days = int(request.form.get('max_days'))
    study_time = days * hours
    study_time = str(study_time)
    if days < max_days:
        spare_days = max_days - days
        spare_days = str(spare_days)
    else:
        spare_days = 0
    extra_time=(1/3)*days
    extra_time = round(extra_time)
    extra_time=str(extra_time)
    return render_template('time_to_study.html',study_time=study_time,spare_days=spare_days,extra_time=extra_time)

if __name__ == '__main__':
    app.run(debug=True)