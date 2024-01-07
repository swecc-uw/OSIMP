import os
import json
from datetime import datetime, timedelta
from constants import ID_FILE, ITEMS_FILE, RESPONSES_FILE, PAIRS_FILE, EMAIL_SECRETS_FILE
from person import Person


def get_last_entry(file_path):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as file:
        entries = file.read().splitlines()
        return entries[-1] if entries else None

def get_last_form_id():
    return get_last_entry(ID_FILE).split(": ")[-1] if get_last_entry(ID_FILE) else None

def get_last_form_item_dict():
    return {x.split(": ")[0]: x.split(": ")[1] for x in get_last_entry(ITEMS_FILE).split(', ')} if get_last_entry(ITEMS_FILE) else None

def get_last_responses():
    if get_last_entry(RESPONSES_FILE) is None:
        return None

    ent = get_last_entry(RESPONSES_FILE).split("; ")
    return [Person(*x.split(", ")) for x in ent] if ent else None

def get_last_n_pairings(n) -> list[list[tuple[Person, Person]]]:
    num_prev = get_num_records(PAIRS_FILE)

    if n <= 0 or n > num_prev or get_last_entry(PAIRS_FILE) is None:
        return None

    out = []

    for line in reversed(list(open(PAIRS_FILE))[:n]):
        curr = []
        for pair in line.strip().split("; "):
            p1, p2 = pair.split(" - ")
            curr.append((Person(*p1.split(", ")), Person(*p2.split(", "))))

        out.append(curr)

    return out

def get_all_prev_pairings() -> list[tuple[Person, Person]]:
    num_prev = get_num_records(PAIRS_FILE)
    return get_last_n_pairings(num_prev)

def get_last_pairings() -> list[tuple[Person, Person]]:
    if get_num_records(PAIRS_FILE) == 0:
        return None

    return get_last_n_pairings(1)[0]

def write_id_to_file(id, week_str):
    with open(ID_FILE, "a") as f:
        f.write(f"{week_str}: {id}\n")

def write_items_to_file(items):
    with open(ITEMS_FILE, "a") as f:
        out = { i["title"]: i["questionItem"]['question']['questionId'] for i in items }
        for i, (k, v) in enumerate(out.items()):
            if i != 0:
                f.write(", ")
            f.write(f"{k}: {v}")

        f.write("\n")

def write_responses_to_file(responses: list[Person]):
    with open(RESPONSES_FILE, "a") as f:
        for i, response in enumerate(responses):
            if i != 0:
                f.write("; ")
            f.write(str(response))

        f.write("\n")

def write_pairs_to_file(pairs: list[tuple[Person, Person]]):
    if not os.path.exists(PAIRS_FILE):
        with open(PAIRS_FILE, "w") as f:
            pass

    if len(pairs) == 0:
        print("[WARNING]: No pairs to write")
        return

    with open(PAIRS_FILE, "a") as f:
        num_written = 0
        for i, pair in enumerate(pairs):
            if i != 0:
                f.write("; ")
            f.write(f"{pair[0].name}, {pair[0].email}, {pair[0].discord} - {pair[1].name}, {pair[1].email}, {pair[1].discord}")
            num_written += 1

        if num_written != 0:
            f.write("\n")

def get_week_str():
    # this monday
    this_week = datetime.today() - timedelta(days=datetime.today().weekday())
    # format as MM/DD
    return this_week.strftime("%m/%d")

def get_num_records(file_path):
    if not os.path.exists(file_path):
        return 0

    with open(file_path, "r") as file:
        return len(file.readlines())

def get_email_secret():
    with open(EMAIL_SECRETS_FILE, "r") as file:
        return json.load(file).get("secret")

def get_email_endpoint():
    with open(EMAIL_SECRETS_FILE, "r") as file:
        return json.load(file).get("endpoint")