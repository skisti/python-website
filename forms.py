from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, NumberRange


class ContactForm(FlaskForm):
    name = StringField("Full Name:", validators=[InputRequired(), Length(min=3, message="Please enter a valid name.")])
    phone = IntegerField("Phone:", validators=[InputRequired(), NumberRange(min=8, max=15, message="Please enter valid phone number")])
    email = StringField("Email Address:", validators=[InputRequired(), Email()])
    message = TextAreaField("Message")
    submit = SubmitField("Send Message")
