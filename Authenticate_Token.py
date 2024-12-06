# pip install google-auth google-auth-oauthlib google-auth-httplib2
from google_auth_oauthlib.flow import InstalledAppFlow

# https://www.googleapis.com/auth/forms.responses.readonly
# https://www.googleapis.com/auth/forms.responses.readonly

# https://accounts.google.com/o/oauth2/auth
SCOPES = ['https://www.googleapis.com/auth/forms.responses.readonly']

flow = InstalledAppFlow.from_client_secrets_file('owens-web-client-secret.json', SCOPES)

# 8080
creds = flow.run_local_server(port=8081) # The script will run a local web server that listens for the redirect after the user logs in.

print(f"Access Token: {creds.token}")
