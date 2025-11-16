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

def main():
    email = {
        "id": "XYZ123",
        "from": "promo@weirdsite.biz",
        "subject": "YOU WON A PRIZE!!!",
        "body": "Click here for reward..."
    }
    result = classify_email(email)
    print(f'\nUrgency = {result['urgency']}\nSpam = {result['spam']}\nRecommended Action = {result['recommended_action']}\nReason = {result['reason']}\n')

if __name__ == "__main__":
    main()
