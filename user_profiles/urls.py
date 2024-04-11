from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("<int:user_id>", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("fillinfo", views.fill_info, name="fillinfo"),

    #APIs
    path('get_user/<int:user_id>', views.get_user, name='get_user'),
    path('get_major', views.get_major, name='get_major'),
    path('update_user', views.update_user, name='update_user'),
    path('update_user_photo', views.update_user_photo, name='update_user_photo'),
    path('update_student_resume', views.update_student_resume, name='update_student_resume'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)