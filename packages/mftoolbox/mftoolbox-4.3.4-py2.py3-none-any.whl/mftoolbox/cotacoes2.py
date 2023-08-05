import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
#sys.path.append('C:\\Users\\coliveira\\OneDrive\\Coding\\Python\\MFToolbox\\')
from mftoolbox import constants, funcs
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

def volatilidade(__ticker, **kwargs):
    """
        Busca no site da B3 a volatilidade histórica de um ativo

        :param __ticker: código do ativo
        :param __periodo = x, x em meses (1, 3, 6, 12). Padrão = 6 meses
        :return: tuple [ticker, nome de pregão, cotacao, horario, variação monetária, variação percentual
        """

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # interactive
    options = webdriver.ChromeOptions()
    chrome_preferences = {'profile.managed_default_content_settings.images': 2}
    options.add_argument("headless")
    # noinspection SpellCheckingInspection
    options.add_experimental_option("prefs", chrome_preferences)
    browser = webdriver.Chrome(options=options, service_args=['--silent'], desired_capabilities=caps)

    try:
        __periodo = [int(kwargs.get('periodo'))]
        if '|1|3|6|12|'.find('|'+str(__periodo[0])+'|') == -1:
            __periodo = [6]
    except:
        __periodo = [1,3,6,12]
    __result = []
    for __item in __periodo:
        if __item == 1:
            __periodo_txt = '1Mes'
        elif __item == 12:
            __periodo_txt = '1Ano'
        else:
            __periodo_txt = str(__item) + 'Meses'
        # noinspection SpellCheckingInspection
        url = 'http://bvmf.bmfbovespa.com.br/cias-listadas/volatilidade-ativos/ResumoVolatilidadeAtivos.aspx?' \
              'metodo=padrao&' \
              'periodo=' + __periodo_txt + '&' \
              'codigo=' + __ticker + '&' \
              'idioma=pt'
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")
        td_list = soup.find_all('td')
        try:
            __result.append([float(td_list[3].text.replace(",", ".")),float(td_list[4].text.replace(",", "."))])
        except:
            __result.append(['', ''])
    return __result



def ultima_cotacao(__ticker, **kwargs):
    """
    Busca no site Tradingview.com o nome de pregão de um ativo, a última cotação, seu horário,
    ganho monetário e percentual

    :param __ticker: código do ativo
    :param __delay = x, x em seundos
    :return: tuple [ticker, nome de pregão, cotacao, horario, variação monetária, variação percentual
    """
    try:
        __delay = int(kwargs.get('delay'))
    except:
        __delay = 0

    __url = 'https://www.tradingview.com/symbols/' + __ticker

    __caps = DesiredCapabilities().CHROME
    __caps["pageLoadStrategy"] = "eager"
    __options = webdriver.ChromeOptions()
    __chrome_preferences = {'profile.managed_default_content_settings.images': 2}
    __options.add_argument("headless")
    # noinspection SpellCheckingInspection
    __options.add_experimental_option("prefs", __chrome_preferences)
    __browser = webdriver.Chrome(options=__options, service_args=['--silent'], desired_capabilities=__caps)
    __browser.get(__url)
    time.sleep(__delay)
    __html = __browser.page_source
    __soup = BeautifulSoup(__html, "lxml")
    try:
        __nome_pregao = __soup.findAll("div", {"class": "tv-symbol-header__long-title-first-text"})[0].text
    except:
        __nome_pregao = ''
    try:
        __cotacao = float(__soup.findAll("div", {"class": "tv-symbol-price-quote__value js-symbol-last"})[0].text)
    except:
        __cotacao = 0
    try:
        __horario = __soup.findAll("span", {"class": "js-symbol-lp-time"})[0].text.replace(')','').replace('(','')
        __horario = datetime.strptime(__horario[:-6], '%b %d %H:%M')
    except:
        __horario = ''
    try:
        __variacao_monetaria = __soup.findAll("span",
                                          {"class": "js-symbol-change tv-symbol-price-quote__change-value"})[0].text
    except:
        __variacao_monetaria = 0
    try:
        __variacao_percentual = __soup.findAll("span",
                                       {"class": "js-symbol-change-pt tv-symbol-price-quote__change-value"})[0].text
    except:
        __variacao_percentual = 0

    return [__ticker, __nome_pregao, __cotacao, __horario, __variacao_monetaria, __variacao_percentual]


