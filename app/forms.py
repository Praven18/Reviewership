from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, ValidationError
from pytz import all_timezones, country_names, common_timezones
from app.models import User

class CreateForm(FlaskForm):
    """
     form for creating a code review

     Fields:
        Title
        Description
        Biling Address
        
    """
    title = StringField('Title:', validators=[InputRequired('A title is required.'), DataRequired()]) 
    description = TextAreaField('Description:', validators=[InputRequired('A description is required.'), DataRequired()]) 
    biling = StringField('Biling address:', validators=[InputRequired('A Biling address is required.'), DataRequired()])
    create = SubmitField('Create')
