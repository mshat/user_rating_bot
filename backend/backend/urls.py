from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/v1/', include('user_rating.urls')),
    path('tasks/', include('tasks.urls')),
]