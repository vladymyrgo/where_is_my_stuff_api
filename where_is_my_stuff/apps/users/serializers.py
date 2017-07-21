# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from rest_auth.serializers import LoginSerializer as RALoginSerializer
from allauth.account.adapter import DefaultAccountAdapter


# Get the UserModel
UserModel = get_user_model()

adapter = DefaultAccountAdapter()


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ('email', )


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = UserDetailsSerializer()


class LoginSerializer(RALoginSerializer):
    """
    Override default LoginSerializer provided by django-rest-auth to add 'too many attempts'
    behavior from django-allauth
    """

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email') or ''
        password = attrs.get('password')

        user = None

        request = self.context.get('request')
        adapter.pre_authenticate(request, **{'username': username, 'email': email})

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials!')
            adapter.authentication_failed(request, **{'username': username, 'email': email})
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs
