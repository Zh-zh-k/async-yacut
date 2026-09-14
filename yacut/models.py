import random
from datetime import datetime

from flask import url_for

from yacut import db
from yacut.constants import (DUPLICATED_SHORT_ID_MESSAGE, FORBIDDEN_SHORT_IDS,
                             ORIGINAL_LINK_MAX_LENGTH, SHORT_ID_CHARS,
                             SHORT_ID_GENERATION_ATTEMPTS, SHORT_ID_LENGTH)


class ShortIdAlreadyExistsError(Exception):
    pass


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(ORIGINAL_LINK_MAX_LENGTH),
        nullable=False
    )
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )

    @classmethod
    def get_by_short(cls, short_id):
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def get_unique_short_id(cls):
        for _ in range(SHORT_ID_GENERATION_ATTEMPTS):
            short_id = ''.join(
                random.choices(
                    SHORT_ID_CHARS,
                    k=SHORT_ID_LENGTH
                )
            )
            if not cls.get_by_short(short_id):
                return short_id

        raise RuntimeError(
            'Не удалось сгенерировать уникальную короткую ссылку.'
        )

    @classmethod
    def create(cls, original, custom_id=None):
        if custom_id:
            if (
                custom_id in FORBIDDEN_SHORT_IDS
                or cls.get_by_short(custom_id)
            ):
                raise ShortIdAlreadyExistsError(
                    DUPLICATED_SHORT_ID_MESSAGE
                )
            short_id = custom_id
        else:
            short_id = cls.get_unique_short_id()

        url_map = cls(
            original=original,
            short=short_id
        )

        db.session.add(url_map)
        db.session.commit()

        return url_map

    def get_short_link(self):
        return url_for(
            'redirect_view',
            short_id=self.short,
            _external=True
        )

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.get_short_link()
        }
