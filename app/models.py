from app import db
from flask_login import UserMixin
from app import login_manager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class User(UserMixin, db.Model):
    """User model
    UserMixin
    db.Model
    Attributes:
        id:             The unique user identifier
        First name:     The user's first name
        Last name:      The user's last name
        email:          The user email address
        profile pic:    The user pic
        rank:           The user's rank. 1-able to request reviews|2-able to accept reviews|3-manager|4-admin
        num_of_reviews: The amount of reviews needed by the user
    """
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String, index=True)
    last_name = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)
    profile_pic = db.Column(db.String, index=True)
    rank = db.Column(db.Integer)
    num_of_reviews = db.Column(db.Integer)
    team = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<User {}>'.format([self.id,self.first_name,self.last_name,self.email,self.profile_pic])


    def get(uid):
        for user in db.session.query(User).filter(User.id==uid):
         print(type(user))
        
        return user

    def get_name(uid):
        user = User.get(uid)
        return user.first_name + ' ' + user.last_name
    
    def get_rank(id):
        user = User.get(id)
        print(user)
        return user.rank

    def setRank(id, rank):
        user = User.get(id)
        user.rank = rank
        """
            please delete this later
        """
        if(rank==1):
            user.num_of_reviews = 3
        elif(rank==2):
            user.num_of_reviews = 2
        else:
            user.num_of_reviews = 1

        db.session.commit()
    
    def addToTeam(id, team):
        user = User.get(id)
        user.team = team
        db.session.commit()

    def search(option, text):
        namelist = []
        if (option=='name'):
            users = db.session.query(User)
            for x in users:
                name = x.first_name.lower() + ' ' + x.last_name.lower()
                email = x.email
                if text in name:
                    namelist.append(name)
                    namelist.append(email)
            return namelist
        elif (option=='team'):
            
            team = Teams.teamList()
            for x in team:
                if text in x:
                    namelist.append(teams.team)
            return namelist
        elif (option=='role'):
            namelist.append('requestor')
            namelist.append('reviewer')
            namelist.append('manager')
            namelist.append('admin')
            return namelist
    
    def setRequiredReviews(option, num, text):
        if option == 'name':
            users = db.session.query(User).filter(User.email==text)
            for x in users:
                x.num_of_reviews = num
            db.commit()
        elif option == 'team':
            users = db.session.query(User).filter(User.team==text)
            for x in users:
                x.num_of_reviews = num
            db.commit()
        elif option == 'role':
            i = 1
            if text == 'reviewer':
                i =2
            elif text == 'manager':
                i = 3
            elif text == 'admin':
                i = 4
            users = db.session.query(User).filter(User.rank == i)
            for x in users:
                x.num_of_reviews = num
            db.commit()
        elif option == 'all':
            users = db.session.query(User)
            for x in users:
                x.num_of_reviews = num
            db.commit()

   
class Review(db.Model):
    """
    Code Review Request Model
    Attributes:
    id:                The identitifer of the review
    Title:             The title of the review
    Date:              If status - 0, date means date review was created. If status - 1 proposed dateTime for code review. 
                       If status - 2 the dateTime the code review will happen. If status - 3 date code review was completed
    Status:            Status - 0 means code review has been rerquested but is waiting a reviewer. Status - 1 means reviewer and requestor are deciding a dateTime. 
                       Status - 2 means the dateTime has been agreed and is in progress and is waiting feedback. Status - 3 means code review is compplete
    Description:       The description of the code review
    Biling Address:    The biling address for the code review
    RequestorID:       The id of the requestor
    Requestor Name:    The name of the requestor
    ReviewerID:        The id of the reviewer
    pic
    Reviewer Name:     The name of the reviewer 
    last changed:      Stores the id of the person who last proposed the date
    tags:              Tags on Review
    tagString:         The String format of tags
    """   

    id = db.Column(db.Integer, index=True, unique=True, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    biling = db.Column(db.String)
    status = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable = True)
    requestor = db.Column(db.String, nullable=True)
    requestor_name = db.Column(db.String, nullable=True)
    pic = db.Column(db.String, nullable=True)
    reviewer = db.Column(db.String, nullable=True)
    reviewer_name = db.Column(db.String, nullable=True)
    last_changed = db.Column(db.String, nullable=True)
    tags = db.relationship('reviewTags', back_populates='review')
    tagString = db.Column(db.String, nullable=True)
    #feedback_response = db.relationship('FeedbackResponse', back_populates='review')
    

    def __repr__(self):
        return '<Review {}>'.format([self.id,self.title,self.description,self.biling,self.status,self.date,self.requestor,self.requestor_name,self.reviewer,self.reviewer_name])

    def get(rid):
        for review in db.session.query(Review).filter(Review.id==rid):
            print(type(review))
            print(review)
        return review
    
    def change_status(int, review_id,reviewer_id,reviewer_name,date):
       review = Review.get(review_id)
       review.status = int
       review.reviewer = reviewer_id
       review.reviewer_name = reviewer_name
       review.date = date
       review.last_changed = reviewer_id
       db.session.commit()
    
    def accept_review(id):
        review = Review.get(id)
        review.status= 3
        review.last_changed=''
        db.session.commit()

    def setTags(tags, id):
        for tag in tags:
            print('777777777777777777777777')
            print(tag.strip(','))
            tag = tag.strip(',')
            tag.lower()
            exist = Tag.query.filter_by(tag=tag).first()
            if exist == None:
                new_tag = Tag(tag=tag)
                db.session.add(new_tag)
                exist = Tag.query.filter_by(tag=tag).first()
            review_tag = reviewTags(review_id=id,tag_id=exist.id) 
            db.session.add(review_tag)
            db.session.commit()
            Review.setTagString(id)

    def setTagString(id):
        text = ""
        for tag in db.session.query(reviewTags).filter(reviewTags.review_id == id):
            text = text + '    ' + Tag.tagValue(tag.tag_id)
        review = Review.get(id)
        review.tagString = text
        db.session.commit()

    def getReview(id):
        for review in db.session.query(Review).filter(Review.id==id):
         print(type(review))
        
        return review            

