
import re

from datetime import datetime

from django.conf import settings


def clean_code(text):
    return re.sub(r'[\W_]+', '', text).lower()


def get_date_from_request(request, key):
    return request.GET.get(
        key,
        datetime.now().date().strftime(settings.DATE_INPUT_FORMATS[0])
    )
