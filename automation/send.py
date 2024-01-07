import requests
import sys
from person import Person
from util import get_email_endpoint, get_email_secret, get_week_str, get_last_pairings


def EMAIL(recip: Person, partner: Person, problem_link: str) -> str:
    return (
        f"<html>"
        f"<body>"
        f"<p>Hi {recip.name},</p>"
        f"<p>This week you will be partnered with {partner.name}, and you will be interviewing them on <a href='{problem_link}'>{problem_link}</a>. Please reach out to them and schedule a time to meet.</p>"
        f"<p>Email: {partner.email}</p>"
        f"<p>Discord: {partner.discord}</p>"
        f"<p>Good luck!</p>"
        f"<p>Best,</p>"
        f"<p>SWECC Leadership</p>"
        f"</body>"
        f"</html>"
    )


def generate_emails(pairs: list[tuple[Person, Person]], plink_1, plink_2):
    out = {}

    for pair in pairs:
        out[pair[0].email] = EMAIL(pair[0], pair[1], plink_1)
        out[pair[1].email] = EMAIL(pair[1], pair[0], plink_2)

    return out


def send(email: str, content: str):
    """
    to, from, subject, content
    """

    body = {
        "to": email,
        "secret": get_email_secret(),
        "subject": "OSIMP Partner " + get_week_str(),
        "content": content,
    }

    content_type = "application/json"

    res = requests.post(get_email_endpoint(), json=body, headers={"Content-Type": content_type})

    if res.status_code != 200:
        print(f"[ERROR]: {res.status_code} {res.text}")
        return False

    return True

def send_emails(pairs: list[tuple[Person, Person]], plink_1, plink_2):
    for email, content in generate_emails(pairs, plink_1, plink_2).items():
        send(email, content)


if __name__ == "__main__":
    # pairs = [
    #     (
    #         Person("A_name", "elimelt@uw.edu", "A_discord"),
    #         Person("B_name", "elimelt@uw.edu", "B_discord"),
    #     ),
    #     (
    #         Person("C_name", "elimelt@uw.edu", "C_discord"),
    #         Person("D_name", "elimelt@uw.edu", "D_discord"),
    #     ),
    # ]
    # for email, content in generate_emails(pairs, "plink_1", "plink_2").items():
    #     send(email, content)

    # read CLI args
    if len(sys.argv) != 3:
        print(f"[ERROR]: Expected 2 arguments, got {len(sys.argv) - 1}")
        sys.exit(1)

    plink_1 = sys.argv[1]
    plink_2 = sys.argv[2]

    pairs = get_last_pairings()

    send_emails(pairs, plink_1, plink_2)

