from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name='company'
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:comp_id>", views.comp_info, name="comp_info"),
    path("create_company_page", views.create_company_page, name="create_company_page"),

    #APIs
    path('get_company/<int:comp_id>', views.get_company, name='get_company'),
    path('update_company/<int:comp_id>', views.update_company, name='update_company'),
    path('update_comp_logo/<int:comp_id>', views.update_comp_logo, name='update_comp_logo'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)