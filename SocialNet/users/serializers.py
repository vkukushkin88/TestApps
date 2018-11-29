
from django.conf import settings
from rest_framework import serializers
from .models import User, UserAccount

from email_hunter import EmailHunterClient


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ('about', )
        read_only_fields = ('user', )


class UserSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(many=False, allow_null=True,
                                         read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'username', 'is_staff',
            'user_account', 'password')
        write_only_fields = ('password', )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.select_related('user_account')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        client = EmailHunterClient(settings.HUNTER_TOKEN)
        # hunter_check = client.verify(data['email'])
        # # TODO: other part of hunter result can be used to checks and it could
        # # be stored with user for future
        # if hunter_check['status'] != 'success':
        #     raise serializers.ValidationError('Email is not valid.')

        return super(UserSerializer, self).validate(data)

