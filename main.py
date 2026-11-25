"""Absurd Clause Contest — one clause, buried deep in the terms.

The brief: a single original English sentence, at most 200 characters,
phrased as a clause that could sit buried deep inside a terms-of-service
agreement — deadpan legal boilerplate that quietly turns absurd. Entries
are paired against each other and judged from the published brief, so the
line has to survive on its own: no setup, no explanation, one reading.

How the pick is made. Twelve lines were drafted by hand and graded 0–10
on the five things the brief rewards, in brief order: it must read as a
real clause hiding in a ToS; it must be funny on first reading; it must
sound like genuine boilerplate until the absurdity lands; it must be
concrete and original rather than a vague wave at the genre; it must be
tight. Highest total wins; a tie goes to the shorter line, so the result
is the same on every run.

Field screen. The contest already holds 512 entries, and the visible
titles show which devices the field has worn out: carrier pigeons in
several jobs, a monthly live goat, firstborns renamed five times over,
houseplants inheriting estates, trial by combat against a goose, and
addressing the chief executive as "Your Majesty". None of those devices
appears in any candidate below, and the guard in this file refuses any
line that leans on one, so a crowded device cannot slip back in later.

Second draft. The winner first read with "third failed login attempt"
and ended "a handwritten letter expressing mild disappointment". The
revision adds "consecutive" — the word real lockout boilerplate uses,
which makes the legal voice truer — and swaps the ending to "a
handwritten letter of mild disappointment", seven characters shorter and
closer to legal phrasing ("letter of intent", "letter of complaint"),
so the punch stays the last thing the reader meets. The runner-up was
revised the same way: "future company holiday card" became "the
Company's annual holiday card", and "including years in which the User
is deceased" tightened to "including any year in which the User is
deceased".

Code second draft. The first version of the guard only checked length,
blankness, line breaks and crowded devices, and the chooser trusted the
table blindly. The revision adds two real gates: every candidate must
end with a full stop, because a clause that trails off is not a clause,
and no line may appear twice, because a duplicated draft would silently
double-weight one joke. Both gates run before any scoring, so a bad
draft fails here instead of winning by accident.
"""

import hashlib
import sys
from pathlib import Path

CHAR_LIMIT = 200
FORBIDDEN_BITS = ("pigeon", "goat", "firstborn", "houseplant",
                  "your majesty", "trial by combat")
CRITERIA = ("buried clause", "first-read laugh", "boilerplate voice",
            "concrete image", "tightness")
OUT_FILE = Path("/output/entry.txt")

# Each entry: the line, then one mark per criterion in CRITERIA order.
# Totals are summed here, never hard-coded, so a mis-scored line shows
# up as soon as the table is read.
ENTRIES = (
    ("Upon the User's third consecutive failed login attempt, the Service shall lock the account and mail the User a handwritten letter of mild disappointment.", (9, 10, 9, 9, 10)),
    ("The User grants the Company a perpetual, irrevocable licence to use the User's likeness in the Company's annual holiday card, including any year in which the User is deceased.", (10, 8, 10, 9, 9)),
    ("All user data shall be stored on servers located, for tax purposes, inside a single filing cabinet in international waters.", (9, 8, 9, 9, 9)),
    ("The User shall, once per calendar year, present the Company with a satisfactory haiku, failing which the Service may be paused until one is received.", (8, 8, 9, 9, 9)),
    ("Upon termination, the User's remaining account balance shall be converted into confetti and released, without ceremony, over the Company's parking lot.", (8, 8, 8, 10, 8)),
    ("By using the Service, the User consents to being followed, at a respectful distance, by one (1) Company representative at all times.", (8, 8, 9, 8, 9)),
    ("By continuing to use the Service, the User agrees to be buried, upon death, in the Company's branded hoodie, which shall be provided at cost.", (9, 7, 9, 8, 8)),
    ("The Company reserves the right to charge the User's credit card for emotional damages suffered by the Company's servers during peak hours.", (8, 8, 8, 8, 9)),
    ("Any user found to be a robot must, within seven (7) days, provide proof of humanity in the form of a handwritten letter from their mother.", (8, 8, 8, 9, 8)),
    ("In the event of a solar eclipse, the User agrees to hold the Company harmless for any werewolves created, summoned, or otherwise inconvenienced by the Service.", (7, 8, 7, 9, 8)),
    ("The User acknowledges that by reading these Terms in full, the User has waived the right to enjoy parties, weddings, and other gatherings.", (8, 7, 8, 7, 8)),
    ("The User agrees that the Company's terms may be updated at any time, including retroactively, and including this sentence.", (7, 7, 8, 6, 9)),
)


def guard(line):
    """Refuse any line that cannot be the entry, loudly and early."""
    if not line.strip():
        raise ValueError("candidate is blank")
    if len(line) > CHAR_LIMIT:
        raise ValueError(f"candidate is {len(line)} chars, over the {CHAR_LIMIT} limit")
    if "\n" in line or "\r" in line:
        raise ValueError("candidate spans more than one line")
    if not line.endswith("."):
        raise ValueError("a clause must end with a full stop")
    lowered = line.lower()
    for bit in FORBIDDEN_BITS:
        if bit in lowered:
            raise ValueError(f"candidate leans on a crowded device: {bit!r}")


def choose(entries):
    """Highest total wins; ties go to the shorter line."""
    ranked = []
    seen = set()
    for line, marks in entries:
        if line in seen:
            raise ValueError(f"duplicate candidate drafted twice: {line!r}")
        seen.add(line)
        if len(marks) != len(CRITERIA):
            raise ValueError(f"candidate scored on {len(marks)} criteria, need {len(CRITERIA)}: {line!r}")
        guard(line)
        ranked.append((-sum(marks), len(line), line))
    ranked.sort()
    return ranked[0][2]


def emit(line):
    """Write the line as the entry file, then prove the bytes on disk."""
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_bytes(line.encode("utf-8"))
    on_disk = OUT_FILE.read_bytes()
    digest = hashlib.sha256(on_disk).hexdigest()
    payload = line.encode("utf-8")
    wanted = hashlib.sha256(payload).hexdigest()
    if digest != wanted:
        raise ValueError("entry.txt on disk is not the chosen line")
    if not 1 <= len(on_disk.decode("utf-8")) <= CHAR_LIMIT:
        raise ValueError("entry.txt breaks the character gate")
    OUT_FILE.chmod(0o644)
    return digest


def run():
    line = choose(ENTRIES)
    digest = emit(line)
    sys.stdout.write(f"{line}\n")
    print(f"sha256={digest} chars={len(line)}")
    return 0


if __name__ == "__main__": raise SystemExit(run())
