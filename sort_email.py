import sys
import json
from openai import OpenAI

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


Ensure your response is in dictionary format using curly brackets, and uses a linebreak after the open curly bracket, as well as each key/value pair in the dict

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


    raw = response.output_text.strip()
    #print(raw + '\n')
    
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {
            "urgency": "low",
            "spam": True,
            "recommended_action": "ignore",
            "reason": "Model returned unexpected output; defaulting to low importance."
        }

    if parsed.get("spam") == "True" or parsed.get("spam") == "true":
        parsed["spam"] = True
    elif parsed.get("spam") == "False" or parsed.get("spam") == "false":
        parsed["spam"] = False

    return {
        "id": email.get("id"),
        "from": email.get("from"),
        "subject": email.get("subject"),
        "urgency": parsed.get("urgency"),
        "spam": parsed.get("spam"),
        "recommended_action": parsed.get("recommended_action", ""),
        "reason": parsed.get("reason", "")
    }




def test1():
    email = {
        "id": "XYZ123",
        "from": "promo@weirdsite.biz",
        "subject": "YOU WON A PRIZE!!!",
        "body": "Click here for reward..."
    }
    result = classify_email(email)
    print(result)




def main():
    if "--test1" in sys.argv:
        test1()
        return

if __name__ == "__main__":
    main()
