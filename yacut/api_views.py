import re
from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id

SHORT_ID_PATTERN = re.compile(r'^[A-Za-z0-9]+$')

DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)

INVALID_SHORT_ID_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST
        )

    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!',
            HTTPStatus.BAD_REQUEST
        )

    custom_id = data.get('custom_id')

    if custom_id:
        if (
            len(custom_id) > 16
            or not SHORT_ID_PATTERN.fullmatch(custom_id)
        ):
            raise InvalidAPIUsage(
                INVALID_SHORT_ID_MESSAGE,
                HTTPStatus.BAD_REQUEST
            )

        if (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first()
        ):
            raise InvalidAPIUsage(
                DUPLICATED_SHORT_ID_MESSAGE,
                HTTPStatus.BAD_REQUEST
            )

        short_id = custom_id

    else:
        short_id = get_unique_short_id()

    url_map = URLMap(
        original=data['url'],
        short=short_id
    )

    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': f'http://localhost/{url_map.short}'
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND
        )

    return jsonify({
        'url': url_map.original
    }), HTTPStatus.OK
