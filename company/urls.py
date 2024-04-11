from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:comp_id>", views.comp_info, name="comp_info"),

    #APIs
    path('get_company/<int:comp_id>', views.get_company, name='get_company'),
]