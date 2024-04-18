from django.urls import path, re_path

from . import views

app_name='job_post'

urlpatterns = [
    path("", views.index, name="index"),
    path("favourite", views.favourite, name="favourite"),
    path("following", views.following, name="following"),
    path("followed_companies", views.followed_companies, name="followed_companies"),
    path("posted_job_posts", views.posted_job_posts, name="posted_job_posts"),
    path("applied_job_posts", views.applied_job_posts, name="applied_job_posts"),
    path("job_post/create", views.create_job_post, name="create_job_post"),
    path("job_post/<int:job_post_id>/edit", views.edit_job_post, name="edit_job_post"),
    re_path("job_post(?:/(?P<job_post_id>[0-9]+))?/$", views.display_job_post, name="display_job_post"),
    path('generate_pdf/<int:job_post_id>', views.generate_pdf, name='generate_pdf'),
    
    #APIs
    path("update_job_post/<int:job_post_id>", views.update_job_post, name="update_job_post"),

    #------------------------------------------------------------------------------------------------------------
    path('toggle_favorite/<int:job_post_id>/', views.toggle_favorite, name='toggle_favorite'),
    path("apply_job/<int:job_post_id>/", views.apply_job, name="apply_job"),
   
]