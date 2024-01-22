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
            f"This week we will be doing problems that require <b>graph traversal</b> and <b>memoization</b>. Memoization is a very powerful pattern that can be used on a wide variety of problems. You'll want to be comfortable doing a DFS/BFS on both adjacency list and grid representations of graphs, as well as any data structures you choose for saving the intermediate results of sub-problems. Check out these resources to learn more:"
        f"</p>"
        f"<ul>"
        f"<li><a href='https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/'>DFS for adj list</a></li>"
        f"<li><a href='https://www.geeksforgeeks.org/depth-first-traversal-dfs-on-a-2d-array/'>DFS for 2D grid</a></li>"
        f"<li><a href='https://www.geeksforgeeks.org/what-is-memoization-a-complete-tutorial/'>Overview of memoization</a></li>"
        f"</ul>"
        f"<p>It's worth mentioning that this week's problems are intentionally a step up in difficulty from previous weeks. If you're struggling to understand your assigned question, feel free to reach out to me (Elijah) over discord (elimelt)."
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
        print("========================================================")
        print(f"Sent email to {email}")
        print(content)
        print("========================================================")


if __name__ == "__main__":


    # pair = [(
    #     Person("A_name", "elimelt@uw.edu", "A_discord"),
    #     Person("B_name", "elimelt@cs.washington.edu", "B_discord"),
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

    # https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
    # https://leetcode.com/problems/evaluate-division/