from job_post.models import JobPost
from datetime import datetime
import pytz



def update_job_post_status():
    
    active_job_posts = JobPost.objects.filter(job_status='active')
    for job_post in active_job_posts:
        if job_post.job_close_date:
            utc=pytz.UTC
            current_datetime = utc.localize(datetime.now()) 
            close_datetime = job_post.job_close_date
            if close_datetime < current_datetime:
                job_post.job_close_date = None
                job_post.job_status = 'inactive'
                job_post.save()
                print(f'Update JobPost {job_post.pk} Successfully')
