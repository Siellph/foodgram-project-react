from api.views.recipes import IngredientViewSet, RecipeViewSet, TagViewSet
from api.views.base_api import BaseAPIRootView
from api.views.users import UsersViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'


class RuDefaultRouter(DefaultRouter):
    """Показывает описание главной страницы API на русском языке.
    """
    APIRootView = BaseAPIRootView


router = RuDefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
