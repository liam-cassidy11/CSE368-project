import json
from openai import OpenAI
import msal
from msal import PublicClientApplication
import requests

#MATT'S OPENAI CODE
client = OpenAI()

def classify_email(email: dict) -> dict:
    """
    email = {
        "id": str,
        "from": str,
        "subject": str,
        "body": str
    }
    """

    prompt = f"""
You are an email assistant for a busy user, and your job is to help classify and sort incoming emails.
Summarize this email very briefly, do not restate. Your response should have the following structure:

    "urgency": "high/medium/low",
    "spam": "True/False",
    "recommended_action": "...",
    "reason": "short explanation"

Urgency indicates how important it is that the user view the email, so most emails indicated as spam should be low urgency, 
unless it indicates something like a security issue. 

Sender: {email.get("from", "")}
Subject: {email.get("subject", "")}
Body: {email.get("body", "")}
"""

    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
    )

    text_output = response.output_text
    try:
        result = json.loads(text_output)
    except json.JSONDecodeError:
        cleaned = text_output[text_output.find("{"): text_output.rfind("}")+1]
        result = json.loads(cleaned)

    return result


#MINGI'S GET TOKEN CODE
def get_token():
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
        
    return result

#GET EMAILS, not sure how to do this
def get_emails(token):
    emails = []
    return emails

#LIAM'S UI CODE
def menu():
    print("========= EMAIL SORTER MENU =========")
    print("1. Classify emails")
    print("2. Quit.")

def main():
    token = get_token()
    stored_emails = []

    while True:
        menu() #display menu options from above
        choice = input("Select an option: ")

        #Option 1: Classify emails
        if choice == "1": 

            #Get emails
            emails = get_emails(token)

            #Classify emails
            
            print("\nClassifying emails...\n")

            for email in emails:
                print(f"Email from: {email['from']}")
                print(f"Subject: {email['subject']}")

                classifier = classify_email(email)

                print("Urgency:", classifier["urgency"])
                print("Spam:", classifier["spam"])
                print("Action:", classifier["recommended_action"])
                print("Reason:", classifier["reason"])
                print("-------------------------------------------")

        #Option 2: quit
        elif choice == "2":
            print("Quitting...")
            break
        else:
            print("Invalid option. Please select an option from the menu.")

if __name__ == "__main__":
    main()
