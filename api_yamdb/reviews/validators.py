from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(year):
    if year > timezone.now().year:
        raise ValidationError(
            'Год превышает текущий',
            code='invalid',
            params={'year': year},
        )
