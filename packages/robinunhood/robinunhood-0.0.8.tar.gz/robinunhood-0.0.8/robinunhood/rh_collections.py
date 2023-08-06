import pandas as pd
import requests
import json
import re

def get_top_movers():
    """
    :return: pandas dataframe of top 20 stocks that are the top movers
    """

    url = 'https://api.robinhood.com/midlands/tags/tag/top-movers/'
    x = requests.get(url)
    y = json.loads(x.text)
    z = y['instruments']

    df = pd.DataFrame()
    for i in range(len(z)):
        d = requests.get(z[i])
        f = json.loads(d.text)
        df_tmp = pd.DataFrame.from_dict(f, orient='index').T
        df = df.append(df_tmp)

    return df


def get_most_popular():
    """
    :return: pandas dataframe of 100 most-popular
    """
    [df] = pd.read_html('https://robinhood.com/collections/100-most-popular')
    return df


def get_collection(collection):
    """
    :param collection: "100-most-popular", "upcoming-earnings", "new-on-robinhood", "technology", "oil-and-gas",
    "finance", "software-service", "energy", "manufacturing", "consumer-products", "etf", "video-games", "social-media",
    "health", "entertainment"
    :return: pandas dataframe of collection stocks
    """
    url = f'https://robinhood.com/collections/{collection}'
    [df] = pd.read_html(url)
    return df


def get_tipranks_sentiment(collection):
    """
        :param collection: "100-most-popular", "upcoming-earnings", "new-on-robinhood", "technology", "oil-and-gas",
        "finance", "software-service", "energy", "manufacturing", "consumer-products", "etf", "video-games", "social-media",
        "health", "entertainment"
        :return: pandas dataframe of collection stocks
        """
    url = f'https://robinhood.com/collections/{collection}'
    [df] = pd.read_html(url)

    symbols = list(df.Symbol.values)
    for i, s in enumerate(symbols):
        # print("Processing {}".format(s))
        url = "https://www.tipranks.com/api/stocks/getNewsSentiments/?ticker={}".format(s)
        s2 = pd.read_json(url, orient="index", typ="series")
        df2 = pd.DataFrame(s2).T
        # print("Processing {}: cols={}".format(s, df2.columns))
        if df2.shape[1] > 0:
            if len(df2.buzz) > 0:
                df.loc[i, 'buzz'] = df2.buzz.iloc[0]['buzz']
            if (df2.sentiment.any()):
                df.loc[i, 'bullish_pct'] = df2.sentiment.iloc[0]['bullishPercent']
            df.loc[i, 'sector_avg_bullish_pct'] = df2.sectorAverageBullishPercent.iloc[0]
            df.loc[i, 'score'] = df2.score.iloc[0]
            df.loc[i, 'sector_avg_news_score'] = df2.sectorAverageNewsScore.iloc[0]
        return df


if __name__ == "__main__":

    #df = get_top_movers()
    #print(df.symbol.values)

    #df = get_most_popular()
    #print(df.Symbol.values)

    #df = get_collection('etf')
    #print(df.Symbol.values)

    symbols = get_tipranks_sentiment('100-most-popular')
    print(symbols)