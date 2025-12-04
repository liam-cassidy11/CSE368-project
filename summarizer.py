from datetime import datetime
from openai import OpenAI
from sort_email import classify_email
import sys

summary_client = OpenAI()

def summarize_interval_emails(processed_emails: list[dict], interval_minutes: int) -> dict:
    """
    processed_emails: list of email dicts already classified using classify_email()
        Each item must look like:
        {
            "id": "...",
            "from": "...",
            "subject": "...",
            "urgency": "...",
            "spam": True/False,
            "recommended_action": "...",
            "reason": "..."
        }
    interval_minutes: how often this summary is generated (user-chosen)

    """

    important_items = []
    spam_count = 0

    for e in processed_emails:
        if e["spam"] or e["spam"] == "True":
            spam_count += 1
        else:
            important_items.append(e)

    prompt = f"""
Create a SHORT summary of the most important emails received in the last {interval_minutes} minutes.

Only include:
- A brief intro (1 short sentence)
- A short ordered list of emails the user should check first. Include the email subject (CUT IT OFF IF EXCEEDING 50 CHARACTERS) and a very brief description (couple of words) as to why it's listed as urgent
- A single sentence about spam: "Spam removed: # of spam"

Do NOT restate full bodies. Keep everything compact.

Emails:
{important_items}

Spam count: {spam_count}
"""
    
    response = summary_client.responses.create(
        model="gpt-5-nano",
        input=prompt
    )

    output_text = response.output_text.strip()

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "summary_text": output_text
    }


def test1():
    raw_emails = [
        {
            "id": "498",
            "from": "boss@example.com",
            "subject": "Project deadline moved up",
            "body": "We need to ship the project one week earlier. Please review the new schedule."
        },
        {
            "id": "499",
            "from": "friend@example.com",
            "subject": "Dinner this weekend?",
            "body": "Hey, are you free on Saturday for dinner?"
        },
        {
            "id": "500",
            "from": "newsletter@randompromo.biz",
            "subject": "SUPER SALE on things you don't need",
            "body": "Huge discounts!! Limited time!!"
        },
    ]

    processed_emails = []
    for e in raw_emails:
        classified = classify_email(e)
        processed_emails.append(classified)

    
    print(processed_emails)
    summary = summarize_interval_emails(processed_emails, interval_minutes=30)

    print("Summary generated at:", summary["timestamp"])
    print("-------- SUMMARY TEXT --------")
    print(summary["summary_text"])
    print("------------------------------")


def main():
    if "--test1" in sys.argv:
        test1()
        return


if __name__ == "__main__":
    main()