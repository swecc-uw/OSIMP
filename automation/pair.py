from util import get_all_prev_pairings, write_pairs_to_file, get_last_responses
from person import Person


def does_pair_exist(p1: Person, p2: Person, prev_pairings: list[list[tuple[Person, Person]]]) -> bool:
    for prev_pairing in prev_pairings:
        for pair in prev_pairing:
            if p1 in pair and p2 in pair:
                return True

    return False


def pair(people: list[Person]) -> list[tuple[Person, Person]]:

    prev_pairs = get_all_prev_pairings()
    paired = set()

    if prev_pairs is None:
        prev_pairs = []

    out = []

    for i, p1 in enumerate(people):
        if p1 in paired:
            continue

        for p2 in people[i + 1:]:
            if p2 in paired:
                continue

            if not does_pair_exist(p1, p2, prev_pairs):
                out.append((p1, p2))
                paired.add(p1)
                paired.add(p2)
                break

    if len(paired) != len(people):
        print("[WARNING]: the following people were not paired:")
        print(list(filter(lambda x: x not in paired, people)))
    return out

if __name__ == "__main__":
    people = get_last_responses()
    pairs = pair(people)
    print('pair result', pairs)
    write_pairs_to_file(pairs)
    print("wrote pairs to file")

