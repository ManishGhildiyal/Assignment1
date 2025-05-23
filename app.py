from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)

class TicketRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    event_url = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-tables')
def create_tables():
    db.create_all()
    return "Tables created successfully!"

@app.route('/api/events')
def get_events():
    events = Event.query.all()
    return jsonify([{'name': event.name, 'date': event.date, 'description': event.description, 'url': event.url} for event in events])

@app.route('/get_tickets', methods=['POST'])
def get_tickets():
    email = request.form.get('email')
    event_url = request.form.get('url')
    if email and event_url:
        ticket_request = TicketRequest(email=email, event_url=event_url)
        db.session.add(ticket_request)
        db.session.commit()
    return jsonify({'message': 'Thank you! You will be redirected.', 'url': event_url})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

