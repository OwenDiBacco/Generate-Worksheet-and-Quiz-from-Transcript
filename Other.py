from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'owens-web.json'

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/forms.body']

# Authenticate using the service account
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Create the service
service = build('forms', 'v1', credentials=creds)

# Create a new form
form_data = {
    'info': {
        'title': 'My New Google Form'
    }
}
form = service.forms().create(body=form_data).execute()
print(f"Form created with ID: {form['formId']}")