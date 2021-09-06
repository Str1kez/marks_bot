import requests
import datetime as dt
import lxml.html
from data.config import EDU_LOGIN, EDU_PASSWORD


def convert_to_utc(date: dt.date):
    """
    :param date:
    :return: None or date_utc
    Перемещение в дневнике по страницам, указываем число
    Проверка на воскр, на переполнение выкинет ошибку, а воскр вернет False
    """
    try:
        date_utc = dt.datetime(date.year, date.month, date.year)
        date_utc = dt.datetime.timestamp(date_utc)
    except ValueError:
        return None
    return None if not (1630789200 - int(date_utc)) % 604800 else int(date_utc)


def get_dairy_html(date: dt.date):
    """
    :param date:
    :return: None or html with diary
    получаем исходник с дневником, а парамы можно получить из даты
    """
    s = requests.Session()
    url = 'https://edu.tatar.ru/logon'
    data = {
        'main_login': EDU_LOGIN,
        'main_password': EDU_PASSWORD
    }
    s.post(url=url, data=data, headers=dict(Referer=url))
    utc_date = convert_to_utc(date)
    if not utc_date:
        return None
    r = s.get(url='https://edu.tatar.ru/user/diary/week',
              params={'date': utc_date})
    return r.text


def get_dict(func):
    def wrapper(data, day: str):
        answer = func(data, day)
        result = dict(day=answer.pop(0))
        last_data = None
        for elem in answer:
            if not all((x.isdigit() for x in elem.split('/'))):
                result[elem] = None
                last_data = elem
            else:
                result[last_data] = elem
        return result
    return wrapper


@get_dict
def day_prepare_statistic(data, day: str):
    """
    :param data: string with html
    :param day: number of required day
    :return: list with day on first position and subj, mark in queue
    TODO: Сделать словарик со статистикой дня
    """
    markup = lxml.html.document_fromstring(data)
    xpath = '//td[@class="tt-days"]/div/span | //td[@class="tt-subj"]/div/span \
         | //td[@class="tt-mark"]/div/span \
         | //tr[@class="tt-separator"]/*'
    matches = markup.xpath(xpath)
    dairy_data = [x.text for x in matches]
    day_start = dairy_data.index(day)
    day_end = dairy_data.index(None, day_start)
    day_data = dairy_data[day_start:day_end]
    return day_data


def get_marks(day: dt.date):
    with open('utils/dairy.html', 'r', encoding='utf-8') as f:
        dairy = f.read()
    # dairy = get_dairy_html(day)
    if dairy:
        prepared_stat = day_prepare_statistic(dairy, str(day.day))
    else:
        return None
    return prepared_stat
