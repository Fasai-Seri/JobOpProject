from django.urls import path, re_path

from . import views

app_name='job_post'

urlpatterns = [
    path("", views.index, name="index"),
    path("favourite", views.favourite, name="favourite"),
    path("following", views.following, name="following"),
    path("followed_companies", views.followed_companies, name="followed_companies"),
    re_path("job_post(?:/(?P<job_post_id>[0-9]+))?/$", views.display_job_post, name="display_job_post"),
    path("job_post/<int:job_post_id>/edit", views.edit_job_post, name="edit_job_post"),
    path("job_post/create", views.create_job_post, name="create_job_post"),
    
    #APIs
    path('update_job_desc_file', views.update_job_desc_file, name='update_job_desc_file'),
    path('update_job_requirement_file', views.update_job_requirement_file, name='update_job_requirement_file'),
]