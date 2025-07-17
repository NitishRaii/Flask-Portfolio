from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import re

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Contact Model
class Contact(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    reason = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.String(12), nullable=True)

    def __init__(self, name: str, phone: str, email: str, reason: str) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.reason = reason
        self.date = datetime.now()

    def __repr__(self) -> str:
        return self.name

# Error Handlers
@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', message="Bad Request"), 400

@app.errorhandler(404)
def err_404(e):
    return render_template('error.html', message='404 Page Not Found'), 404

# Routes
@app.route('/')
def main_page():
    return render_template('index.html', title='Dhrumil Mistry - Homepage')

@app.route('/home')
def home():
    return render_template('base.html', title='Base')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    contact_info_included = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        reason = request.form.get('reason', '').strip()

        contact_info_included = False
        if 10 <= len(phone) <= 13 and re.fullmatch(r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$', phone):
            entry = Contact(name, phone, email, reason)
            db.session.add(entry)
            db.session.commit()
            contact_info_included = True

    return render_template('contact.html', title='Contact Page', contact_status=contact_info_included)

@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects")
