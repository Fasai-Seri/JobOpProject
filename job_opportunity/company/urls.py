from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name='company'
urlpatterns = [
    path("", views.index, name="index"),
    re_path("(?P<comp_id>[0-9]+)?$", views.comp_info, name="comp_info"),
    path("create_company_page", views.create_company_page, name="create_company_page"),

    #APIs
    path('get_company/<int:comp_id>', views.get_company, name='get_company'),
    path('get_company_job_posts/<int:comp_id>', views.get_company_job_posts, name='get_company_job_posts'),
    path('update_company/<int:comp_id>', views.update_company, name='update_company'),
    path('follow_company/<int:comp_id>', views.follow_company, name='follow_company'),
    path('favorite/<int:post_id>', views.favorite, name='favorite'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)