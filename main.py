from flask import Flask, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates
import re
import secrets


app = Flask(__name__)

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/travellers'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(20))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    message = request.form.get("message")

    if request.method == "POST":
        name = request.form("name")
        phone = request.form("phone")
        email = request.form("email")

        entry = Contact(name=name, phone=phone, email=email, message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash('Thank you ' + name + ' for contacting us')
        return render_template('contact.html')
    else:
        return render_template('contact.html')


@validates("name")
def validate_name(self, key, name):
    if not name:
        raise AssertionError('Name must not be empty')

    return self.name


@validates("phone")
def validate_phone(self, key, phone):
    if not phone:
        raise AssertionError('Phone number must not be empty')
    if not re.match("[0-9]", phone):
        raise AssertionError('Enter the correct phone number')

    return self.phone


@validates('email')
def validate_email(self, key, email):
    if not email:
        raise AssertionError('Enter an email address')
    if not re.match("[A-Z0-9] + @[A-Z0-9.-]+.[A-Z]", email):
        raise AssertionError('Enter the correct email address')

    return self.email


@app.route("/blog")
def blog():
    return render_template("404.html")


@app.route("/spiti")
def spiti():
    return render_template("spiti-valley.html")


@app.route("/chopta")
def chopta():
    return render_template("chopta.html")


@app.route("/mysore")
def mysore():
    return render_template("coorg.html")


if __name__ == "__main__":
    app.run(debug="True")
