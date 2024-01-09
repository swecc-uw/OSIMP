import os
import sys
import json
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from logutil import read_last_entry, write_form_id, write_items, get_week_str
from constants import CLIENT_SECRETS_FILE, SCOPES, API_SERVICE_NAME, API_VERSION, ID_FILE, ITEMS_FILE, NEW_FORM, NEW_QUESTIONS


def create_form():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(authorization_prompt_message="")
    form_service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM(week_str)).execute()

    # Adds the question to the form
    question_setting = (
        form_service.forms()
        .batchUpdate(formId=result["formId"], body=NEW_QUESTIONS)
        .execute()
    )

    # Prints the result to show the question has been added
    print(f'created form with id: {result["formId"]}')
    get_result = form_service.forms().get(formId=result["formId"]).execute()
    items = get_result["items"]
    id = get_result["formId"]
    return id, items




if __name__ == "__main__":
    if not os.path.exists(ID_FILE):
        with open(ID_FILE, "w") as f:
            pass

    if not os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "w") as f:
            pass

    week_str = get_week_str()

    last_date, last_id = read_last_entry(ID_FILE).split(": ") if read_last_entry(ID_FILE) else (None, None)

    if last_date == week_str:
        print("Form already created")
        sys.exit(0)
    else:
        id, items = create_form()
        write_form_id(id, week_str)
        write_items(items)