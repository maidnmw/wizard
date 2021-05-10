from django.urls import include, path
from django.contrib import admin

from app import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('rest_framework.urls')),

    path('api/v1/direction', views.Direction.as_view()),
    path('api/admin/candidates', views.Candidates.as_view()),
    path('api/admin/regions', views.Regions.as_view()),
]
