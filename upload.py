from datetime import datetime
import requests
import json

# Oauth settings
# Use the strava-auth.py in the same folder to do the first auth
with open('app.json') as f:
    js = json.loads(f.read())
    client_id = js['client_id']
    client_secret = js['client_secret']

# Activity settings
name = 'Commute'
act_type = 'Ride'
start_date_local = datetime.now().isoformat()
# start_date_local = datetime(2021, 10, 7, 17, 00).isoformat()
elapsed_time = (60 * 25)
description = 'Commute by bicycle'
distance = '10000'
commute = 1

# Print request responses
debug = 0

# If any errors, run the strava-auth script first
with open('refresh_token.txt') as f:
    refresh_token = f.read()

print('Request auth token from strava')
response = requests.post(
    'https://www.strava.com/api/v3/oauth/token',
    params={'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'refresh_token', 'refresh_token': refresh_token}
)
if debug:
    print(response)
token = response.json()['access_token']

print('Get user info')
response = requests.get(
    'https://www.strava.com/api/v3/athlete',
    headers={'Authorization': f'Bearer {token}'},
)
if debug:
    print(response.json())

print('Write activity')
response = requests.post(
    'https://www.strava.com/api/v3/activities',
    headers={'Authorization': f'Bearer {token}'},
    params={'name': name, 'type': act_type, 'start_date_local': start_date_local, 'elapsed_time': elapsed_time, 'description': description, 'distance': distance, 'commute': commute},
)
if debug:
    print(response.json())

print('Read back activities')
response = requests.get(
    'https://www.strava.com/api/v3/athlete/activities',
    headers={'Authorization': f'Bearer {token}'},
)
if debug:
    print(response.json())

for r in response.json():
    d = datetime.fromisoformat(r['start_date_local'][0:-1])
    datestring = '{}  {:2d}:{:02d}'.format(d.date().isoformat(),
                                           d.hour, d.minute)
    print('({}) {:20} {:6} km, {:5} mins, avg {:3} km/h'.format(
        datestring,
        r['name'],
        r['distance'] / 1000,
        r['elapsed_time'] / 60,
        round(r['average_speed'] * 3.6)
    ))
