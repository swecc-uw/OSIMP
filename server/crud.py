import os
import logging
import dataclasses
import uuid
from model import EmailRequest, Problem, SignupRecord, PairRecord
from typing import List
from supabase import create_client, Client
import dotenv
logging.getLogger("httpx").setLevel(logging.WARNING)
dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_signups() -> List[SignupRecord]:
    signups_data = supabase.table("signups").select("*").execute().data
    signups = []
    for signup in signups_data:
        signup_record = SignupRecord(
            created_at=signup['created_at'],
            form_id=signup['form_id'],
            availability=signup['availability'],
            user_id=signup['user_id']
        )
        signups.append(signup_record)
    return signups

def get_signups_for_form(form_id: int) -> List[SignupRecord]:
    signups_data = supabase.table("signups").select("*").match({"form_id": form_id}).execute().data
    signups = []
    for signup in signups_data:
        signup_record = SignupRecord(
            created_at=signup['created_at'],
            form_id=signup['form_id'],
            availability=signup['availability'],
            user_id=signup['user_id']
        )
        signups.append(signup_record)
    return signups

def delete_all_pairings_for_form(form_id: int) -> None:
    supabase.table("pairs").delete().match({"form_id": form_id}).execute()

def insert_pairings(pairing: List[PairRecord]) -> None:
    supabase.table("pairs").insert([dataclasses.asdict(p) for p in pairing]).execute()

def insert_unpaired(unpaired: List[SignupRecord], form_id: int) -> None:
    print(unpaired)
    unpaired_records = [{"form_id": form_id, "user_id": sr.user_id} for sr in unpaired]
    supabase.table("unpaired").insert(unpaired_records).execute()

def get_active_form_id() -> int:
    res = supabase.table("forms").select("id").eq("state", "active").execute()

    if len(res.data) != 1:
        return -1

    return res.data[0]["id"]

def get_interiew_form_id() -> int:
    res = supabase.table("forms").select("id").eq("state", "interview").execute()

    if len(res.data) != 1:
        return -1

    return res.data[0]["id"]

def update_form_state(form_id: int, state: str) -> None:
    supabase.table("forms").update({"state": state}).eq("id", form_id).execute()

def create_form_with_state(state: str) -> int:
    if state not in ["active", "interview", "inactive"]:
        raise ValueError("Invalid state")

    if state == "active" or state == "interview":

        res = supabase.table("forms").select("id").eq("state", state).execute()
        if len(res.data) > 0:
            raise ValueError(f"There is already a form with state {state}")

    res = supabase.table("forms").insert({"state": state}).execute()
    return res.data[0]["id"]

def get_email_for_id(user_id: str) -> str:
    res = supabase.table("users").select("email").eq("user_id", user_id).execute()
    if len(res.data) != 1:
        return ""
    return res.data[0]["email"]

def get_emails_for_ids(user_ids: List[uuid.UUID]):
    res = supabase.table("users").select("email,user_id").in_("user_id", user_ids).execute()
    return {
        user["user_id"]: user["email"]
        for user in res.data
    }

def get_emails_sent_for_form(form_id: int) -> List[str]:
    res = supabase.table("email_notifications").select("user_id").eq("form_id", form_id).execute()
    return [r["user_id"] for r in res.data]

def get_pairings_for_form(form_id: int) -> List[PairRecord]:
    res = supabase.table("pairs").select("*").eq("form_id", form_id).execute()
    pairings = []
    for pairing in res.data:
        pair_record = PairRecord(
            form_id=pairing['form_id'],
            p1_id=pairing['p1_id'],
            p2_id=pairing['p2_id']
        )
        pairings.append(pair_record)
    return pairings

def get_unpaired_for_form(form_id: int) -> List[str]:
    res = supabase.table("unpaired").select("user_id").eq("form_id", form_id).execute()
    return [r["user_id"] for r in res.data]

def add_sent_emails(form_id: int, user_ids: List[str], content: str, subject: str) -> None:
    sent_already = set(get_emails_sent_for_form(form_id))

    if any(uid in sent_already for uid in user_ids):
        raise ValueError("Some emails already sent")

    records = [{"form_id": form_id, "user_id": uid, "contents": content, "subject": subject} for uid in user_ids]
    supabase.table("email_notifications").insert(records).execute()

def get_all_form_ids() -> List[int]:
    res = supabase.table("forms").select("id").execute()
    return [r["id"] for r in res.data]

def upload_problem(problem1: Problem) -> None:
    supabase.table("problems").insert(dataclasses.asdict(problem1)).execute()

def get_problems_for_form(form_id: int) -> List[Problem]:
    res = supabase.table("problems").select("*").eq("form_id", form_id).execute()
    print(res)

    return [
        Problem(
            problem_url=r["problem_url"],
            problem_number=r["problem_number"],
            form_id=r["form_id"],
            seq=r["seq"],
            topic=r["topic"]
        ) for r in res.data]

def main():
    fid = get_active_form_id()
    if fid == -1:
        raise ValueError("No active form")
    emails_sent = get_emails_sent_for_form(fid)
    print(emails_sent)


if __name__ == "__main__":
    main()