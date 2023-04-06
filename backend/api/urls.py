from api.views.recipes import IngredientViewSet, RecipeViewSet, TagViewSet
from api.views.users import UsersViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]