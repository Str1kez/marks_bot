import asyncio
import functools
from concurrent import futures

import lxml.html

from app.data.config import EDU_LOGIN, EDU_PASSWORD
from app.utils.misc.logging import exc_log


SAVE_DIARY = None


def get_table_html(session):
    """
    :param session:
    :return: None or html with diary
    получаем исходник с табелем
    """

    url = "https://edu.tatar.ru/logon"
    data = {"main_login2": EDU_LOGIN, "main_password2": EDU_PASSWORD}
    headers = {"Referer": url, "Content-Type": "application/x-www-form-urlencoded"}
    try:
        session.post(url=url, data=data, headers=headers)
        r = session.get(url="https://edu.tatar.ru/user/diary/term?term=1")
    except Exception:
        exc_log.error("Не смог спарсить таблицу")
        return None
    return r.text


def is_mean_mark(mark):
    return "." in mark and mark.replace(".", "0").isdigit()


def get_dict(func):
    def wrapper(data):
        table = func(data)
        result = dict()
        last_subj = None
        for elem in table:
            if not is_mean_mark(elem) and not elem.isdigit():
                result[elem] = None
                last_subj = elem
            elif not result[last_subj]:
                result[last_subj] = [elem]
            else:
                result[last_subj].append(elem)
        global SAVE_DIARY
        SAVE_DIARY = result
        return result

    return wrapper


@get_dict
def table_prepare_statistic(data):
    """
    :param data:
    :return:
    """
    markup = lxml.html.document_fromstring(data)
    xpath = "//tbody/tr/td[text()]"
    matches = markup.xpath(xpath)
    # берем до -3, потому что там итог, возможно здесь будет баг
    diary_data = [x.text for x in matches if "\n" not in x.text][:-3]
    return diary_data


def pretty_table(table: dict):
    result = ""
    for elem in table:
        if table[elem]:
            table[elem][-1] = f"<b>{table[elem][-1]}</b>"
            for x in range(len(table[elem])):
                if table[elem][x] == "2":
                    table[elem][x] = "2️⃣"
            result += f"<u>{elem}</u>" + "\t\t\t\t" + "  ".join(table[elem][-4:]) + "\n"
        else:
            result += f"<u>{elem}</u>\n"
    return result


async def get_table(session):
    """
    :param session:
    :return:
    Делаем request асинхронным, так как через aiohttp не работает прокси для сайта
    """
    loop = asyncio.get_running_loop()
    with futures.ThreadPoolExecutor() as pool:
        diary = await loop.run_in_executor(pool, functools.partial(get_table_html, session))
    if diary:
        return pretty_table(table_prepare_statistic(diary))
    return "Ошибочка вышла :("


def get_subjects():
    return list(SAVE_DIARY)


def get_subject(subj: str):
    if subj not in SAVE_DIARY:
        exc_log.error("Ошибка в поиске предмета для представления в подробном виде")
        return
    if not SAVE_DIARY[subj]:
        return f"<u>{subj}</u>\t\t\t\tНет оценок"
    SAVE_DIARY[subj][-1] = f"<b>{SAVE_DIARY[subj][-1]}</b>"
    for x in range(len(SAVE_DIARY[subj])):
        if SAVE_DIARY[subj][x] == "2":
            SAVE_DIARY[subj][x] = "2️⃣"
    return f"<u>{subj}</u>\t\t\t\t" + "  ".join(SAVE_DIARY[subj]) + "\n"
