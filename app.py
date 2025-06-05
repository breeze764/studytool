#prototype website for the study habits website (very bad)

from flask import Flask, render_template, request, jsonify
import sqlite3

DB_PATH="subjects.db"

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

@app.route('/')
def index():
    return render_template('index.html')

"""---------------------------------Tutorial One Stuff-----------------------------------------"""

@app.route('/tutorial1')
def myths():
    return render_template('tutorial1.html',questions=questions)

@app.route('/answers')
def answers():
    return render_template('answers.html',questions=questions)

"""---------------------------------Calculator Stuff-----------------------------------------"""

@app.route('/pre-calculator')
def info():
    return render_template('pre_calculator.html')

@app.route('/calculator')
def get_hours():
    return render_template("calculator.html")

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
    return render_template('calculation_results.html',study_time=study_time,spare_days=spare_days,extra_time=extra_time)

"""---------------------------------Tutorial Two Stuff-----------------------------------------"""

@app.route('/tutorial2')
def plan():
    return render_template('tutorial2.html')

@app.route('/stem')
def sci_math():
    return render_template('stem.html') 

@app.route('/standard_requirements.html',methods=['POST','GET'])
def show_requirements():
    their_input = request.values.get('their_input')
    try:
        subject_ID = query("SELECT ID FROM Subjects WHERE Name=?",(their_input,))
        subject_ID = subject_ID[0][0]
    except IndexError:
        return render_template("error_page.html",their_input=their_input)
    standards = query("SELECT Name, Requirements, Special_Note FROM Standards WHERE Subject_ID=?",(subject_ID,))
    standards_dict = {}
    thing = []
    line_counter = 0
    for standard in standards:
        string_requirements = standard[1]
        list_requirements = string_requirements.split(",")
        list_requirements_title_caps = []
        for requirement in list_requirements:
            #the only ones which needs special capitalization are DNA and DC because they look silly as Dc and Dna
            if "DNA" not in requirement and "DC" not in requirement:
                requirement = requirement.title()
                list_requirements_title_caps.append(requirement)
            elif "DNA" in requirement:
                list_requirements_title_caps.append("Structure of DNA")
            else:
                list_requirements_title_caps.append("The DC Motor")
            line_counter += 1
        #makes the standard name a key in the dictionary, which maps to a list of requirements
        standards_dict[standard[0]] = list_requirements_title_caps
        if standard[2]:
            special_note = standard[2]
        else:
            special_note = ""
    lines_remaining = 38 - line_counter
    if lines_remaining > 0:
        n = 0
        while n <= lines_remaining:
            thing.append("")
            n += 1
    
    line_counter = int(line_counter)

    #tempoarily overriding what it would normally return to see the output
    #return render_template("testingstuff.html",thing_to_test=standards)
    return render_template("standard_requirements.html",standards_dict=standards_dict,thing=thing,line_counter=line_counter,special_note=special_note) 

@app.route('/essay_subjects')
def essay_tips():
    return render_template('essay_subjects.html')

@app.route('/language_subjects')
def language_tips():
    return render_template('language_subjects.html')

"""---------------------------------Tutorial Three Stuff-----------------------------------------"""

@app.route('/tutorial3')
def how_to():
    return render_template('tutorial3.html')

"""-------------------------------------------------------------------------------------"""

#executes a query to the sqlite database and returns the results
def query(query,args=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query,args)
    rows = cur.fetchall()
    conn.close()
    return rows

#something I'm only using for testing
@app.route('/crappy_dumpster', methods=['POST', 'GET'])
def display_random_stuff():
    #re define this each time I want to print something different
    their_input = request.values.get('their_input')
    subject_ID = query("SELECT ID FROM Subjects WHERE Name=?",(their_input,))
    subject_ID = subject_ID[0][0]
    thing_to_test = query("SELECT Name FROM Standards WHERE Subject_ID=?",(subject_ID,))
    return render_template("testingstuff.html",thing_to_test=thing_to_test)


if __name__ == '__main__':
    app.run(debug=True)