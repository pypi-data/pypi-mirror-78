import requests
import json
import pandas as pd

def get_tipranks_stocks(score):
    """
    get stocks based on tipranks score
    :param score: from 1 to 5 (probably maps to 1-10 on the tipranks website)
    :return: list of 20 stocks from tipranks with requested score
    """

    url = f'https://www.tipranks.com/api/Screener/GetStocks/?tipranksScore={score}'
    x = requests.get(url)
    y = json.loads(x.text)

    symbols = []
    for i in range(20):
        symbols.append(y['data'][i]['ticker'])

    return symbols


def get_news_sentiments(symbol):
    """
    get news sentiments from tipranks
    :param symbol: stock symbol
    :return: unflattened dataframe with sentiments for stock symbol
    """

    url = f"https://www.tipranks.com/api/stocks/getNewsSentiments/?ticker={symbol}"
    df = pd.read_json(url, orient="index", typ="series")
    return pd.DataFrame(df).T


def get_data(symbol):
    """
    get news sentiments from tipranks
    :param symbol: stock symbol
    :return: unflattened dataframe with sentiments for stock symbol
    """

    url = f"https://www.tipranks.com/api/stocks/getData/?name={symbol}"
    df = pd.read_json(url, orient="index", typ="series")
    return pd.DataFrame(df).T


def get_trending_stocks(days):
    """

    :param days:
    :return:
    """

    url = f"https://www.tipranks.com/api/stocks/gettrendingstocks/?daysago={days}&which=most"
    return pd.read_json(url)


if __name__ == "__main__":

    symbols = get_tipranks_stocks(5)
    print(symbols)

    df = get_news_sentiments('NKE')
    print(df.head())

    df = get_data('NKE')
    print(df.head())

    df = get_trending_stocks(3)
    print(df.head())