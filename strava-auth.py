import os
import requests
import urllib.parse
import json

from flask import Flask, request, Response, jsonify, redirect

app = Flask(__name__)

with open('app.json') as f:
    js = json.loads(f.read())
    STRAVA_CLIENT_ID = js['client_id']
    STRAVA_CLIENT_SECRET = js['client_secret']

REDIRECT_URI = 'http://localhost:5000/strava_redirect'

def exchange_token(code):
    strava_request = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )

    # Write refresh token to file
    with open('refresh_token.txt', 'w') as f:
        f.write(strava_request.json()['refresh_token'])

    # Print full response in browser
    return jsonify(strava_request.json())

@app.route('/', methods=['GET'])
def strava_authorize():
    params = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'activity:read_all,activity:write'
    }
    return redirect('{}?{}'.format(
        'https://www.strava.com/oauth/authorize',
        urllib.parse.urlencode(params)
    ))

@app.route('/strava_redirect', methods=['GET'])
def strava_token():
    code = request.args.get('code')
    if not code:
        return Response('Error: Missing code param', status=400)
    return exchange_token(code)


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
