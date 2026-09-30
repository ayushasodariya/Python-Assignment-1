import re

b = int(input())
banned = [input().strip().lower() for _ in range(b)]

n = int(input())

for i in range(1, n + 1):
    password = input().strip()

    if len(password) < 6 or len(password) > 12:
        print(f"{i}: WEAK_LENGTH")
        continue

    if not (re.search(r"[a-z]", password) and
            re.search(r"[A-Z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[$#@]", password)):
        print(f"{i}: WEAK_PATTERN")
        continue

    if any(word in password.lower() for word in banned):
        print(f"{i}: COMPROMISED")
        continue

    if re.search(r"(.)\1{3,}", password):
        print(f"{i}: WEAK_PATTERN")
        continue

    print(f"{i}: STRONG")