from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.book import Book
from .models.copy import Copy
from .models.trade import Trade
from .models.mango import Mango
from .models.user import User

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn',
                  'genre', 'pages', 'image', 'published')


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ('id', 'book', 'owner')


class CopyReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    owner = serializers.SlugRelatedField(read_only=True, slug_field='email')

    # book = serializers.StringRelatedField(many=True, read_only=True)
    # print('THIS IS THE BOOK', book)

    class Meta:
        model = Copy
        fields = '__all__'


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'

class TradeReadSerializer(serializers.ModelSerializer):
    copy_from = CopyReadSerializer()
    copy_to = CopyReadSerializer()
    from_user = serializers.SlugRelatedField(read_only=True, slug_field='email')
    to_user = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Trade
        fields = '__all__'

# class TradeCreateSerializer(serializers.ModelSerializer):
#     # copy_from = CopySerializer()
#     # copy_to = CopySerializer()
#     # from_user = copy_from['owner']
#     # to_user = copy_from['owner']
#     class Meta:
#         model = Trade
#         fields = '__all__'


class MangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')
