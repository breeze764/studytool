#the study tool website python backend

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
    "to a phenomenon known as the <a href='https://www.phd-education.com.sg/post/the-illusion-of-learning-what-it-is-and-how-to-overcome-it#:~:text=The%20%E2%80%9Cillusion%20of%20learning%E2%80%9D%20is,the%20%E2%80%9Cillusion%20of%20learning%E2%80%9D.' target='_blank' rel='noopener norefferer'>illusion of learning.</a>"),
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

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    #gets the info from our form about how long they want to study
    n_weeks = int(request.form.get('n_weeks'))
    n_hours_per_day = int(request.form.get('hours'))
    goal = int(request.form.get('goal'))
    #a list of days they want to study on
    days_to_study = request.form.getlist('week')
    technique = request.form.get('technique')
    time_of_day = request.form.getlist('time_of_day')

    #if they didn't check any "time of day" checkboxes, render the error page
    if time_of_day == []:
        their_error="You need to select at least one time to study."
        #these two are so the user can get back to the form from the error page, to retry it
        back_button="Back to Calculator"
        back_href="calculator"
        return render_template("error_page.html",their_error=their_error,back_button=back_button,back_href=back_href)
    
    #if they didn't select any days to study, render the error page
    if len(days_to_study) == 0:
        their_error="You need to select at least one day to study on."
        back_button="Back to Calculator"
        back_href="calculator"
        return render_template("error_page.html",their_error=their_error,back_button=back_button,back_href=back_href)

    n_study_sessions = len(time_of_day) #ie, 2, morning and evening

    #calculates how many hours they are going to study and whether they'll achieve their goal
    n_days = len(days_to_study)
    study_time = n_hours_per_day * n_days * n_weeks
    if study_time >= goal:
        goal_ach = "going to"
    else:
        goal_ach = "not going to"

    #calculates study time per sprint (if they have multiple) by first finding the number of whole
    #hours they need to study per session, and then finding the remainder, and converting it into minutes
    t_session = n_hours_per_day // n_study_sessions
    remainder = n_hours_per_day / n_study_sessions - t_session 
    minutes_raw = remainder * 60
    #rounds the minutes up to the nearest quarter of an hour for practicality
    rounding="(Rounded up)."
    if minutes_raw == 0:
        minutes = 0
        rounding = ""
    elif minutes_raw <= 15:
        minutes = 15
    elif minutes_raw <=30:
        minutes = 30
    elif minutes_raw <=45:
        minutes = 45
    elif minutes_raw <=60:
        #we'll round it up to another entire hour
        minutes = 0
        t_session += 1
    else:
        minutes= 0
        t_session += 1

    #personalized instructions based on technique selected
    if technique == "Pomodoro":
        instructions = "You are going to study in 25 minute sprints, taking 5 minute breaks in between."
    elif technique == "Interleaving":
        instructions = "You will focus on different topics, using different study methods each session."
    elif technique == "Both":
        instructions = "You are going to study in 25 minute sprints, taking 5 minute breaks in between, and focusing on different topics and techniques."
    else:
        instructions = ""

    #personalized recommendation based on goal achieved (or not)
    if goal_ach == "going to":
        surplus_t = str(study_time - goal)
        #convert to minutes for practicality
        surplus_per_session = int(surplus_t) / (n_days * n_weeks * n_study_sessions)
        surplus_per_session_mins = str(round(surplus_per_session * 60))
        
        rec = "You're already achieving your goal, so consider raising it, or reducing your study time." \
        "You are studying " + surplus_t + " hours extra overall and " + surplus_per_session_mins + " minutes extra per session."
    else:
        deficit_t = str((goal - study_time)*60)
        mins_plus = str(20 * n_study_sessions * n_weeks * n_days)
        rec = "You currently aren't achieving your study goal. You're " + deficit_t + " minutes short. If you studied just 20 minutes extra per study session, you could study " + mins_plus + " minutes extra overall."

    #make all the ints into strings so they can be printed in html
    study_time = str(study_time)
    goal = str(goal)
    n_study_sessions = str(n_study_sessions)
    t_session = str(t_session)
    minutes = str(minutes)

    return render_template('calculation_results.html',study_time=study_time,goal=goal,goal_ach=goal_ach,
                           days_to_study=days_to_study,n_study_sessions=n_study_sessions,time_of_day=time_of_day,
                           t_session=t_session,minutes=minutes,rounding=rounding,instructions=instructions,rec=rec)

"""---------------------------------Tutorial Two Stuff-----------------------------------------"""

@app.route('/tutorial2')
def plan():
    return render_template('tutorial2.html')

@app.route('/stem')
def sci_math():
    return render_template('stem.html') 

@app.route('/standard_requirements.html',methods=['POST','GET'])
def show_requirements():
    #gets what they typed into searchbar
    their_input = request.values.get('their_input')
    #tries to find it in the database
    try:
        subject_ID = query("SELECT ID FROM Subjects WHERE Name=?",(their_input,))
        subject_ID = subject_ID[0][0]
    except IndexError:
        their_error="There don't seem to be any results for " + their_input + "."
        #these two allow the user to return to this page from the error page
        back_button="Back to Subject Search"
        back_href="stem"
        return render_template("error_page.html",their_error=their_error,back_button=back_button,back_href=back_href)
    #if it's in the database, collect the relevant standards to build a dictionary
    standards = query("SELECT Name, Requirements, Special_Note FROM Standards WHERE Subject_ID=?",(subject_ID,))
    standards_dict = {}
    extra_spaces = []
    #line counter will count how much space this subject takes up on the page
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
        #if this standard has a special note with it in the database, carry that over
        if standard[2]:
            special_note = standard[2]
        else:
            special_note = ""
    #no matter how many requirements and standards per subject, I want the html page to have same length
    #so for shorter subjects, I build a list of extra space up, to print later
    lines_remaining = 38 - line_counter
    if lines_remaining > 0:
        n = 0
        #building up an appropriate amount of extra space depending how long subject was
        while n <= lines_remaining:
            extra_spaces.append("")
            n += 1
    
    line_counter = int(line_counter)

    return render_template("standard_requirements.html",standards_dict=standards_dict,extra_spaces=extra_spaces,line_counter=line_counter,special_note=special_note) 

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

@app.route('/motivation')
def motivation():
    return render_template('motivation.html')

@app.route('/understanding')
def understanding():
    return render_template('understanding.html')

@app.route('/memorizing')
def memorizing():
    return render_template('remembering.html')

"""--------------------------------Extra Stuff-----------------------------------"""

@app.route('/settings')
def settings():
    return render_template('settings.html')

#executes a query to the sqlite database and returns the results
def query(query,args=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query,args)
    rows = cur.fetchall()
    conn.close()
    return rows

#something I'm only using for testing
@app.route('/crappy_dumpster')
def display_random_stuff():
    #re define this each time I want to print something different
    return render_template("testingstuff.html")


if __name__ == '__main__':
    app.run(debug=True)