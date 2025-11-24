import msal
from msal import PublicClientApplication

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
    
print(result)

