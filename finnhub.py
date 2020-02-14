import requests
from ratelimit import limits, sleep_and_retry
import time

API_ENDPOINT = 'https://finnhub.io/api/v1/stock/'
API_QUOTE_ENDPOINT = 'https://finnhub.io/api/v1/quote'
API_TECHNICAL_ENDPOINT = 'https://finnhub.io/api/v1/scan/'
API_NEWS_ENDPOINT = 'https://finnhub.io/api/v1/news/'
API_DEVELOPMENTS_ENDPOINT = 'https://finnhub.io/api/v1/major-development'
API_SENTIMENT_ENDPOINT = 'https://finnhub.io/api/v1/news-sentiment'

class FinnHub(): 
    def __init__(self, symbol, token): 
        self.failed = []
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
            time.sleep(50)
            return True
        else:
            return False
    
    def _send_request(self, endpoint):
        def generate_url():
            if endpoint == 'support-resistance' or endpoint == 'technical-indicator':
                url_string = API_TECHNICAL_ENDPOINT + endpoint + '?symbol={0}&resolution=D&token={1}'.format(self.symbol, self.token)
            elif endpoint == 'quote':
                url_string = API_QUOTE_ENDPOINT + '?symbol={0}&token={1}'.format(self.symbol, self.token)
            elif endpoint == 'news':
                url_string = API_NEWS_ENDPOINT + '{0}?token={1}'.format(self.symbol, self.token)
            elif endpoint == 'developments':
                url_string = API_DEVELOPMENTS_ENDPOINT  + '?symbol={0}&token={1}'.format(self.symbol, self.token)
            elif endpoint == 'news_sentiment':
                url_string = API_SENTIMENT_ENDPOINT + '?symbol={0}&token={1}'.format(self.symbol, self.token)
            else:
                url_string = API_ENDPOINT + endpoint + '?symbol={0}&token={1}'.format(self.symbol, self.token)
            return url_string
        url_string = generate_url()
        try:
            r = requests.get(url_string, timeout=(2, 10))
        except Exception as e:
            print(e)
            self.failed.append(url_string)
            return {}
        if self._check_request(r):
            try:
                url_string = generate_url()
                r = requests.get(url_string, timeout=(2, 10))
            except Exception as e:
                print(e)
                self.failed.append(url_string)
                return {}
            return r.json()
        return r.json()

    def _get_information(self):
        self._stock_data['profile'] = self._send_request('profile')
        self._stock_data['ceo_compensation'] = self._send_request('ceo-compensation')
        self._stock_data['recommendation'] = self._send_request('recommendation')
        self._stock_data['quote'] = self._send_request('quote')
        self._stock_data['levels'] = self._send_request('support-resistance')
        self._stock_data['indicators'] = self._send_request('technical-indicator')
        self._stock_data['news'] = self._send_request('news')
        self._stock_data['developments'] = self._send_request('developments')
        self._stock_data['news_sentiment'] = self._send_request('news_sentiment')

    def stock_data(self):
        return self._stock_data