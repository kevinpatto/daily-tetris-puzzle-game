# taken from https://sixfeetup.com/blog/custom-password-validators-in-django
# credit goes to the author: Anthony Bosio.

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

# TODO: make validate & get_help_text into static methods, then convert methods in classes to calls

class NumberValidator(object): # fixed wth AI
    def validate(self, password, user=None):
        if not re.search(r"\d", password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code="password_no_number",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 digit, 0-9.")


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class SymbolValidator(object): # fixed with AI
    def validate(self, password, user=None):
        if not re.search(r"""[()[\]{}|`~!@#$%^&*_\-+=;:'",<>./?]""", password):
            raise ValidationError(
                _("The password must contain at least 1 symbol: " +
                  "()[]{}|\\`~!@#$%^&*_-+=;:'\",<>./?"),
                code="password_no_symbol",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol: " +
            "()[]{}|\\`~!@#$%^&*_-+=;:'\",<>./?"
        )
