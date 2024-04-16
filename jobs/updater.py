from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update_job_post_status

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_job_post_status, 'interval', seconds=1)
    scheduler.start()
    print('Check Successfully')