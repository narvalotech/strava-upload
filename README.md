Simple strava commute uploader
=============================

Uploads a fixed commute to strava.

Needs an "app.json" file where you put the client ID and client secret for the custom app you created on strava.
This app should have localhost as redirect setting.

Auth
----

Use `python strava-auth.py` to launch a server that once visited will prompt you to login and approve the app.
Once the json response is visible in the browser, kill it with Ctrl-C.
It saves the refresh token to refresh_token.txt in the same folder.

Usage
-----

Configure the activity constants in `upload.py` and run it. It should print the list of activities before closing.

Deps
----

Needs flask, requests, probably some other deps.
