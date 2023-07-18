import requests

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
    return response.json()

print(postlist(headers))