from flask import redirect, request, render_template, Blueprint, url_for, flash
from flask_bootstrap import Bootstrap
import requests
import json
from oauthlib.oauth2 import WebApplicationClient
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import or_
from app.models import User, Review, Teams, Question, Feedback, FeedbackResponse
from app.forms import CreateForm, DateForm
from app import db, login_manager
import datetime

#from app import app


app = Blueprint('app', __name__)

GOOGLE_CLIENT_ID ='856122308427-29ccsisqdr637u58u4k2dmoo5aom68df.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'YjwznTE9_1qaccXUFxiUO4L2'
GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

#login_manager = LoginManager()
#login_manager.init_app(app)
    # OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

    # Flask-Login helper to retrieve a user from our db
#@login_manager.user_loader
#def load_user(user_id):
    #return User.get(user_id)

      # Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        #return (

        #User.addToTeam('109651862078448085401', None)
        return render_template('index.html')
            #"<p>Hello, {}! You're logged in! Email: {}</p>"
            #"<div><p>Google Profile Picture:</p>"
            #'<img src="{}" alt="Google profile pic"></img></div>'
            #'<a class="button" href="/logout">Logout</a>'.format(
            #    current_user.first_name, current_user.email, current_user.profile_pic
            #)
        #)
    else:
        return render_template('index.html')
        #return '<a class="button" href="/login">Google Login</a>'

