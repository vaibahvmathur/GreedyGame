from rest_framework.decorators import api_view
from django.conf import settings
import urllib, json
from rest_framework.response import Response


def GetGoogle(searched_str):
    key = settings.GOOGLE_KEY
    google_api = 'https://www.googleapis.com/customsearch/v1?key='+key+'&cx=017576662512468239146:omuauf_lfve&q='+searched_str
    response = urllib.urlopen(google_api)
    data = json.loads(response.read())
    try:
        text = data['items'][0]['title']
        url = data['items'][0]['link']
    except Exception as e:
        url = '--NA--'
        text = '--NA--'
    return url, text


def GetDuckDuckgo(searched_str):
    key = settings.GOOGLE_KEY
    duck_api = 'http://api.duckduckgo.com/?q='+searched_str+'&format=json'
    response = urllib.urlopen(duck_api)
    data = json.loads(response.read())
    try:
        url = data['RelatedTopics'][0]['FirstURL']
        text = data['RelatedTopics'][0]['Text']
    except Exception as e:
        url = '--NA--'
        text = '--NA--'
    return url, text


def GetTwitter(searched_str):
    CONSUMER_KEY = settings.CONSUMER_KEY
    CONSUMER_SECRET = settings.CONSUMER_SECRET
    ACCESS_KEY = settings.ACCESS_KEY
    ACCESS_SECRET = settings.ACCESS_SECRET
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)
    timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json"
    # timeline_endpoint = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    response, data = client.request(timeline_endpoint)
    tweets = json.loads(data)
    for tweet in tweets:
        print tweet


@api_view(['GET'])
def HomePage(request):
    final_result = {}
    result = {}
    if 'q' in request.GET:
        searched_str = str(request.GET['q'])
        if searched_str:
            final_result.update({'query': searched_str})
            url, text = GetGoogle(searched_str)
            google = {}
            google.update({'url': str(url)})
            google.update({'text': str(text)})
            result.update({'google': google})
            url, text = GetDuckDuckgo(searched_str)
            duck = {}
            duck.update({'url': str(url)})
            duck.update({'text': str(text)})
            result.update({'duckduckgo': duck})
            # GetTwitter(searched_str)
        else:
            result = "Empty String"
        final_result.update({'result': result})
    else:
        final_result = 'No Search Query'
    return Response(final_result)


