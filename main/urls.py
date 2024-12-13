from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')), 
    path('accounts/', include('allauth.urls')),
    path('studyspace/', include('studyspace.urls')),
    
]
