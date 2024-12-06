SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]

DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store_token = Storage("token.json") # token is Tanmay's; Google Forms

credentials = store_token.get() # gets credentials from the token

if not credentials or credentials.invalid:
    
    flow = client.flow_from_clientsecrets("owens-client_secrets.json", SCOPES) # flow object: gets client secret
    credentials = tools.run_flow(flow, store_token)