@app.route("/home", methods=['GET', 'POST'])
def home(): 
    forms = DateForm()
    if request.method== 'POST':
        id = request.form['id']
        Review.accept_review(id)
        return redirect(url_for("app.home"))
    proposed_reviews = Review.query.order_by(Review.id).filter(Review.status==2).filter(or_(Review.requestor == current_user.id, Review.reviewer == current_user.id)).filter(Review.last_changed == current_user.id)
    received_reviews = Review.query.order_by(Review.id).filter(Review.status==2).filter(or_(Review.requestor == current_user.id, Review.reviewer == current_user.id)).filter(Review.last_changed != current_user.id)
    progress_reviews = Review.query.order_by(Review.id).filter(Review.status==3).filter(or_(Review.requestor == current_user.id, Review.reviewer == current_user.id))
    completed_reviews = Review.query.order_by(Review.id).filter(Review.status==4).filter(or_(Review.requestor == current_user.id, Review.reviewer == current_user.id)).order_by(Review.date).limit(4)
    if forms.validate_on_submit:
        print('8888888888888888888888888888888888888888888888888')
    
  
   
    return render_template('home.html', user=current_user, forms=forms,proposed_reviews=proposed_reviews, received_reviews=received_reviews, progress_reviews=progress_reviews, completed_reviews=completed_reviews)

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    print('+++++++++++++++++++++++++++')
    #print(client.prepare_token_request(token_endpoint,authorization_response=request.url,redirect_url=request.base_url,code=code,)
    print(token_url)
    print(headers)
    print(body)
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    print(token_response)
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        _id = userinfo_response.json()["sub"]
        _email = userinfo_response.json()["email"]
        _picture = userinfo_response.json()["picture"]
        f_name = userinfo_response.json()["given_name"]
        l_name = userinfo_response.json()["family_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id=_id, first_name=f_name, last_name = l_name, email=_email, profile_pic=_picture, rank=1, num_of_reviews=3
    )

    # Doesn't exist? Add to database
    exists = db.session.query(User.id).filter_by(id=_id).scalar() is not None
    if not exists:
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user, remember=True)

    # Send user back to homepage

    return redirect(url_for("app.home"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/requestor", methods=['GET', 'POST'])
def requestor():
    cform = CreateForm()
    if cform.validate_on_submit():
        print(current_user.first_name)
        review = Review(title=cform.title.data, description=cform.description.data, biling=cform.biling.data, status = 1, requestor = current_user.id, requestor_name=User.get_name(current_user.id), date = datetime.datetime.now(), pic=current_user.profile_pic)
        db.session.add(review)
        db.session.commit()       
        tags=cform.tags.data
        print(tags)
        tag_list=tags.split(',')
        print('4444444444444444')
        print(tag_list)
        Review.setTags(tag_list,review.id)
        print('333333333333333333')
        return redirect(url_for("app.requestor"))
    else:
        print('bad')
        
    return render_template('requestor.html', cform=cform, user=current_user)

@app.route("/reviewer", methods=['GET', 'POST'])
def reviewer():
    reviews = Review.query.order_by(Review.id).filter(Review.status==1)
    print(reviews)
    form = DateForm()
    if form.validate_on_submit():
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(form.date.data)
        #id = request.data
        print(form.id.data)
        print(form.submit)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        Review.change_status(2,form.id.data,current_user.id,User.get_name(current_user.id),form.date.data)
    return render_template('reviewer.html', reviews=reviews, form=form, rank=current_user.rank, user=current_user)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    #if(current_user.rank != 4):
        #return render_template('sorry.html')
    users = User.query.order_by(User.id)
    return render_template('admin.html', users=users, user=current_user)

@app.route("/adminQuestions", methods=['POST'])
def adminQuestions():
    if request.method=='POST':
        question = request.form['question']
        print(question)
        Question.addQuestion(question)
    return '1'   
    

@app.route("/user", methods=['GET'])
def user():
    id = request.args['id']
    print(id)
    rank = {'rank': User.get_rank(id)}
    
    return rank

@app.route("/rank", methods=['GET', 'POST'])
def rank():
    id = request.form['id']
    rank = request.form['role']
    checked = request.form['checked']
    print(id)
    print(rank)
    print(checked)
    if(rank=='reviewer'):
        print('same')
    else:
        print('not same')

    if(checked==1):
        print('same')
    else:
        print('not same')

    if(rank=='reviewer'):
        if(checked=='1'):
            User.setRank(id,2)        
        else:
            User.setRank(id,1)          
    elif(rank=='manager'):
        if(checked=='1'):
            None
        else:
            User.setRank(id,2)
    elif(rank=='admin'):
        if(checked == '1'):
            User.setRank(id,4)
        else:
            User.setRank(id,3)
    return '1'

@app.route("/manager")
def manager():
   # if(current_user.rank < 3):
    #    return render_template('stop_error.html')
    your_users = User.query.order_by(User.id).filter(User.rank < 4).filter(User.team == current_user.team)
    teamless_users = User.query.order_by(User.id).filter(User.rank < 4).filter(User.team == None)
    return render_template('manager.html', your_users=your_users, teamless_users= teamless_users, user=current_user)

@app.route("/numReviews", methods=['GET', 'POST'])
def numReviews():
    print('here')
    if request.method == 'GET':
        count = 0
        id = request.args['id']
        user = User.get(id)
        for reviews in db.session.query(Review).filter(or_(Review.requestor == id, Review.reviewer == id)):
            count = count + 1
        data = {'count': count, 'num':user.num_of_reviews, 'id':id}
        return data
    elif request.method == 'POST':
        print('here')
        num = request.form['number']
        option = request.form['option']
        text = request.form['value']
        User.setRequiredReviews(option,num,text)
        print('here')
        return '1'

@app.route("/teams", methods=['GET', 'POST'])
def teams():
    if request.method == 'POST':
        if (request.form['data'] == None):
            print('888888888888888888888888888888888\nnonedetected')
            return '1'
        exists = db.session.query(Teams.team).filter_by(team=request.form['data']).scalar() is not None
        if not exists:
            team = Teams()
            team.team = request.form['data']
            db.session.add(team)
            db.session.commit()
        else:
            User.addToTeam(request.form['id'], request.form['data'])

        return '1'
    
    if request.method == 'GET':
        teamList = Teams.teamList()
        teams = {} 
        x = 0
        for i in teamList:
            teams[x] = str(teamList[x])
            x = x + 1
        return teams 

@app.route("/search", methods=['GET'])
def search():
    option = request.args['option']
    text = request.args['text']
    text.lower()
    data= {}
    i = 0
    name_list = User.search(option, text)
    for x in name_list:
        data[i] = str(name_list[i])
        i = i + 1

    return data

@app.route("/test")
def test():
    x = "asd"
    print(x[0:5])
    return render_template('test.html')

@app.route("/feedback", methods=['GET','POST'])
def feedback():
    if request.method == 'GET':
        questionList = Question.questionList()
        print(questionList)
        questions = {}
        x = 0
        for i in questionList:
            questions[x] = questionList[x]
            x = x + 1
        return questions 
    elif request.method == 'POST':
        print(request.form)
        id = request.form['id']
        answers = request.form['answer'].replace('[','').replace(']','').split(',')
        questions = request.form['stuff'].replace('[','').replace(']','').split(',')
        print(id)
        print(answers)
        print(questions)
        Feedback.addFeedback(current_user.id, questions, answers, id)

@app.route("/review", methods=['GET'])
def review():
    id = request.args['id']
    answerList = FeedbackResponse.review(current_user.id,id)
    answers = {}
    x = 0
    for i in answerList:
        answers[x] = answerList[x]
        x = x + 1
    print(answers)
    return answers
   

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
