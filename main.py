from flask import Flask, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import ContactForm
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)

app.secret_key = "Secret"
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(20))


@app.route("/")
def home():
    return render_template("index.html", params=params)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit() and request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get("message")
        entry = Contact(name=name, phone=phone, email=email, message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash('Thank you ' + name + ' for contacting us')
        return redirect('/contact')
    return render_template('contact1.html', params=params, form=form)


@app.route('/signup')
def signup():
    form = ContactForm()
    return render_template('signup.html', form=form)


@app.route("/blog")
def blog():
    return render_template("blog.html", params=params)


@app.route("/spiti")
def spiti():
    return render_template("spiti-valley.html", params=params)


@app.route("/chopta")
def chopta():
    return render_template("chopta.html", params=params)


@app.route("/mysore")
def mysore():
    return render_template("coorg.html", params=params)


if __name__ == "__main__":
    app.run(debug="True")
