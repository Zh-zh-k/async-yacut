from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import (EMPTY_REQUEST_MESSAGE, ID_NOT_FOUND_MESSAGE,
                             INVALID_SHORT_ID_MESSAGE, MISSING_URL_MESSAGE,
                             SHORT_ID_MAX_LENGTH, SHORT_ID_PATTERN)
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import ShortIdAlreadyExistsError, URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage(
            EMPTY_REQUEST_MESSAGE,
            HTTPStatus.BAD_REQUEST
        )

    if 'url' not in data:
        raise InvalidAPIUsage(
            MISSING_URL_MESSAGE,
            HTTPStatus.BAD_REQUEST
        )

    custom_id = data.get('custom_id')

    if custom_id and (
        len(custom_id) > SHORT_ID_MAX_LENGTH
        or not SHORT_ID_PATTERN.fullmatch(custom_id)
    ):
        raise InvalidAPIUsage(
            INVALID_SHORT_ID_MESSAGE,
            HTTPStatus.BAD_REQUEST
        )

    try:
        url_map = URLMap.create(
            original=data['url'],
            custom_id=custom_id
        )
    except ShortIdAlreadyExistsError as error:
        raise InvalidAPIUsage(
            str(error),
            HTTPStatus.BAD_REQUEST
        )

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.get_by_short(short_id)

    if url_map is None:
        raise InvalidAPIUsage(
            ID_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND
        )

    return jsonify({
        'url': url_map.original
    }), HTTPStatus.OK
