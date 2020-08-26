import requests

TALKAPI_KEY = 'DZZSPWtxfG7VGhTzbvsSqYzP3FJvQrUP'

def talkapi(text):
    url = 'https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk'
    req = requests.post(url, {'apikey':TALKAPI_KEY,'query':text}, timeout=5)
    data = req.json()

    if data['status'] != 0:
        return data['message']

    msg = data['results'][0]['reply']
    return msg