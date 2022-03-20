
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from versatileimagefield.serializers import VersatileImageFieldSerializer

from . import models as app_models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = app_models.User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'posts', 'liked_posts')


class UserTokenSerializer(serializers.Serializer):
    user = UserSerializer()
    access_token = serializers.CharField(required=True)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    avatar = VersatileImageFieldSerializer(required=False, allow_null=True, sizes='all_image_size')

    class Meta:
        fields = UserSerializer.Meta.fields

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError('Password and Confirm password must be the same.')
        super().validate(attrs)
        return attrs

    def create(self, validated_data):
        _ = validated_data.pop('confirm_password')
        user = app_models.User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)

        return user, token


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=True)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = app_models.Post
        exclude = ['modified', 'created']
        read_only_fields = ['likes', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        post = super().create(validated_data)
        return post
