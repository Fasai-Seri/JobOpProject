from django.apps import AppConfig


class JobPostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_post'
    
    def ready(self):
        from jobs import updater
        updater.start()