from news.models import Story
import unirest

class Services:
    def __init__(self):
        pass

    def create_hackernews_url(self, args):
        base_url = "https://community-hacker-news-v1.p.mashape.com/"
        formatted_args = '/'.join(args)
        end_url = ".json?print=pretty"
        return base_url+formatted_args+end_url

    def create_sentiment_url(self, args):
        base_url = "https://community-sentiment.p.mashape.com/"
        formatted_args = '/'.join(args)
        return base_url+formatted_args+'/'

    def get_headers(self):
        return {
            "X-Mashape-Key": "iJ9qlgSeokmshwV2g5qPIR2N504Jp1IC1nmjsn46PylVKw3cnZ",
            "Accept": "application/json"
        }

    def post_headers(self):
        return {
            "X-Mashape-Key": "iJ9qlgSeokmshwV2g5qPIR2N504Jp1IC1nmjsn46PylVKw3cnZ",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

    def do_get(self, args):
        url = self.create_hackernews_url(args)
        response = unirest.get(url, headers = self.get_headers())
        return response.body

    def setparams(self, text):
        return {
            "txt": text
        }

    def do_post(self, args, text):
        url = self.create_sentiment_url(args)
        response = unirest.post(url, headers=self.post_headers(), params=self.setparams(text))
        return response.body

    def get_sentiment(self, title):
        req=self.do_post(['text'], title)
        return req['result']['sentiment']

    def get_topstories(self, page):
        top_stories_ids = self.do_get(['topstories'])
        obsoleted = Story.objects.exclude(story_id__in = top_stories_ids).delete()

        top_stories_page_ids = top_stories_ids[10*(page-1):10*(page-1)+10]

        stories_in_db = Story.objects.all().values_list('story_id', flat=True)
        stories_in_db = list(stories_in_db)
        stories_to_be_fetched = [item for item in top_stories_page_ids if item not in stories_in_db]

        for story_id in stories_to_be_fetched:
            try:
                _story = self.do_get(['item', str(story_id)])
                _story_id = _story['id']
                _rank = top_stories_ids.index(_story_id)
                _title = _story['title'].encode('utf-8')
                _username = _story['by']
                if 'url' in _story:
                    _url = _story['url']
                else:
                    _url = None
                _score = _story['score']
                if 'text' in _story:
                    _description = _story['text']
                else:
                    _description = None
                _sentiment = self.get_sentiment(_title)
            except:
                pass
            story = Story(story_id=_story_id, username=_username, title=_title, url=_url, score=_score, description=_description, sentiment=_sentiment, rank=_rank)
            story.save()

        top_stories_page = Story.objects.filter(story_id__in = top_stories_page_ids).order_by('rank')
        return top_stories_page
        
