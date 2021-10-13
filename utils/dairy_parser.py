import datetime as dt
import lxml.html
from data.config import EDU_LOGIN, EDU_PASSWORD
import logging


def convert_to_utc(date: dt.date):
    """
    :param date:
    :return: None or date_utc
    Перемещение в дневнике по страницам, указываем число
    Проверка на воскр, на переполнение выкинет ошибку, а воскр вернет строку
    """
    try:
        date_utc = dt.datetime(date.year, date.month, date.day)
        date_utc = dt.datetime.timestamp(date_utc)
        print(date_utc)
    except ValueError:
        logging.exception('Такого дня не существует в этом месяце')
        return None
    return "Воскресенье" if not (1630789200 - int(date_utc)) % 604800 else int(date_utc)


def get_dairy_html(date: dt.date, session):
    """
    :param date:
    :param session:
    :return: None or html with diary
    получаем исходник с дневником, а парамы можно получить из даты
    """

    url = 'https://edu.tatar.ru/logon'
    data = {
        'main_login': EDU_LOGIN,
        'main_password': EDU_PASSWORD
    }
    headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 Safari/537.36'
    }
    session.post(url=url, data=data, headers=headers)
    utc_date = convert_to_utc(date)
    if not utc_date or utc_date == 'Воскресенье':
        return utc_date
    r = session.get(url='https://edu.tatar.ru/user/diary/week',
                    params={'date': 1634072400})
    return r.text


def get_dict(func):
    def wrapper(data, day: str):
        answer = func(data, day)
        if not answer:
            return None
        result = dict(day=answer.pop(0))
        last_data = None
        for elem in answer:
            if not all((x.isdigit() or x == 'н' for x in elem.split('/'))):
                result[elem] = None
                last_data = elem
            else:
                result[last_data] = elem
        return result
    return wrapper


def get_label(dairy_data, day, day_start):
    result = None
    try:
        result = dairy_data.index(str(int(day) + 1), day_start)
    except ValueError:
        try:
            result = dairy_data.index('1', day_start)
        except ValueError:
            pass
    return result


@get_dict
def day_prepare_statistic(data, day: str):
    """
    :param data: string with html
    :param day: number of required day
    :return: list with day on first position and subj, mark in queue
    """
    markup = lxml.html.document_fromstring(data)
    xpath = '//td[@class="tt-days"]/div/span | //td[@class="tt-subj"]/div \
         | //td[@class="tt-mark"]/div \
         | //tr[@class="tt-separator"]/*'
    matches = markup.xpath(xpath)
    dairy_data = [x.text for x in matches if x.text is not None]
    print(dairy_data)
    try:
        day_start = dairy_data.index(day)
    except ValueError:
        logging.exception('Нет запрашиваемого дня в данных')
        return None
    label = get_label(dairy_data, day, day_start)
    day_data = dairy_data[day_start:label]
    return day_data


def get_marks(day: dt.date, session):
    if day.weekday() == 6:
        return 'Воскресенье'
    dairy = get_dairy_html(day, session)
    prepared_stat = day_prepare_statistic(
        dairy, str(day.day)) if dairy else None
    return prepared_stat


def pretty_diary(data):
    if not data or data == 'Воскресенье':
        return data
    result = ""
    for subj in data:
        if subj == 'day':
            continue
        if data[subj]:
            result += f'<u>{subj}</u>' + ': ' + data[subj] + '\n'
        else:
            result += f'<u>{subj}</u>' + ':\n'
    return result
