from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from rest_framework.authtoken.models import Token

from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken


admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.unregister(Token)

admin.site.unregister(EmailAddress)
admin.site.unregister(EmailConfirmation)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
