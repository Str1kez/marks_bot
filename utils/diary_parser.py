import asyncio
import datetime as dt
import functools
from concurrent import futures
import lxml.html

from data.config import EDU_LOGIN, EDU_PASSWORD
from utils.misc.logging import exc_log


def convert_to_utc(date: dt.date):
    """
    :param date:
    :return: None or date_utc
    Перемещение в дневнике по страницам, указываем число
    Проверка на воскр, на переполнение выкинет ошибку, а воскр вернет строку
    """
    try:
        date_utc = dt.datetime(date.year, date.month, date.day)
        date_utc = dt.datetime.timestamp(date_utc) - 10800
    except ValueError:
        exc_log.error('Такого дня не существует в этом месяце')
        return None
    return "Воскресенье" if not (1630789200 - int(date_utc)) % 604800 else int(date_utc)


def get_diary_html(date: dt.date, session):
    """
    :param date:
    :param session:
    :return: None or html with diary
    получаем исходник с дневником, а парамы можно получить из даты
    """

    url = 'https://edu.tatar.ru/logon'
    data = {
        'main_login2': EDU_LOGIN,
        'main_password2': EDU_PASSWORD
    }
    headers = {
        'Referer': url,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        session.post(url=url, data=data, headers=headers)
        utc_date = convert_to_utc(date)
        if not utc_date or utc_date == 'Воскресенье':
            return utc_date
        r = session.get(url='https://edu.tatar.ru/user/diary/week',
                        params={'date': utc_date})
        return r.text
    except Exception:
        exc_log.error('Не смог спарсить дневник')


def get_dict(func):
    def wrapper(data, day: str):
        answer = func(data, day)
        if not answer:
            return None
        result = dict(day=answer.pop(0))
        last_data = None
        for elem in answer:
            if not all((x.isdigit() or x == 'н' for x in elem.split('/'))):
                result.setdefault(elem)
                last_data = elem
            else:
                if result.get(last_data):
                    result[last_data] += ' ' + elem
                else:
                    result[last_data] = elem
        return result
    return wrapper


def get_label(diary_data, day, day_start):
    result = None
    try:
        result = diary_data.index(str(int(day) + 1), day_start)
    except ValueError:
        try:
            result = diary_data.index('1', day_start)
        except ValueError:
            exc_log.error("Что-то не так с датой")
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
    diary_data = [x.text for x in matches if x.text is not None]
    try:
        day_start = diary_data.index(day)
    except ValueError:
        exc_log.error('Нет запрашиваемого дня в данных')
        return None
    label = get_label(diary_data, day, day_start)
    day_data = diary_data[day_start:label]
    return day_data


async def get_marks(day: dt.date, session):
    """
    :param day:
    :param session:
    :return:
    Делаем request асинхронным, так как через aiohttp не работает прокси для сайта
    """
    if day.weekday() == 6:
        return 'Воскресенье'
    loop = asyncio.get_running_loop()
    with futures.ThreadPoolExecutor() as pool:
        diary = await loop.run_in_executor(pool, functools.partial(get_diary_html, day, session))
    prepared_stat = day_prepare_statistic(
        diary, str(day.day)) if diary else None
    return prepared_stat


def prettify(s: str) -> str:
    res = ""
    marks = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
    for m in s:
        if m.isdigit():
            res += marks[int(m) - 1]
        else:
            res += m
    return res


def pretty_diary(data):
    if not data or data == 'Воскресенье':
        return data
    result = ""
    for subj in data:
        if subj == 'day':
            continue
        if data[subj]:
            data[subj] = prettify(data[subj])
            result += f'<u>{subj}</u>' + '\t\t\t\t' + data[subj] + '\n'
        else:
            result += f'<u>{subj}</u>\n'
    return result
