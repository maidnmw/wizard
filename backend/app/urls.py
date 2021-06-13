from django.urls import include, path
from django.contrib import admin

from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('rest_framework.urls')),

    path('api/v1/direction', views.Direction.as_view()),
    path('api/directions_list', views.DirectionsList.as_view()),
    path('api/admin/candidates', views.Candidates.as_view()),
    path('api/admin/regions', views.Regions.as_view()),

    path('api/dev/candidates', views.DevCandidates.as_view()),
    path('api/dev/cities', views.DevCities.as_view()),
    path('api/dev/region_population', views.RegionPopulation.as_view()),
    path('api/dev/all_cities', views.DevAllCities.as_view()),
    path('api/dev/all_users_to_db', views.DbCitiesToUsers.as_view()),
    path('api/dev/all_users_predict', views.DbUsersPredict.as_view()),
]
