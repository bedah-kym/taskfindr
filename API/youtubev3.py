"""import os
from googleapiclient.discovery import build
from requests import HTTPError

api_service_name = "youtube"
api_version = "v3"
KEY= os.environ.get('YOUTUBE_API_KEY')

youtube = build(api_service_name, api_version, developerKey=KEY)
#request = youtube.videos().(part="statistics",forUsername="shafer5")
#request = youtube.activities().list(part="contentDetails",channelId="UCDuU0CDDU-hH2GdqQlbMD3w")
request = youtube.videos().list(part='statistics,snippet', id="e9OcytXzBsU")  
try:  
    response = request.execute()
    title = response['items']
    views = response['items'][0]['statistics']['viewCount']  
    likes = response['items'][0]['statistics']['likeCount']  
    print(title)
except HTTPError as error:  
    print('API Error', f'An error occurred: {error}')  """
    
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up your API key
API_KEY =os.environ.get('YOUTUBE_API_KEY')
VIDEO_ID = "e9OcytXzBsU"

def get_youtube_service(api_key):
    """Builds the YouTube service object."""
    return build('youtube', 'v3', developerKey=api_key)

def get_comments(service, video_id):
    """Fetches comments from a YouTube video."""
    try:
        
        request = service.subscriptions().list(
            part='snippet',
            

        )
        response = request.execute()
        
        comments = response.get('items', [])
        print (comments)
        """for comment in comments:
            author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
            print(f'found Username: {author}')"""
            
    
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')

if __name__ == "__main__":
    youtube_service = get_youtube_service(API_KEY)
    get_comments(youtube_service, VIDEO_ID)