def ultimo_pregao(_ativo):
    """
    Busca no site IBOVX a data do último pregão para um ativo

    :param _ativo: código do ativo
    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """

    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _ativo + '&qtdpregoes=1'
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    try:
        if _tabela[20].text == 'Nº Negócios':
            posicao = 21
        else:
            posicao = 19
        return  (datetime.strptime(_tabela[posicao].text, '%d/%m/%Y'),_tabela[posicao].text)
    except:
        return (None, None)

def cotacao(_ativo, _data):
    """
    Busca no site IBOVX a cotação do ativo na data especificada. Retorna um tuple com data e cotação. Se não houver
    negociação naquela data, retorna a primeira cotação anterior disponível

    :param _ativo: código do ativo
    :param _data: data da cotação

    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """
    _data = datetime.strptime(_data, '%d/%m/%Y')
    _pregoes = str((datetime.now() - _data).days)
    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _ativo + '&qtdpregoes=' + _pregoes
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    i = len(_tabela)
    _cotacao_anterior = []
    if _tabela[20].text == 'Nº Negócios':
        incremento = 9
    else:
        incremento = 7

    try:
        while i >=0:
            _data_pagina = datetime.strptime(_tabela[i-incremento].text, '%d/%m/%Y')
            _cotacao = float(_tabela[i-incremento+3].text.replace('.','').replace(',','.'))
            if _data_pagina == _data:
                return (_data, _data.strftime('%d/%m/%Y'), _cotacao)
            elif _data_pagina > _data:
                return (_cotacao_anterior)
            _cotacao_anterior = (_data_pagina, _data_pagina.strftime('%d/%m/%Y'), _cotacao)
            i -= incremento
    except:
        return (_cotacao_anterior)


def cotacoes(_ativo, **kwargs):
    """
    Busca no site IBOVX a cotação do ativo na data especificada. Retorna um tuple com data e cotação. Se não houver
    negociação naquela data, retorna a primeira cotação anterior disponível

    :param _ativo: código do ativo
    :param data_inicio: data da primeira cotação, defautl = 01/01/2019
    :param pregoes: quantidade de pregoes retornados = 300

    :return: tuple com a data como datetime, data no formato DD/MM/AAAA e a cotação
    """
    _data = datetime.strptime(_data, '%d/%m/%Y')
    _pregoes = str((datetime.now() - _data).days)
    url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + _ativo + '&qtdpregoes=' + _pregoes
    r = requests.get(url, headers=constants.Header.header)
    soup = BeautifulSoup(r.text, 'lxml')
    _tabela = soup.find_all('td')
    i = len(_tabela)
    _cotacao_anterior = []
    if _tabela[20].text == 'Nº Negócios':
        incremento = 9
    else:
        incremento = 7

    try:
        while i >=0:
            _data_pagina = datetime.strptime(_tabela[i-incremento].text, '%d/%m/%Y')
            _cotacao = float(_tabela[i-incremento+3].text.replace('.','').replace(',','.'))
            if _data_pagina == _data:
                return (_data, _data.strftime('%d/%m/%Y'), _cotacao)
            elif _data_pagina > _data:
                return (_cotacao_anterior)
            _cotacao_anterior = (_data_pagina, _data_pagina.strftime('%d/%m/%Y'), _cotacao)
            i -= incremento
    except:
        return (_cotacao_anterior)


