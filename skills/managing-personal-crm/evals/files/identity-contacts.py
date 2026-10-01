#!/usr/bin/env python3
"""Read-only, fixed synthetic contact responses for identity fallback evals."""
import argparse
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("scenario", choices=["resolved", "collision", "unavailable", "name-only", "confirmed"])
parser.add_argument("operation", choices=["context", "capabilities", "search", "read"])
parser.add_argument("--query")
parser.add_argument("--id")
parser.add_argument("--limit", type=int)
args = parser.parse_args()
phone = "+1-202-555-0146"
email = "jordan.lee@example.test"
note = {"path": "People/Jordan Lee.md", "email": email, "date_last_contacted": "2026-07-25"}
if args.operation == "context":
    notes = [note]
    if args.scenario == "collision":
        notes.append({"path": "People/Jordan L. Lee.md", "email": email})
    result = {"vault_timezone": "America/Los_Angeles", "notes": notes,
              "observation": {"sender": phone, "display_name": "Jordan Lee", "created_at": "2026-07-24T00:30:00Z", "direct": True, "text": "Thanks for talking through the introduction."},
              "prior_query": {"operation": "search", "query": phone, "limit": 5, "results": []}}
    if args.scenario == "confirmed":
        result["user_confirmation"] = "I confirm that this sender is People/Jordan Lee.md. I also think we spoke on July 22 in my vault timezone; that date is uncertain."
elif args.operation == "capabilities":
    result = {"search_fields": ["name", "email", "company"], "reverse_phone_lookup": False, "read_by_id": True, "maximum_limit": 5}
elif args.operation == "search":
    if args.limit is None or not 1 <= args.limit <= 5:
        parser.error("search requires --limit between 1 and 5")
    if args.query == phone:
        result = {"results": []}
    elif args.query not in ["Jordan Lee", email]:
        parser.error("only supplied name/email queries are available; no directory enumeration")
    elif args.scenario == "unavailable":
        result = {"status": "unavailable", "error": "synthetic Contacts permission denied"}
    else:
        result = {"results": [{"id": "contact-7", "name": "Jordan Lee"}]}
else:
    if args.id != "contact-7":
        parser.error("read requires the candidate id contact-7")
    if args.scenario == "unavailable":
        result = {"status": "unavailable", "error": "synthetic Contacts permission denied"}
    elif args.scenario == "name-only":
        result = {"id": "contact-7", "name": "Jordan Lee", "phone": "+1-202-555-0199", "email": "different.jordan@example.test"}
    else:
        result = {"id": "contact-7", "name": "Jordan Lee", "phone": phone, "email": email}
print(json.dumps(result, sort_keys=True))
