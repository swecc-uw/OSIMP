import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from person import Person
from util import get_last_entry, get_last_form_id, get_last_form_item_dict, write_responses_to_file, get_last_responses
from constants import CLIENT_SECRETS_FILE, SCOPES, API_SERVICE_NAME, API_VERSION




def get_responses_raw():
    form_id = get_last_form_id()

    if not form_id:
        print("No form ID found")
        return

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(authorization_prompt_message="")
    forms_service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    http_res = forms_service.forms().responses().list(formId=form_id).execute()
    return http_res['responses'] if 'responses' in http_res else None


def parse_response(response, item_dict) -> Person:
    answers = response['answers']

    qids = answers.keys()

    name = answers[item_dict['Name']]['textAnswers']['answers'][0]['value']
    email = answers[item_dict['Email']]['textAnswers']['answers'][0]['value']
    discord = answers[item_dict['Discord']]['textAnswers']['answers'][0]['value']

    return Person(name, email, discord)


def parse_responses(responses):
    if not responses:
        return None

    item_dict = get_last_form_item_dict()
    people = [parse_response(x, item_dict) for x in responses]
    return people

def get_responses() -> list[Person]:
    return parse_responses(get_responses_raw())

if __name__ == "__main__":
    responses = get_responses()
    write_responses_to_file(responses)
    print("wrote responses to file")
