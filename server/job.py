from typing import List
from model import SignupRecord, PairRecord
from pair import pair_signups
from crud import get_signups_for_form, get_active_form_id, delete_all_pairings_for_form, insert_pairings

def clear_active_form_pairings():
  form_id = get_active_form_id()
  if form_id == -1:
    return -1

  delete_all_pairings_for_form(form_id)
  return form_id

def create_pairings(signups: List[SignupRecord]):
  pairs, unpaired = pair_signups(signups)
  pair_records = [PairRecord(form_id=signups[0].form_id, p1_id=pair[0], p2_id=pair[1]) for pair in pairs]
  unpaired_signups = []
  for uid in unpaired:
    signup = next(s for s in signups if s.user_id == uid)
    unpaired_signups.append(signup)
  return pair_records, unpaired_signups

def main():
  fid = clear_active_form_pairings()

  if fid == -1:
    return [], []

  signups = get_signups_for_form(fid)
  pairings, unpaired = create_pairings(signups)
  insert_pairings(pairings)

  return pairings, unpaired



if __name__ == "__main__":
  main()