import random
import string

from yacut.models import URLMap

SHORT_ID_LENGTH = 6
SHORT_ID_CHARS = string.ascii_letters + string.digits


def get_unique_short_id():
    while True:
        short_id = ''.join(
            random.choices(SHORT_ID_CHARS, k=SHORT_ID_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
