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
        id:            The unique user identifier
        First name:    The user's first name
        Last name:     The user's last name
        email:         The user email address
        profile pic:   The user pic
       
    """
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String, index=True)
    last_name = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)
    profile_pic = db.Column(db.String, index=True)

    def __repr__(self):
        return '<User {}>'.format([self.id,self.first_name,self.last_name,self.email,self.profile_pic])


    def get(uid):
        for user in db.session.query(User).filter(User.id==uid):
         print(type(user))
        
        return user

    def get_name(uid):
        user = User.get(uid)
        return user.first_name + ' ' + user.last_name
    
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
    Reviewer Name:     The name of the reviewer 


    """   

    id = db.Column(db.Integer, index=True, unique=True,primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    biling = db.Column(db.String)
    status = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable = True)
    requestor = db.Column(db.Integer, nullable=True)
    requestor_name = db.Column(db.String, nullable=True)
    reviewer = db.Column(db.Integer, nullable=True)
    reviewer_name = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Review {}>'.format([self.id,self.title,self.description,self.biling,self.status,self.date,self.requestor,self.requestor_name,self.reviewer,self.reviewer_name])

    def get(rid):
        for review in db.session.query(Review).filter(Review.id==rid):
            print(type(review))
            print(review)
        return review
    
    def change_status(int, review_id,reviewer_id,reviewer_name,date):
       print('----------------------------------------------')
       review = Review.get(review_id)
       review.status = int
       print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
       print('made')
       review.reviewer = review_id
       print('made')
       review.reviewer_name = reviewer_name
       review.date = date
       db.session.commit()




