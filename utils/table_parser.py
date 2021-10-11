import logging

from data.config import EDU_LOGIN, EDU_PASSWORD
import lxml.html


def get_table_html(session):
    """
    :param session:
    :return: None or html with diary
    получаем исходник с табелем
    """

    url = 'https://edu.tatar.ru/logon'
    data = {
        'main_login': EDU_LOGIN,
        'main_password': EDU_PASSWORD
    }
    proxy = {
    'https': 'http://squid2.kpfu.ru:8080',
    'http': 'http://squid2.kpfu.ru:8080',
    }
    session.proxies = proxy
    try:
        session.post(url=url, data=data, headers=dict(Referer=url))
        print(session.get(url='https://httpbin.org/ip').text)
        r = session.get(url='https://edu.tatar.ru/user/diary/term?term=1')
    except Exception:
        logging.exception('Не смог спарсить таблицу')
        return None
    return r.text


def is_mean_mark(mark):
    return '.' in mark and mark.replace('.', '0').isdigit()


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
        return result
    return wrapper


@get_dict
def table_prepare_statistic(data):
    """
    :param data:
    :return:
    """
    markup = lxml.html.document_fromstring(data)
    xpath = '//tbody/tr/td[text()]'
    matches = markup.xpath(xpath)
    # берем до -3, потому что там итог, возможно здесь будет баг
    dairy_data = [x.text for x in matches if '\n' not in x.text][:-3]
    return dairy_data


def pretty_table(table: dict):
    result = ""
    for elem in table:
        if table[elem]:
            table[elem][-1] = f'<b>{table[elem][-1]}</b>'
            result += f'<u>{elem}</u>' + ':    ' + '  '.join(table[elem][-4:]) + '\n'
        else:
            result += f'<u>{elem}</u>' + ':\n'
    return result


def get_table(session):
    dairy = get_table_html(session)
    if dairy:
        return pretty_table(table_prepare_statistic(dairy))
    return 'Ошибочка вышла :('
