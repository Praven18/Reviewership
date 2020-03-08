from app import db
from flask_login import UserMixin
from app import login_manager
from flask_sqlalchemy import SQLAlchemy

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
            print(user)
        
        return user
    
class Review(db.Model):
    """
    Code Review Request Model
    Attributes:
    id:
    Title:
    Date:
    Status:
    Description:
    Biling Address:
    RequestorID:
    ReviewerID:


    """   

    id = db.Column(db.Integer, primary_key=True)

