from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.users import UsersViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
