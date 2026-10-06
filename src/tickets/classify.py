import re

BILLING = {"invoice", "charge", "refund"}
ACCESS = {"login", "password", "sso"}
OUTAGE = {"down", "outage", "500"}


class InputError(ValueError):
    pass


def classify(text):
    if not isinstance(text, str) or not text.strip() or len(text) > 10000:
        raise InputError("Text must contain 1 to 10000 characters.")
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    counts = {}
    counts['billing'] = sum(token in BILLING for token in tokens)
    counts['access'] = sum(token in ACCESS for token in tokens)
    counts['outage'] = sum(token in OUTAGE for token in tokens)
    label = max(counts, key=lambda name: (counts[name], name))
    if all(value == 0 for value in counts.values()):
        label = "unknown"
    best = max(counts.values())
    tied = sorted(name for name, count in counts.items() if count == best) if best else []
    evidence = {name: sorted(set(tokens) & keywords) for name, keywords in
                [("billing", BILLING), ("access", ACCESS), ("outage", OUTAGE)]}
    return {"label": label, "counts": counts, "tokens": len(tokens), "matched_keywords": evidence,
            "needs_review": best == 0 or len(tied) > 1, "tied_labels": tied,
            "review_reason": "no keyword evidence" if best == 0 else "tied categories" if len(tied) > 1 else None}
