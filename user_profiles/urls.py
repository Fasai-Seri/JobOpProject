from django.urls import path

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
    path('get_user_type/<int:user_id>', views.get_user_type, name='get_user_type'),
]