def cotacoes_historicas(ativo, **kwargs):
    '''
    Carrega as cotações históricas de um ativo

    Args:
        ativo: ticker do ativo
        **kwargs:
            pregoes: quantidade de pregões retornados
            data_inicio: data do pregão mais antigo a ser retornado. Se não houve pregão nesta data, retorna o primeiro
                        pregão após esta data

    Returns:
        caso não seja passado o ticker do ativo (independentemente dos outros parâmetros):
            mensagem: Ativo não pode ser ''.
        caso o argumento data_inicio não seja uma data válida (e não tenha acontecido as situação acima):
            mensagem: Data 'DD/MM/YYYY' é inválida.
        se forem passados ambos os argumentos, vale o número de pregões
        se não for passado nenhum argumento, serão retornados os dados do último pregão

        lista de tuples com os seguintes dados:
            ativo
            data da cotação
            variação de preço percentual
            variação de preço em valor
            cotação
            preço de abertura
            preço mínimo
            preço máximo
            volume financeiro (ordem de grandeza)
            número de negócios


    '''

    if ativo == '':
        return "Ativo não pode ser ''"
    __param = {}
    for __item in kwargs:
        __param[__item.upper()] = kwargs[__item]
    try:
        pregoes = __param['PREGOES']
        __modo_pregoes = True
    except KeyError:
        # data_inicio = datetime.strptime('01/01/2019', '%d/%m/%Y')
        pregoes = 0
        __modo_pregoes = False
    try:
        data_inicio = __param['DATA_INICIO']
        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
    except (KeyError, ValueError):
        if not __modo_pregoes and len(__param) > 0:
            return "Data '" + data_inicio + "' é inválida."
        else:
            data_inicio = ''
            __modo_pregao = True

    if pregoes == 0 and data_inicio == '':
        pregoes = 1
        __modo_pregoes = True
    elif pregoes == 0 and data_inicio != '':
        pregoes = (datetime.now() - data_inicio).days
        __modo_pregoes = False

    __url = 'https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=' + ativo + '&qtdpregoes=' + str(pregoes)
    __r = requests.get(__url, headers=constants.Header.header)
    __soup = BeautifulSoup(__r.text, 'lxml')
    if __soup.text.find('Papel não encontrado ou sem histórico.') >= 0:
        return "Ativo '" + ativo.upper() + "' não encontrado."
    __tabela = __soup.find_all('td')
    __i = len(__tabela)
    __cotacoes = []
    if __tabela[20].text == 'Nº Negócios':
        __incremento = 9
    else:
        __incremento = 7

    while __i >= 0:
        try:
            __data = datetime.strptime(__tabela[__i - __incremento + 0].text, '%d/%m/%Y')
        except ValueError:
            break
        __variacao_perc = funcs.num_ptb2us(__tabela[__i - __incremento + 1].text)
        __variacao_num = funcs.num_ptb2us(__tabela[__i - __incremento + 2].text)
        __cotacao = funcs.num_ptb2us(__tabela[__i - __incremento + 3].text)
        __abertura = funcs.num_ptb2us(__tabela[__i - __incremento + 4].text)
        __minimo = funcs.num_ptb2us(__tabela[__i - __incremento + 5].text)
        __maximo = funcs.num_ptb2us(__tabela[__i - __incremento + 6].text)
        __volumme = funcs.num_ptb2us(__tabela[__i - __incremento + 7].text)
        __negocios = funcs.num_ptb2us(__tabela[__i - __incremento + 8].text)
        if __tabela[__i - __incremento - 1].text.find('bannerresponsivoabaixomenu') > 0:
            __skip = 1
        else:
            __skip = 0
        __cotacoes.append((ativo, __data, __variacao_perc, __variacao_num, __cotacao, __abertura, __minimo, __maximo,
                           __volumme, __negocios))

        __i = __i - __incremento - __skip

    __cotacoes_final = []
    __cotacoes = sorted(__cotacoes, key=lambda x: x[1], reverse=True)
    # __cotacoes.sort(key=takeDate, reverse = True)
    if __modo_pregoes:
        __pregoes_carregados = len(__cotacoes)
        for __id, __linha in enumerate(__cotacoes):
            if __id < pregoes:
                __cotacoes_final.append(__linha)
    else:
        for __linha in __cotacoes:
            if __linha[1] >= data_inicio:
                __cotacoes_final.append(__linha)

    # return "Modo pregões = " + str(__modo_pregoes), "Quantidade de registros = " + str(len(__cotacoes_final)), "Parêmetro pregões = " + str(pregoes), "Última data dos registros = " + str(__cotacoes_final[len(__cotacoes_final)-1][1]), "Parâmetro data de início = " + str(data_inicio)
    return __cotacoes_final