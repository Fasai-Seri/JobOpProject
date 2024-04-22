from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name='user_profiles'

urlpatterns = [
    path("", views.login_view, name="login"),
    path("<int:user_id>", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("fillinfo", views.fill_info, name="fillinfo"),
    path("create_employer", views.create_employer, name="create_employer"),

    #APIs
    path('get_user/<int:user_id>', views.get_user, name='get_user'),
    path('get_major', views.get_major, name='get_major'),
    path('update_user', views.update_user, name='update_user'),
    path('update_student_resume', views.update_student_resume, name='update_student_resume'),
    path('update_student_portfolio', views.update_student_portfolio, name='update_student_portfolio'),
    path('remove_student_portfolio/<str:file_name>', views.remove_student_portfolio, name='remove_student_portfolio'),
    path('get_company', views.get_company, name='get_company'),
    path('followed_comp', views.followed_comp, name='followed_comp'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)