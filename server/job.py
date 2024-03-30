from model import SignupRecord, PairRecord
from pair import pair_signups
from crud import (
    get_signups_for_form,
    get_active_form_id,
    get_interiew_form_id,
    insert_pairings,
    insert_unpaired,
    update_form_state,
    create_form_with_state,
    get_emails_for_ids,
    get_email_for_id
)


def create_pairings(signups: list[SignupRecord]):
    pairs, unpaired = pair_signups(signups)
    pair_records = [
        PairRecord(form_id=signups[0].form_id, p1_id=pair[0], p2_id=pair[1])
        for pair in pairs
    ]
    unpaired_signups = []
    for uid in unpaired:
        signup = next(s for s in signups if s.user_id == uid)
        unpaired_signups.append(signup)
    return pair_records, unpaired_signups


def main():
    afid = get_active_form_id()
    ifid = get_interiew_form_id()

    if afid == -1:
        raise ValueError("No active form")

    signups = get_signups_for_form(afid)

    if len(signups) == 1:
        return [], [get_email_for_id(signups[0].user_id)]

    if len(signups) < 1:
        raise ValueError("Not enough signups")

    pairings, unpaired = create_pairings(signups)

    insert_pairings(pairings)
    insert_unpaired(unpaired, afid)

    if ifid != -1:
      update_form_state(ifid, "inactive")
    update_form_state(afid, "interview")
    create_form_with_state("active")

    all_emails = get_emails_for_ids([s.user_id for s in signups])

    paired_emails = [
        (all_emails[p.p1_id], all_emails[p.p2_id])
        for p in pairings
    ]

    unpaired_emails = [all_emails[u.user_id] for u in unpaired]

    return paired_emails, unpaired_emails


if __name__ == "__main__":
    main()
