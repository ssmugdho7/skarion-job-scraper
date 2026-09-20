from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import run_scraper
from datetime import datetime

def job_scraping_task():
    print(f"[{datetime.now()}] Starting scheduled job scraping...")
    run_scraper()
    print(f"[{datetime.now()}] Finished scheduled job scraping.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Run every 4 hours
    scheduler.add_job(job_scraping_task, 'interval', hours=4)
    print("Scheduler started. Running job scraper every 4 hours.")
    
    # Run once at startup
    job_scraping_task()
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
