from pathlib import Path
from urllib.parse import urljoin


DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PATTERN_LATEST_VERSIONS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS_DIR = 'results'
DOWNLOAD_DIR = 'downloads'
PRETTY_REGIME = 'pretty'
FILE_REGIME = 'file'

ARGUMENT_PARSER_MESSAGE = 'Аргументы командной строки: {args}'
CONNECTION_ERROR_MESSAGE = 'Возникла ошибка при загрузке страницы {url}'
DOWNLOAD_SAVE_MESSAGE = 'Архив был загружен и сохранён: {archive_path}'
ERROR_MESSAGE = 'Ошибка в работе программы: {error}'
FILE_OUTPUT_MESSAGE = 'Файл с результатами был сохранён: {file_path}'
FINISH_PARSER_MESSAGE = 'Парсер завершил работу.'
LATEST_VERSIONS_TABLE = ('Ссылка на документацию', 'Версия', 'Статус')
NOT_FOUD_TAG = 'Не найден тег ul с необходимыми параметрами'
RETURN_PEP = ('Статус', 'Количество')
START_PARSER_MESSAGE = 'Парсер запущен!'
TAG_ERROR_MESSAGE = 'Не найден тег {tag} {attrs}'
UNEXPECTED_STATUS_MESSAGE = (
    'Несовпадающие статусы у PEP: '
    '"{url_pep}".'
    'Статус в карточке: {status} '
    'ожидаемые статусы: {pep_statuslist}.'
)
UNKNOWN_KEY_STATUS_MESSAGE = (
    '"{url_pep}". '
    'Неизвестный ключ статуса: \'{pep_statuslist}\''
)
WHATS_NEW = ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
