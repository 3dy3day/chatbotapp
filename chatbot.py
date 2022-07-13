from random import random
from urllib import response
import requests
import json
import wave
import uuid
import os

def main(text):
    url = "https://api-mebo.dev/api"

    json_data = {
        "api_key": os.getenv("MEBO_API_KEY"),
        "agent_id": os.getenv("MEBO_AGENT_ID"),
        "utterance": str(text),
        "uid": "tsukushiai_debuguser"
    } 

    response = requests.post(
        url,
        data = json.dumps(json_data),
        headers={'Content-Type': 'application/json'}
        )

    res_data = response.json()
    response = res_data['bestResponse']['utterance']
    emo = emo_prediction(response)
    return response, emo

def emo_prediction(text):
    client_id     = os.getenv("COTOHA_CLIENT_ID")
    client_secret = os.getenv("COTOHA_CLIENT_SECRET")
    url = 'https://api.ce-cotoha.com/v1/oauth/accesstokens'

    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'grantType'   : 'client_credentials',
        'clientId'    : client_id,
        'clientSecret': client_secret
    })
    with requests.post(url, headers=headers, data=data) as req:
        response = req.json()
    access_token = response['access_token']
    sentence = str(text)

    url = 'https://api.ce-cotoha.com/api/dev/nlp/v1/sentiment'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': f'Bearer {access_token}'
    }
    data = json.dumps({
        'sentence': sentence
    })
    with requests.post(url, headers=headers, data=data) as req:
        response = req.json()
    return response['result']['sentiment']

def generate_wav(text):
    host = "voicevox_engine"
    port = 50021
    params = (
        ('text', text),
        ('speaker', 8),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    hoge_id = str(uuid.uuid4())
    randomid = str(hoge_id) + '.wav'
    wf = wave.open("./static/audio/"+randomid, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()
    return randomid

def delAudio(id):
    os.remove("./static/audio/"+str(id))

