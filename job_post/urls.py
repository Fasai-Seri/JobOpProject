from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("companies", views.companies, name="companies"),
    path("create_company", views.create_company, name="create_company"),
    path("favourite", views.favourite, name="favourite"),
    path("following", views.following, name="following"),
    path("followed_companies", views.followed_companies, name="followed_companies")
]