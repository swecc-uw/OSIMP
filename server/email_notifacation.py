import dotenv
import os
import requests

from crud import (
    get_emails_for_ids,
    get_signups_for_form,
    get_pairings_for_form,
    get_unpaired_for_form,
    get_interiew_form_id,
)

dotenv.load_dotenv()

EMAIL_SECRET = os.getenv("EMAIL_SECRET")
EMAIL_ENDPOINT = os.getenv("EMAIL_ENDPOINT")

def send(email: str, content: str, subject: str):
    """
    to, from, subject, content
    """
    body = {
        "to": email,
        "secret": EMAIL_SECRET,
        "subject": subject,
        "content": content,
    }
    print(body)
    content_type = "application/json"

    res = requests.post(EMAIL_ENDPOINT, json=body, headers={"Content-Type": content_type})

    if res.status_code != 200:
        print(f"[ERROR]: {res.status_code} {res.text}")
        return False

    return True


def get_emails_to_send_for_form(form_id: int) -> tuple[list[tuple[str, str]], list[str], dict[str, str]]:
    signups = get_signups_for_form(form_id)
    unpaired = get_unpaired_for_form(form_id)
    pairs = get_pairings_for_form(form_id)
    if len(signups) == 1:
        return get_emails_for_ids([signups[0].user_id])
    if len(signups) < 1:
        raise ValueError("Not enough signups")
    emails: dict = get_emails_for_ids([s.user_id for s in signups])

    return [
        (p.p1_id, p.p2_id)
        for p in pairs
    ], [u for u in unpaired], emails


if __name__ == "__main__":
  print(get_emails_to_send_for_form(24))