Sydney Events Website
Overview
This project is a web application that scrapes event listings for Sydney, Australia, from Eventbrite (https://www.eventbrite.com.au/d/australia--sydney/events/) and displays them on a minimalistic webpage. Users can view event details (name, date, description, URL) and click a "Get Tickets" button to submit their email and be redirected to the original event page. The events are automatically updated daily using a scheduler.
This fulfills the requirements of Assignment 1 for creating a webpage that scrapes and displays Sydney events, developed using open-source tools (Flask, Selenium, BeautifulSoup, SQLite).
Features

Scrapes Sydney events from Eventbrite, including name, date, description, and URL.
Displays events in a clean, card-based layout with a responsive design.
Allows users to submit their email via a form and redirects to the event’s Eventbrite page.
Stores email submissions in a SQLite database for future use.
Automatically updates event listings daily using APScheduler.
Handles duplicates and filters non-Sydney events.

Technologies Used

Backend: Flask, Flask-SQLAlchemy, SQLite
Scraping: Selenium, BeautifulSoup, requests, webdriver-manager
Frontend: HTML, CSS, JavaScript
Automation: APScheduler
Environment: Python 3.8+, pip

Project Structure
event_website/
│
├── app.py                  # Flask application
├── scrape_events.py        # Event scraping script
├── run_scraper.py          # Scheduler for automatic updates
├── config.py               # Flask configuration
├── templates/
│   └── index.html          # Main webpage template
├── static/
│   ├── css/styles.css      # CSS for styling
│   └── js/scripts.js       # JavaScript for dynamic content
├── events.db               # SQLite database
├── page.html               # Debug HTML from scraping
├── scraper.log             # Scraping logs
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Git ignore file

Setup Instructions

Clone the Repository (if using version control):
git clone <repository-url>
cd event_website


Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Initialize the Database:

Start the Flask app:python app.py


Visit http://127.0.0.1:5000/create-tables in a browser to create the events and ticket_request tables.


Run the Scraper:
python scrape_events.py

This scrapes events from Eventbrite and saves them to events.db.

Start the Web Application:
python app.py

Open http://127.0.0.1:5000/ to view the website.

Automate Updates (optional):
python run_scraper.py

Runs the scraper daily to update events.


Usage

View Events: Browse the homepage (http://127.0.0.1:5000/) to see a list of Sydney events.
Get Tickets: Click the "Get Tickets" button, enter your email, and be redirected to the event’s Eventbrite page.
Check Database:from app import db, app, Event, TicketRequest
with app.app_context():
    print("Events:", [(e.id, e.name, e.date, e.description, e.url) for e in Event.query.all()])
    print("Ticket Requests:", [(r.id, r.email, r.event_url) for r in TicketRequest.query.all()])



Notes

The scraper uses Selenium to handle Eventbrite’s dynamic content, with the .event-card selector for event listings.
Duplicates are filtered by event URL, and non-Sydney events are excluded based on "Sydney" in the name or description.
If scraping fails (e.g., Found 0 event elements), check page.html and scraper.log for debugging.
Ensure Chrome is installed for Selenium’s WebDriver.

Challenges Faced

Initial database error (no such table: event) resolved by initializing tables.
Scraping issues (Found 0 event elements) fixed using Selenium and correct selectors.
Duplicate and non-Sydney events addressed with filtering logic.

Future Improvements

Refine selectors for precise data extraction.
Scrape multiple Eventbrite pages for more events.
Add front-end filters (e.g., by date or category).
Send email confirmations using Flask-Mail.

License
This project is open-source and available under the MIT License.
