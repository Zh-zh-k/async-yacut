import re
import string

SHORT_ID_LENGTH = 6
SHORT_ID_MAX_LENGTH = 16
SHORT_ID_CHARS = string.ascii_letters + string.digits
SHORT_ID_PATTERN = re.compile(r'^[A-Za-z0-9]+$')
SHORT_ID_GENERATION_ATTEMPTS = 100

ORIGINAL_LINK_MAX_LENGTH = 2048

FORBIDDEN_SHORT_IDS = {
    'files',
}

DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
MISSING_URL_MESSAGE = '"url" является обязательным полем!'
ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = (
    f'{API_HOST}{API_VERSION}/disk/resources/upload'
)
DOWNLOAD_LINK_URL = (
    f'{API_HOST}{API_VERSION}/disk/resources/download'
)
