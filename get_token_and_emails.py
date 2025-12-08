import msal
from msal import PublicClientApplication
import requests

# username = "mhub_testacc745@outlook.com"
# scope = ["Mail.Read","User.Read"]

def create_token_app():
    #In order to obtain an authorization token, first you need a public client application. Public means that the user
    #cannot be trusted to hold a client secret, and I think it fits for this application since everything will be on 
    #the user's device, and we won't have a server or anything. Once you pass the client id (my application's id that I 
    #registered in microsoft azure), and the authority, (I think this is the page microsoft takes you to if you need to authorize
    #the account), you will be set.
    client_id = "f7e1e1be-526d-458a-bcef-b377558bc4ef"   
    authority = "https://login.microsoftonline.com/common/"

    app = PublicClientApplication(
        client_id, 
        authority=authority
        )
    
    return app

def acquire_authorization_token(app, username, scope):
    #From there, acquiring the authorization token goes like this: Do we already have the authorization token at hand? If yes, then
    #do the silent obtaining and obtain the token. If we don't, ask the user on a website to grant access to an account through the
    #application.
    result = None

    accounts = app.get_accounts(username=username)
    if accounts:
        result = app.acquire_token_silent(scope, account=accounts[0])

    if not result:
        result = app.acquire_token_interactive( 
            scopes=scope)
        
    return result

def get_emails(access_token):
    #Once we do have the access token, we just send the request over and obtain the emails using it!
    url = "https://graph.microsoft.com/v1.0/me/messages"
    headers = {"Authorization": "Bearer " + access_token, "Host": "graph.microsoft.com", 
               "Prefer": 'outlook.body-content-type="text"'}
    response = requests.get(url, headers=headers)
    if response.ok == False: 
        return -1
    
    return response.json().get("value", [])

