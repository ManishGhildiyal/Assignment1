
from apscheduler.schedulers.blocking import BlockingScheduler 
from scrape_events import scrape_events

scheduler = BlockingScheduler()
scheduler.add_job(scrape_events, 'interval', hours=24)  
scheduler.start()