from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_shorter_than(text):
    if len(text) < 3:
        raise ValidationError(
            _("Email is too short!"),
            params={"text": text}
        )