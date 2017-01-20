import requests
import tweepy
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient


class MultipleSearchResource(tornado.web.RequestHandler):

    # @tornado.web.asynchronous
    # @gen.coroutine
    def google(self, query, callback=None):
        google_api_key = 'AIzaSyDnbC_-OlordxU7xfpAPw2pBMkXjm6uwT4'
        google_search_api = "https://www.googleapis.com/customsearch/v1?key={key}&" \
                            "cx=017576662512468239146:omuauf_lfve&q={query}".format(
            key=google_api_key, query=query)
        try:
            google_result = requests.get(google_search_api, timeout=1).json()
        except requests.exceptions.Timeout:
            google_result = {'result': 0, 'message': 'Request timed out'}
        return google_result

    # @tornado.web.asynchronous
    # @gen.coroutine
    def duck_duck_go(self, query):
        duck_duck_go_api = "http://api.duckduckgo.com/?q={query}&format=json".format(query=query)
        try:
            duck_duck_go_result = requests.get(duck_duck_go_api, timeout=1).json()
        except requests.exceptions.Timeout:
            duck_duck_go_result = {'result': 0, 'message': 'Request timed out'}
        return duck_duck_go_result

    # @tornado.web.asynchronous
    # @gen.coroutine
    def twitter(self, query):
        API_KEY = "CEiNihr0GDvuvo4zsa9eEkcAB"
        API_SECRET = "zi3uyW6dqanVvotwdz3sG3ST1rLRCvgF2FVpNvgjMiaZoALo1z"
        auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
        api = tweepy.API(auth, timeout=1)
        try:
            twitter_result = api.search(q=query, count=10)
            twitter_result = [{'text': t.text} for t in twitter_result]
        except requests.exceptions.Timeout:
            twitter_result = {'result': 0, 'message': 'Request timed out'}
        return twitter_result

    # @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        query = self.get_argument("q", default=None, strip=False)
        print 'starting tornado'
        if not query:
            response = {'result': 0}

        else:
            # Google
            # google_api_key = 'AIzaSyDnbC_-OlordxU7xfpAPw2pBMkXjm6uwT4'
            google_api_key = 'AIzaSyD3Jvo-c569LNhyVNoabvJfFo4b2AD88mA'
            google_search_api = "https://www.googleapis.com/customsearch/v1?key={key}&" \
                                "cx=017576662512468239146:omuauf_lfve&q={query}".format(
                key=google_api_key, query=query)

            client = AsyncHTTPClient()
            try:
                google_result = yield client.fetch(google_search_api)
                google_result = google_result.body
            except requests.exceptions.Timeout:
                google_result = {'result': 0, 'message': 'Request timed out'}

            # Duck Duck Go
            duck_duck_go_api = "http://api.duckduckgo.com/?q={query}&format=json".format(query=query)
            try:
                duck_duck_go_result = yield client.fetch(duck_duck_go_api)
                duck_duck_go_result = duck_duck_go_result.body
            except requests.exceptions.Timeout:
                duck_duck_go_result = {'result': 0, 'message': 'Request timed out'}

            # Twitter
            API_KEY = "CEiNihr0GDvuvo4zsa9eEkcAB"
            API_SECRET = "zi3uyW6dqanVvotwdz3sG3ST1rLRCvgF2FVpNvgjMiaZoALo1z"
            auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
            api = tweepy.API(auth, timeout=1)
            try:
                twitter_result = api.search(q=query, count=10)
                twitter_result = [{'text': t.text} for t in twitter_result]
            except requests.exceptions.Timeout:
                twitter_result = {'result': 0, 'message': 'Request timed out'}

            response = {'google': google_result, 'duckduckgo': duck_duck_go_result, 'twitter': twitter_result}

        self.write(response)


application = tornado.web.Application([
    (r"/search/", MultipleSearchResource),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()