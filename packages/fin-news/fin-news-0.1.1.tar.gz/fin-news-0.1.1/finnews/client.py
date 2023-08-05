import json

from typing import List
from typing import Dict
from typing import Union

from finnews.cnbc import CNBC
from finnews.nasdaq import NASDAQ
from finnews.market_watch import MarketWatch
from finnews.sp_global import SPGlobal
from finnews.seeking_alpha import SeekingAlpha
from finnews.cnn_finance import CNNFinance
from finnews.wsj import WallStreetJournal
from finnews.yahoo_finance import YahooFinance


class News():

    """
    Represents the main News Client that is used to access 
    the different news providers.
    """

    def __init__(self) -> None:
        """Initalizes the main `News` client.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()
        """

        self._cnbc_client = None
        self._nasdaq_client = None
        self._market_watch_client = None
        self._sp_global_client = None
        self._seeking_alpha_client = None
        self._cnn_finance_client = None
        self._wsj_client = None
        self._yahoo_finance_client = None

    def __repr__(self) -> str:
        """Represents the string representation of the client object.

        Returns:
        ----
        (str): The string representation.
        """
        return "<NewsClient Connected: True'>"

    @property
    def cnbc(self) -> CNBC:
        """Returns a new instance of the `CNBC` news client.

        Returns:
        ----
        CNBC: The `CNBC` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the CNBC News Client.
            >>> cnbc_news_client = news_client.cnbc        
        """

        self._cnbc_client = CNBC()

        return self._cnbc_client

    @property
    def nasdaq(self) -> NASDAQ:
        """Returns a new instance of the `NASDAQ` news client.

        Returns:
        ----
        NASDAQ: The `NASDAQ` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the NASDAQ News Client.
            >>> nasdaq_news_client = news_client.nasdaq       
        """

        self._nasdaq_client = NASDAQ()

        return self._nasdaq_client

    @property
    def market_Watch(self) -> MarketWatch:
        """Returns a new instance of the `MarketWatch` news client.

        Returns:
        ----
        MarketWatch: The `MarketWatch` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the MarketWatch News Client.
            >>> market_Watch_client = news_client.market_Watch       
        """

        self._market_watch_client = MarketWatch()

        return self._market_watch_client

    @property
    def sp_global(self) -> SPGlobal:
        """Returns a new instance of the `SPGlobal` news client.

        Returns:
        ----
        SPGlobal: The `SPGlobal` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the SPGlobal News Client.
            >>> sp_global_client = news_client.sp_global       
        """

        self._sp_global_client = SPGlobal()

        return self._sp_global_client

    @property
    def seeking_alpha(self) -> SeekingAlpha:
        """Returns a new instance of the `SeekingAlpha` news client.

        Returns:
        ----
        SeekingAlpha: The `SeekingAlpha` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the SeekingAlpha News Client.
            >>> seeking_alpha_client = news_client.seeking_alpha       
        """

        self._seeking_alpha_client = SeekingAlpha()

        return self._seeking_alpha_client

    @property
    def cnn_finance(self) -> CNNFinance:
        """Returns a new instance of the `CNNFinance` news client.

        Returns:
        ----
        CNNFinance: The `CNNFinance` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the CNN Finance News Client.
            >>> cnn_finance_client = news_client.cnn_finance       
        """

        self._cnn_finance_client = CNNFinance()

        return self._cnn_finance_client

    @property
    def wsj(self) -> WallStreetJournal:
        """Returns a new instance of the `WallStreetJournal` news client.

        Returns:
        ----
        WallStreetJournal: The `WallStreetJournal` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the Wall Street Journal News Client.
            >>> wsj_client = news_client.wsj       
        """

        self._wsj_client = WallStreetJournal()

        return self._wsj_client

    @property
    def yahoo_finance(self) -> YahooFinance:
        """Returns a new instance of the `YahooFinance` news client.

        Returns:
        ----
        YahooFinance: The `YahooFinance` news client that can be used to
            query different RSS feeds by topics.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the Yahoo Finance News Client.
            >>> yahoo_finance_client = news_client.yahoo_finance       
        """

        self._yahoo_finance_client = YahooFinance()

        return self._yahoo_finance_client

    def save_to_file(self, content: List[Dict], file_name: str) -> None:
        """Saves the news content to a JSONC file.

        Arguments:
        ----
        content (List[Dict]): A news collection list.

        file_name (str): The name of the file, with no file extension
            included.

        Usage:
        ----
            >>> from finnews.client import News

            >>> # Create a new instance of the News Client.
            >>> news_client = News()

            >>> # Grab the CNBC News Client.
            >>> cnbc_news_client = news_client.cnbc

            >>> # Grab the top news.
            >>> cbnc_top_news = cnbc_news_client.news_feed(topic='top_news')   

            >>> # Save the data.
            >>> news_client.save_to_file(
                content=cbnc_top_news,
                file_name='cnbc_top_news'
            )
        """

        # Define the file name.
        file_name = 'samples/responses/{name}.jsonc'.format(name=file_name)

        # Dump the content.
        with open(file=file_name, mode='w+') as news_data:
            json.dump(obj=content, fp=news_data, indent=2)
