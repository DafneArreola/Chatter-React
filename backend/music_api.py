import requests
from config import Config #keys and stuff should be moved here

CLIENT_ID = '1a9bd2df8c6c44afbbf527403e7306e3'
CLIENT_SECRET = 'edb1c825d83f4719b733d3b8ed05a4e9'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token/' # used to obtain and refresh token
API_BASE_URL = 'https://api.spotify.com/v1/'

def make_api_call():

    # request params to obrain access_token to make NON PERMISSION calls
    req_body = {
        #'code': request.args['code'],
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    headers = {"Content-Type" : 'application/x-www-form-urlencoded'}

    #print("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode())
    #formatted = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode()
    #encoded = base64.b64encode(formatted)
    #headers = {"Content-Type" : 'application/x-www-form-urlencoded', 
    #           "Authorization" : "Basic {}".format(encoded)} 
    
    response = requests.post(TOKEN_URL, data=req_body, headers=headers)
    token_info = response.json()
    token = token_info['access_token']

    print(token_info)

    print()
    print()




    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    response = requests.get(API_BASE_URL + 'artists/4Z8W4fKeB5YxbusRsdQVPb', headers=headers)
    print(response.json() )
    return response.json()    

make_api_call()
