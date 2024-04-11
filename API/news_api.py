from newsapi import NewsApiClient
#from blog.models import blogpost
newsapi = NewsApiClient(api_key='1954b06abe1342aea0dbadcaa8c69e89')

""" steps to intergrate news API to database then render to ui
* get news from api using clientlibrary
* parse result if success or failed
* if status == 200 then get information from the json and save it as a blogppost object
* for the writer we might changeit to random staff but cite the original writter
* we could use the description as an excerpt when saving but we need to make sure we handle errors when
there might be missing parameters from json eg descriptions or sources etc
"""


"""# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)
"""
# /v2/top-headlines/sources
#sources = newsapi.get_sources()
CATEGORY_CHOICES = {
    "entertainment":"MUSIC AND ART",
    "technology":"CYBER-SECURITY",
    "sports":"FOOD AND LIFESTYLE",
    "general":"LIFE HACKS AND JOBS",
    "science":"PROGRAMMING AND DATA SCIENCE"
}
def get_breaking_news(newscategory):
    # /v2/top-headlines
    
    #categories =['business','entertainment', 'general', 'health', 'science', 'sports', 'technology']
    top_headlines = newsapi.get_top_headlines(q='',
                                            category=newscategory,
                                            language='en',
                                            country=None)
    if top_headlines["status"]=="ok":
        return top_headlines
    return None
 
def parse_results(newscategory):
    news = get_breaking_news(newscategory)
    if news and news['status'] == "ok":
        total_posts = news['totalResults']
        posts = news['articles'][:2]  # Limit to 2 posts
        all_post_info = []

        for post in posts:
            source = post['source'].get('name', 'Unknown Source')
            OGauthor = post.get('author', 'Unknown Author')
            title = post.get('title', 'No Title')
            excerpt = post.get('description', 'No Description')
            OGlink = post.get('url', '#')
            image = post.get('urlToImage', '#')
            content = post.get('content', 'No Content')
            if content is None:
                content = title
            category=CATEGORY_CHOICES[newscategory]

            post_info = {
                'main_source': source,
                'mainauthor': OGauthor,
                'title': title,
                'excerpt': excerpt,
                'mainlink': OGlink,
                'images': image,
                'content': content,
                'space':category
            }
            all_post_info.append(post_info)

        return all_post_info

    else:
        return []
    
if __name__ == "__main__":
    print(parse_results())















"""
headers = {'Authorization': 'token 9f5a9a44bc881b0055842c6fe7295acaeb8a2303'}

def auth(): 
    endpoint='http://127.0.0.1:8100/api/auth/'
    data = {
        "username":"blogadmin",
        "password": "admin"
    }
    response=requests.post(url=endpoint,data=data)
    return response.json()


def postlist(headers):
    listendpoint = 'http://127.0.0.1:8100/api/myblogs/'
    response = requests.get(url=listendpoint,headers=headers)
    return response.json()["results"]#[0]["spaces"]

print(postlist(headers))
"""
