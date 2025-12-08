import json
from openai import OpenAI
import msal
from msal import PublicClientApplication
import requests

from get_token_and_emails import create_token_app, acquire_authorization_token, get_emails

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
Summarize this email very briefly, do not restate. Respond ONLY with a valid JSON object (no extra text).
Your response should have the following structure:

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

#LIAM'S UI CODE
def menu():
    print("========= EMAIL SORTER MENU =========")
    print("1. Authorize app & obtain authorization token")
    print("2. Classify emails")
    print("3. Quit.")

def main():
    app = create_token_app()
    access_token = ""
    while True:
        menu() #display menu options from above
        choice = input("Select an option: ")

        #Option 1: Authorization
        if choice == "1":
            username = input("Please type in the email account that you wish to check the emails for. If an account has been authorized previously, the process will be automatic. Otherwise, you will need to manually authorize the application.")
            authorization_result = acquire_authorization_token(app, username, ["Mail.Read","User.Read"])
            if "error" in authorization_result.keys():
                print("There was either a cancellation or some sort of error during the authorization! Please try again.")
            else:
                access_token = authorization_result['access_token']
                print("Access token obtained!")
        #Option 2: Classify emails
        elif choice == "2": 
            #Get emails
            emails = get_emails(access_token)
            if emails == -1:
                print("There was an error obtaining the emails! Please refresh your access token, as that is most likely the problem.")

            #Classify emails
            
            print("\nClassifying emails...\n")

            for email in emails:
                
                classifier = classify_email(email)

                print(f"Email from: {((email['from'])['emailAddress'])['address']} ({((email['from'])['emailAddress'])['name']})")
                print(f"Subject: {email['subject']}")
                print("Urgency:", classifier["urgency"])
                print("Spam:", classifier["spam"])
                print("Action:", classifier["recommended_action"])
                print("Reason:", classifier["reason"])
                print("-------------------------------------------")

        #Option 3: quit
        elif choice == "3":
            print("Quitting...")
            break
        else:
            print("Invalid option. Please select an option from the menu.")

if __name__ == "__main__":
    main()
