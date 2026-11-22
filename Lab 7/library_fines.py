import re

_MEMBER_RE = re.compile(r"([A-Za-z]+)-([0-9]+)")
_DAYS_RE = re.compile(r"[0-9]{1,9}")  # ASCII digits only, bounded length
MAX_DAYS_ALLOWED = 14
FINE_PER_DAY = 2


def parse_member_id(member_id):
    """Return (TYPE, number) for IDs like 'STU-1023', or None if invalid."""
    if not isinstance(member_id, str):
        return None
    match = _MEMBER_RE.fullmatch(member_id.strip())
    if not match:
        return None
    member_type, number = match.groups()
    if len(number) > 18:  # avoid absurdly large numbers
        return None
    return member_type.upper(), int(number)


def total_fine(days_csv):
    """Sum fines for a CSV of days kept. Invalid/empty entries are skipped;
    non-string input yields 0."""
    if not isinstance(days_csv, str):
        return 0
    fine = 0
    for token in days_csv.split(','):
        token = token.strip()
        if not _DAYS_RE.fullmatch(token):
            continue
        d = int(token)
        if d > MAX_DAYS_ALLOWED:
            fine += (d - MAX_DAYS_ALLOWED) * FINE_PER_DAY
    return fine


def shelf_code(title):
    """Return the uppercase initials of the first two words, or '' if the
    title is not a string or has fewer than two words."""
    if not isinstance(title, str):
        return ""
    words = title.split()
    if len(words) < 2:
        return ""
    return (words[0][0] + words[1][0]).upper()


def main():
    print("==== Running parse_member_id ====")
    user_input = input("Enter a member ID (e.g. STU-1023): ")
    result = parse_member_id(user_input)
    print("Member Type and Number:", result if result else "Invalid member ID")

    print("\n==== Running total_fine ====")
    user_input = input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    result = total_fine(user_input)
    print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    user_input = input("Enter a book title with at least two words: ")
    result = shelf_code(user_input)
    print("Shelf Code:", result if result else "Invalid title (need at least two words)")

if __name__ == "__main__":
    main()
