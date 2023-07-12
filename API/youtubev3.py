import os
from googleapiclient.discovery import build
from requests import HTTPError

api_service_name = "youtube"
api_version = "v3"
KEY = "AIzaSyCh3AOeBlquScKAMYulyt9x70yf-r1rF0A"

youtube = build(api_service_name, api_version, developerKey=KEY)
#request = youtube.videos().(part="statistics",forUsername="shafer5")
#request = youtube.activities().list(part="contentDetails",channelId="UCDuU0CDDU-hH2GdqQlbMD3w")
request = youtube.videos().list(part='statistics,snippet', id="e9OcytXzBsU")  
try:  
    response = request.execute()  
    title = response['items'][0]['snippet']['title']  
    views = response['items'][0]['statistics']['viewCount']  
    likes = response['items'][0]['statistics']['likeCount']  
    print(title,views,likes,response)
except HTTPError as error:  
    print('API Error', f'An error occurred: {error}')  

