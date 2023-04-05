from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from users.models import Follow, User


class UsersCreateSerializer(UserCreateSerializer):
    """Обработка запросов создания пользователя"""
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Невозможно создать пользователя с таким именем'
            )
        return value


class UsersInfoSerializer(UserSerializer):
    """Вывод информации о пользователе"""
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=object.id).exists()


class FollowSerializer(UsersInfoSerializer):
    """Добавление/удаление/просмотр подписок"""
    recipes = SerializerMethodField(read_only=True)
    recieps_count = SerializerMethodField(read_only=True)

    class Meta(UsersInfoSerializer.Meta):
        fields = UsersInfoSerializer.Meta.fields + ('recieps', 'recieps_count')

    def get_recieps(self, object):
        from .recipes import RecipeShowInfoSerializer
        request = self.context.get('request')
        context = {'request': request}
        recipe_limit = request.query_params.get('recipe_limit')
        queryset = object.reciepe.all()
        if recipe_limit:
            queryset = queryset[int:(recipe_limit)]
            return RecipeShowInfoSerializer(queryset,
                                            context=context,
                                            many=True).data

    def get_recipes_count(self, object):
        return object.recipes.count()
