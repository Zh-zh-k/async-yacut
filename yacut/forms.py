from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from yacut.constants import (ORIGINAL_LINK_MAX_LENGTH, SHORT_ID_MAX_LENGTH,
                             SHORT_ID_PATTERN)


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(),
            Length(max=ORIGINAL_LINK_MAX_LENGTH),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(max=SHORT_ID_MAX_LENGTH)]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and not SHORT_ID_PATTERN.fullmatch(field.data):
            raise ValidationError(
                'Короткая ссылка может содержать только '
                'латинские буквы и цифры.'
            )


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[
            FileRequired()
        ]
    )
    submit = SubmitField('Загрузить')
