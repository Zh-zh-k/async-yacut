import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

SHORT_ID_PATTERN = re.compile(r'^[A-Za-z0-9]+$')


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(max=16)]
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
