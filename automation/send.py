import requests
import sys
from person import Person
from logutil import read_email_endpoint, read_email_secret, get_week_str, read_last_pairing, write_problems


def EMAIL(recip: Person, partner: Person, problem_link: str) -> str:
    return (
        f"<html>"
        f"<body>"
        f"<p>Hi {recip.name},</p>"
        f"<p>This week you will be partnered with {partner.name}, and you will be interviewing them on <a href='{problem_link}'>{problem_link}</a>. Please reach out to them and schedule a time to meet.</p>"
        f"<p>Email: {partner.email}</p>"
        f"<p>Discord: {partner.discord}</p>"
        f"<p>"
            f"This week's topic will be <b>Heaps/Priority Queues</b>. You'll want to be very comfortable using the API in your language of choice. Check out these resources to learn more:"
        f"</p>"
        f"<ul>"
        f"<li><a href='https://www.geeksforgeeks.org/minimum-operations-required-to-make-every-element-greater-than-or-equal-to-k/'>A practical example problem</a></li>"
        f"<li><a href='https://en.wikipedia.org/wiki/Heap_(data_structure)'>Theory/implementation details</a></li>"
        f"<li><a href='https://docs.oracle.com/javase/8/docs/api/java/util/PriorityQueue.html'>Java PriorityQueue</a></li>"
        f"<li><a href='https://docs.python.org/3/library/heapq.html'>Python heapq</a></li>"
        f"</ul>"
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
    cred = read_email_secret()
    body = {
        "to": email,
        "secret": cred["secret"],
        "subject": "OSIMP Partner " + get_week_str(),
        "content": content,
    }

    content_type = "application/json"

    res = requests.post(cred["endpoint"], json=body, headers={"Content-Type": content_type})

    if res.status_code != 200:
        print(f"[ERROR]: {res.status_code} {res.text}")
        return False

    return True

def send_emails(pairs: list[tuple[Person, Person]], plink_1, plink_2):
    for email, content in generate_emails(pairs, plink_1, plink_2).items():
        send(email, content)


if __name__ == "__main__":
    # pair = [(
    #     Person("A_name", "elimelt@uw.edu", "A_discord"),
    #     Person("B_name", "elimelt@uw.edu", "B_discord"),
    # )]

    # for email, content in generate_emails(pair, "plink_1", "plink_2").items():
    #     send(email, content)

    # read CLI args
    if len(sys.argv) != 3:
        print(f"[ERROR]: Expected 2 arguments, got {len(sys.argv) - 1}")
        sys.exit(1)

    plink_1 = sys.argv[1]
    plink_2 = sys.argv[2]

    write_problems((plink_1, plink_2))

    print(f"Writing problems to file: {plink_1}, {plink_2}")

    pairs = read_last_pairing()

    print(f"Sending emails to {len(pairs)} pairs")

    send_emails(pairs, plink_1, plink_2)

    # https://leetcode.com/problems/merge-k-sorted-lists/description/
    # https://leetcode.com/problems/top-k-frequent-elements/description/