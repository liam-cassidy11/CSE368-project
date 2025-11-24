import requests

access_token = "insert_access_token_here"
url = "https://graph.microsoft.com/v1.0/me/messages"
headers = {"Authorization": "Bearer " + access_token, "Host": "graph.microsoft.com"}
response = requests.get(url, headers=headers)
print(response.text)