import requests
import time

API_ENDPOINT = 'https://finnhub.io/api/v1/stock/'
API_QUOTE_ENDPOINT = 'https://finnhub.io/api/v1/quote'
API_TECHNICAL_ENDPOINT = 'https://finnhub.io/api/v1/scan/'
API_NEWS_ENDPOINT = 'https://finnhub.io/api/v1/news/'
API_DEVELOPMENTS_ENDPOINT = 'https://finnhub.io/api/v1/major-development'
API_SENTIMENT_ENDPOINT = 'https://finnhub.io/api/v1/news-sentiment'

class FinnHub(): 
    def __init__(self, symbol, token): 
        self._stock_data = {
            'profile': {},
            'ceo_compensation': {},
            'recommendation_trends': {},
            'levels': {},
            'quote': {},
            'indicators': {},
            'news': {},
            'developments': {},
            'news_sentiment': {}
        }
        self.symbol = symbol
        self.token = token
        self._get_information()

    def _check_request(self, r):
        if r.status_code == 429:
            print('Waiting for 1 Minute')
            time.sleep(60)
            return True
        else:
            return False
    def _send_request(self, endpoint):
        url_string = API_ENDPOINT + endpoint + '?symbol={0}&token={1}'.format(self.symbol, self.token)
        r = requests.get(url_string)
        if self._check_request(r):
            r = requests.get(url_string)
            return r.json()
        return r.json()

    def _send_technical_request(self, endpoint):
        url_string = API_TECHNICAL_ENDPOINT + endpoint + '?symbol={0}&resolution=D&token={1}'.format(self.symbol, self.token)
        r = requests.get(url_string)
        if self._check_request(r):
            r = requests.get(url_string)
            return r.json()
        return r.json()

    def _send_quote_request(self):
        url_string = API_QUOTE_ENDPOINT + '?symbol={0}&token={1}'.format(self.symbol, self.token)
        r = requests.get(url_string)
        if self._check_request(r):
            r = requests.get(url_string)
            return r.json()
        return r.json()

    def _send_news_request(self, endpoint):
        url_string = API_NEWS_ENDPOINT + '{0}?token={1}'.format(self.symbol, self.token)
        r = requests.get(url_string)
        if self._check_request(r):
            r = requests.get(url_string)
            return r.json()
        return r.json()

    def _send_developments_request(self):
        url_string = API_DEVELOPMENTS_ENDPOINT  + '?symbol={0}&token={1}'.format(self.symbol, self.token)
        r = requests.get(url_string)
        if self._check_request(r):
            r = requests.get(url_string)
            return r.json()
        return r.json()

    def _send_news_sentiment_request(self):
        url_string = API_SENTIMENT_ENDPOINT + '?symbol={0}&token={1}'.format(self.symbol, self.token)
        r = requests.get(url_string)
        if self._check_request(r):
            r = requests.get(url_string)
            return r.json()
        return r.json()

    def _get_information(self):
        self._stock_data['profile'] = self._send_request('profile')
        self._stock_data['ceo_compensation'] = self._send_request('ceo-compensation')
        self._stock_data['recommendation'] = self._send_request('recommendation')
        self._stock_data['quote'] = self._send_quote_request()
        self._stock_data['levels'] = self._send_technical_request('support-resistance')
        self._stock_data['indicators'] = self._send_technical_request('technical-indicator')
        self._stock_data['news'] = self._send_news_request('general')
        self._stock_data['developments'] = self._send_developments_request()
        self._stock_data['news_sentiment'] = self._send_news_sentiment_request()

    def stock_data(self):
        return self._stock_data