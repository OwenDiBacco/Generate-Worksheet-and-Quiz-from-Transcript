from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define the SCOPES for the Google Forms API
SCOPES = ['https://www.googleapis.com/auth/forms.body']

# Authenticate and create the service
def authenticate():
    creds = None
    # Check if token.pickle exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials, authenticate using credentials.json
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'owens-web-client-secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Main function to create a form and add questions
def create_form():
    creds = authenticate()
    service = build('forms', 'v1', credentials=creds)

    # Create a new form
    form_data = {
        'info': {
            'title': 'My New Google Form'
        }
    }
    form = service.forms().create(body=form_data).execute()
    print(f"Form created with ID: {form['formId']}")

    # Add a question to the form
    question_data = {
        'requests': [
            {
                'createItem': {
                    'item': {
                        'title': 'What is your name?',
                        'questionItem': {
                            'question': {
                                'textQuestion': {}
                            }
                        }
                    },
                    'location': {
                        'index': 0
                    }
                }
            }
        ]
    }
    service.forms().batchUpdate(formId=form['formId'], body=question_data).execute()
    print("Question added to the form.")

if __name__ == '__main__':
    create_form()