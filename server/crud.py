import os
import logging
import dataclasses
from model import SignupRecord, PairRecord
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

def get_active_form_id() -> int:
    res = supabase.table("forms").select("id").order("created_at", desc=True).limit(1).execute()

    if len(res.data) == 0:
        return -1
    return res.data[0]["id"]

def main():
    signups = get_signups()
    print(signups)


if __name__ == "__main__":
    main()