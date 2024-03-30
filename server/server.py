import os
import json
import threading
from datetime import datetime
from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from job import main
from model import EmailRequest, TestEmailRequest
from email_notifacation import send, get_emails_to_send_for_form
from crud import (
    get_interiew_form_id,
    get_emails_sent_for_form,
    add_sent_emails,
    get_pairings_for_form,
    get_unpaired_for_form,
    get_emails_for_ids,
    get_all_form_ids
)

# Global variables to store status and result
status = "waiting"
result = None
timestamp = None


# Function for script execution to be run in another thread
def run_script():
    global status
    global result
    global timestamp
    print("Running script")
    try:
        pairings, unpaired = main()
    except Exception as e:
        status = "error"
        result = str(e)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("error: ", e)
        return

    print("Script execution completed successfully")

    print(pairings)
    print(unpaired)
    # delete old files
    try:
        os.remove("cache/pairings.json")
    except:
        pass

    try:
        os.remove("cache/unpaired.json")
    except:
        pass

    # save to file
    with open("cache/pairings.json", "w") as f:
        json.dump(pairings, f, default=lambda x: x.__dict__)

    with open("cache/unpaired.json", "w") as f:
        json.dump(unpaired, f, default=lambda x: x.__dict__)

    # After completion, update status and result
    status = "finished"
    result = "Script execution completed successfully"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dotenv.load_dotenv()
SCRIPT_SECRET = os.getenv("SCRIPT_SECRET")


@app.get("/")
def serve_html():
    file = "admin.html"
    with open(file, "r") as f:
        content = f.read()
        return HTMLResponse(content)


@app.get("/execute-script")
def execute_script(secret: str):
    global status

    if secret != SCRIPT_SECRET:
        return {"message": "Unauthorized"}

    if status == "running":
        return {"message": "Script already running"}

    status = "running"
    thread = threading.Thread(target=run_script)
    thread.start()

    return {"message": "Script execution started"}


@app.get("/status")
def get_status():
    return {"status": status, "timestamp": timestamp}


@app.get("/local/pairs")
def get_pairs_local():
    try:
        with open("cache/pairings.json", "r") as f:
            pairings = json.load(f)
        return {"pairings": pairings, "timestamp": timestamp}
    except:
        return {"message": "cache miss, execute script first"}


@app.get("/local/unpaired")
def get_unpaired_local():

    try:
        with open("cache/unpaired.json", "r") as f:
            unpaired = json.load(f)
        return {"unpaired": unpaired, "timestamp": timestamp}
    except:
        return {"message": "cache miss, execute script first"}


@app.get("/unpaired/{form_id}")
def get_unpaired_remote(form_id: int):
    unpaired = get_unpaired_for_form(form_id)
    emails = get_emails_for_ids(unpaired)
    return {"unpaired": list(emails.values())}


@app.get("/pairs/{form_id}")
def get_pairs_remote(form_id: int):
    pairs = get_pairings_for_form(form_id)
    emails = get_emails_for_ids([p.p1_id for p in pairs] + [p.p2_id for p in pairs])
    return {"pairs": [(emails[p.p1_id], emails[p.p2_id]) for p in pairs]}


@app.post("/email")
def email(req: EmailRequest):
    if status == "running":
        return {"message": "Script not finished running"}

    resend = req.resend
    upcontent = req.unpaired_content
    pcontent = req.paired_content
    upsubject = req.unpaired_subject
    psubject = req.paired_subject

    if "" in [upcontent, pcontent, upsubject, psubject]:
        return {"message": f"Missing email content or subject"}

    active_form_id = get_interiew_form_id()
    pairings_uid, unpaired_uid, email_dict = get_emails_to_send_for_form(active_form_id)

    already_sent_uid = set(get_emails_sent_for_form(active_form_id))
    new_sent_paired, new_sent_unpaired = [], []

    for pair in pairings_uid:

        if pair[0] not in already_sent_uid or resend:
            send(email_dict[pair[0]], pcontent, psubject)
            new_sent_paired.append(pair[0])

        if pair[1] not in already_sent_uid or resend:
            send(email_dict[pair[1]], pcontent, psubject)
            new_sent_paired.append(pair[1])

    for uid in unpaired_uid:
        if uid not in already_sent_uid or resend:
            send(email_dict[uid], upcontent, upsubject)
            new_sent_unpaired.append(uid)

    if not resend:
        add_sent_emails(active_form_id, new_sent_paired, pcontent, psubject)
        add_sent_emails(active_form_id, new_sent_unpaired, upcontent, upsubject)
    else:
        up_actual_new_sent = [
            uid for uid in new_sent_unpaired if uid not in already_sent_uid
        ]
        p_actual_new_sent = [
            uid for uid in new_sent_paired if uid not in already_sent_uid
        ]
        add_sent_emails(active_form_id, p_actual_new_sent, pcontent, psubject)
        add_sent_emails(active_form_id, up_actual_new_sent, upcontent, upsubject)

    return {
        "sent_paired": [email_dict[p] for p in new_sent_paired],
        "sent_unpaired": [email_dict[u] for u in new_sent_unpaired],
    }


@app.post("/test-email")
def test_email(req: TestEmailRequest):
    send(req.email_paired, req.paired_content, req.paired_subject)
    send(req.email_unpaired, req.unpaired_content, req.unpaired_subject)
    return {"message": "Test email sent"}

@app.get("/forms")
def get_forms():
    return {"forms": get_all_form_ids()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
