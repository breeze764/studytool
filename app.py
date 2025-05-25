#prototype website for the study habits website (very bad)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Question:
    def __init__(self,id,text,correct_answer,explanation):
        self.id = id
        self.text = text
        self.correct_answer = correct_answer #true or false
        self.explanation = explanation #explains why this was true/false
    
    def is_correct(self,answer):
        return answer.lower() == self.correct_answer.lower()
    
questions = [
    Question(1,"There is no such thing as a visual learner","true","This is true! The learning type theory has been "
    "<a href='https://studytime.co.nz/articles/types-of-learners-dont-exist/' target='_blank' " \
    "rel='noopener noreferrer'>thoroughly debunked.</a> " \
    "The best way to study is not to try and put yourself in a box! There are smarter ways to learn."),
    Question(2,"If I want to study, I should set aside an hour a day to do it","false","This is false! " \
    "It's essential to make goals and stick to them, but you don't have to start with an hour a day. " \
    "It's better to <a href='https://inspirationeducation.co.nz/extended-guides/step-step-guide-acing-ncea-exams/#:~:text=A%20good%20strategy%20is%20to,of%20flashcards%2C%20and%20test%20yourself' " \
    "target='_blank' rel='noopener noreferrer'>work in sprints.</a> This is coming up soon."),
    Question(3,"Re-reading your notes is a good way to study","false","This is false! Writing " \
    "notes is a great way to process information, however re-reading them won't build a deeper understanding. It contributes" \
    "to a phenomenon known as the <a href='https://www.phd-education.com.sg/post/the-illusion-of-learning-what-it-is-and-how-to-overcome-it#:~:text=The%20%E2%80%9Cillusion%20of%20learning%E2%80%9D%20is,the%20%E2%80%9Cillusion%20of%20learning%E2%80%9D.' target='_blank' rel='noopener noreffere'>illusion of learning.</a>"),
    Question(4,"Studying doesn't matter if I'm not naturally good at it","false","This is false! If you are dedicated to your studies you'll be an even better student than those who are 'gifted'" \
    " but not <a href='https://www.psychologytoday.com/nz/blog/the-athletes-way/202105/is-diligence-more-important-students-intelligence' target='_blank' rel='noopener noreferrer'>engaged.</a>"),
    Question(5,"You can improve your results by learning studying techniques","true","This is true! That's what this website is all about. Now are you ready to plan your study?"),
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

@app.route('/answers')
def answers():
    return render_template('answers.html',questions=questions)

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