class Tag(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, index=True)
    review = db.relationship('reviewTags', back_populates='tag')

    def __repr__(self):
        return '<Tag: {}>'.format([self.id, self.tag])

    def tagValue(id):
        tag = db.session.query(Tag).filter(Tag.id==id).first()
        return tag.tag

class reviewTags(db.Model):
    """

    """

    review_id = db.Column(db.Integer, db.ForeignKey(Review.id), primary_key=True)
    review = db.relationship('Review',back_populates='tags')
    tag_id = db.Column(db.Integer, db.ForeignKey(Tag.id), primary_key=True)
    tag = db.relationship('Tag',back_populates='review')
    
class Teams(db.Model):
    """
    So the purpose of this table is to keep track of teams. I think there is an easier way to do this but idk what it is.
    this table is only here to give a list of teams to the route team so that a dropdown menu in admin apge can be filled

    I figured it out... you use this to add people to multiple teams

    """
    team = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return '{}'.format(self.team)

    def teamList():
        teams = []
        for team in db.session.query(Teams):
            print(team)
            teams.append(team)
        print(teams)
        print(len(teams))
        return teams
    
    def addTeam(text):
        team = Teams()
        team.team = text.lower()
        db.session.add(team)
        db.session.commit()

class Question(db.Model):
    """
    list of questions to ask
    """

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    response = db.relationship('Response', back_populates='question')

    def __repr__(self):
        return '<Question {}>'.format([self.id,self.question,self.response])

    def addQuestion(text):
        question = Question()
        question.question = text
        db.session.add(question)
        db.session.commit()

    def questionList():
        questions = []
        for question in db.session.query(Question):
            print(question.question)
            questions.append(question.question)
            questions.append(question.id)
        return questions

    def questionText(id):
        question = db.session.query(Question).filter(Question.id == id).first()
        return question.question

class Feedback(db.Model):
    """
    feedback
    """
    id = db.Column(db.Integer, primary_key=True)
    feedback_response = db.relationship('FeedbackResponse',back_populates='feedback')

    def __repr__(self):
        return '<Feedback {}>'.format([self.id])

    def addFeedback(user_id, questions, responses, review_id):
        
        feedback = Feedback()
        db.session.add(feedback)
        db.session.commit()
        FeedbackResponse.populate(feedback.id, user_id, review_id, questions, responses)
        db.session.commit()



class FeedbackResponse(db.Model):
    """
    hmmmm why do i need Feedback?
    """

    id = db.Column(db.Integer, primary_key=True)
    response = db.relationship('Response', back_populates='feedback_response')
    feedback_id = db.Column(db.Integer, db.ForeignKey(Feedback.id))
    feedback = db.relationship('Feedback', back_populates='feedback_response')
    review_id = db.Column(db.Integer)
    feedbackType = db.Column(db.Integer)
    #review = db.relationship('Review', back_populates='feedback_response')

    def __repr__(self):
        return '<FeedbackResponse {}>'.format([self.id,self.feedback_id, self.review_id,self.feedbackType])
    
    def populate(feedback_id, user, review_id, questions, responses):
        print('44444444444444444444444444')
        review = Review.getReview(review_id)
        if review.last_changed=='':
            review.last_changed = user
        else:
            review.status = 4
        if (user==review.requestor):
            feedback_type = 0
        else:
            feedback_type = 1

        feedback_response = FeedbackResponse()
        print(feedback_id)
        print(type(feedback_id))
        feedback_response.feedback_id = feedback_id
        feedback_response.review_id = review_id
        feedback_response.feedbackType = feedback_type
        print(feedback_response)
        db.session.add(feedback_response)
        db.session.commit()
        i = 0
        for x in responses:
            response = Response(feedback_response_id = feedback_response.id,question_id=questions[i], answer = x)
            i = i + 1
            db.session.add(response)
        print('555555555555555555555555555555')

    def review(user_id,review_id):
        review = Review.get(review_id)
        answers = []
        if user_id == review.requestor:
            feedback = db.session.query(FeedbackResponse).filter(FeedbackResponse.review_id==review_id).filter(FeedbackResponse.feedbackType==0).first()
            for x in db.session.query(Response).filter(Response.feedback_response_id == feedback.id):
                answers.append(Question.questionText(x.question_id))
                answers.append(str(x.answer))
            print(answers)
            return answers
        else:
            feedback = db.session.query(FeedbackResponse).filter(FeedbackResponse.review_id==review_id).filter(FeedbackResponse.feedbackType==1).first()
            for x in db.session.query(Response).filter(Response.feedback_response_id == feedback.id):
                answers.append(Question.questionText(x.question_id))
                answers.append(str(x.answer))
            print(answers)
            return answers



class Response(db.Model):
    """
        response to question
    """
    feedback_response_id = db.Column(db.Integer, db.ForeignKey(FeedbackResponse.id), primary_key=True)
    feedback_response = db.relationship('FeedbackResponse', back_populates='response')
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id), primary_key=True)
    question = db.relationship('Question',back_populates='response')
    answer = db.Column(db.Integer)

    def __repr__(self):
        return '<Response {}>'.format([self.feedback_response_id,self.question_id,self.review_id,self.answer])