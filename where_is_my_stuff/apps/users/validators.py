# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import string

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class GenericValidator(object):
    error_message = ''
    error_code = ''

    def invalid_expression(self, password):
        pass

    def get_help_text(self):
        return self.error_message

    def validate(self, password, user=None):
        if self.invalid_expression(password):
            raise ValidationError(self.error_message, code=self.error_code)

    class Meta:
        abstract = True


class HasUpperValidator(GenericValidator):
    error_message = _('Must contain at least one uppercase letter')
    error_code = 'password_uppercase'

    def invalid_expression(self, password):
        return not any(char in string.ascii_uppercase for char in password)


class HasLowerValidator(GenericValidator):
    error_message = _('Must contain at least one lowercase letter')
    error_code = 'password_lowercase'

    def invalid_expression(self, password):
        return not any(char in string.ascii_lowercase for char in password)


class HasDigitValidator(GenericValidator):
    error_message = _('Must contain at least one digit')
    error_code = 'password_digit'

    def invalid_expression(self, password):
        return not any(char in string.digits for char in password)


class HasSpecialCharacterValidator(GenericValidator):
    error_message = _('Must contain at least one special character')
    error_code = 'password_special'

    def invalid_expression(self, password):
        return not any(char in string.punctuation for char in password)
