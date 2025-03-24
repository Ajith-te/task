from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ride_app.views import RideViewSet


router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
