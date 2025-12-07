import msal
from msal import PublicClientApplication
import requests

client_id = "f7e1e1be-526d-458a-bcef-b377558bc4ef"
authority = "https://login.microsoftonline.com/common/"
username = "mhub_testacc745@outlook.com"
scope = ["Mail.Read","User.Read"]

app = PublicClientApplication(
    client_id, 
    authority=authority
    )

result = None

accounts = app.get_accounts(username=username)
if accounts:
    result = app.acquire_token_silent(scope, account=accounts[0])

if not result:
    result = app.acquire_token_interactive( 
         scopes=scope)
    
#print(result)
#print(result.keys())

if "error" in result.keys():
    print("error, please try again")
else:
    access_token = result['access_token']
    url = "https://graph.microsoft.com/v1.0/me/messages"
    headers = {"Authorization": "Bearer " + access_token, "Host": "graph.microsoft.com", 
               "Prefer": 'outlook.body-content-type="text"'}
    response = requests.get(url, headers=headers)
    print(response.text)

