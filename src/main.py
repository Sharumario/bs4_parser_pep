from collections import defaultdict
import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from constants import (
    ARGUMENT_PARSER_MESSAGE, BASE_DIR, DOWNLOAD_DIR, DOWNLOAD_SAVE_MESSAGE,
    DOWNLOADS_URL, ERROR_MESSAGE, EXPECTED_STATUS, FINISH_PARSER_MESSAGE,
    LATEST_VERSIONS_TABLE, MAIN_DOC_URL, MAIN_PEP_URL, NOT_FOUD_TAG,
    PATTERN_LATEST_VERSIONS, RETURN_PEP, START_PARSER_MESSAGE,
    UNEXPECTED_STATUS_MESSAGE, UNKNOWN_KEY_STATUS_MESSAGE, WHATS_NEW,
    WHATS_NEW_URL
)
from configs import configure_argument_parser, configure_logging
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    result = [WHATS_NEW]
    logs = []
    for section in tqdm(
        get_soup(session, WHATS_NEW_URL).select(
            '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
            )):
        version_link = urljoin(WHATS_NEW_URL, section.find('a')['href'])
        try:
            soup = get_soup(session, version_link)
            result.append(
                [
                    version_link,
                    find_tag(soup, 'h1').text,
                    find_tag(soup, 'dl').text.replace('\n', ' ')
                ]
            )
        except (ConnectionError, ParserFindTagException) as error:
            logs.append(ERROR_MESSAGE.format(error=error))
    for log in logs:
        logging.info(log)
    return result


def latest_versions(session):
    ul_tags = get_soup(session, MAIN_DOC_URL).select(
        'div.sphinxsidebarwrapper ul'
    )
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException(NOT_FOUD_TAG)
    results = [LATEST_VERSIONS_TABLE]
    for a_tag in a_tags:
        text_match = re.search(
            PATTERN_LATEST_VERSIONS, a_tag.text
        )
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status))
    return results


def download(session):
    archive_url = urljoin(
        DOWNLOADS_URL,
        get_soup(session, DOWNLOADS_URL).select_one(
            'table.docutils td > a[href$="pdf-a4.zip"]'
        )['href']
    )
    filename = archive_url.split('/')[-1]
    download_dir = BASE_DIR / DOWNLOAD_DIR
    download_dir.mkdir(exist_ok=True)
    archive_path = download_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_SAVE_MESSAGE.format(archive_path=archive_path))


def pep(session):
    count_status = defaultdict(int)
    logs = []
    for tr in tqdm(
        get_soup(session, MAIN_PEP_URL).select('#numerical-index tbody tr')
    ):
        url_pep = urljoin(MAIN_PEP_URL, find_tag(tr, 'a')['href'])
        pep_statuslist = EXPECTED_STATUS.get(tr.td.text[1:])
        if not pep_statuslist:
            pep_statuslist = tr.td.text[1:]
            logs.append(UNKNOWN_KEY_STATUS_MESSAGE.format(
                url_pep=url_pep, pep_statuslist=pep_statuslist
            ))
        try:
            status = (get_soup(session, url_pep).
                      find(string='Status').find_next('dd').text)
            if status not in pep_statuslist:
                logs.append(UNEXPECTED_STATUS_MESSAGE.format(
                        url_pep=url_pep,
                        status=status,
                        pep_statuslist=pep_statuslist
                ))
            count_status[status] += 1
        except ConnectionError as error:
            logs.append(ERROR_MESSAGE.format(error=error))
    for log in logs:
        logging.info(log)
    return [RETURN_PEP, *count_status.items(),
            ('Total', sum(count_status.values()))]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(START_PARSER_MESSAGE)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(ARGUMENT_PARSER_MESSAGE.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.error(ERROR_MESSAGE.format(error=error))
    logging.info(FINISH_PARSER_MESSAGE)


if __name__ == '__main__':
    main()
