from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/target/', include('target.urls')),
    path('api/word/', include('word.urls')),
    path('api/daily-mission/', include('daily_mission.urls')),

]
