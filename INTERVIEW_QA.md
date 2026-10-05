# Support Ticket Classification System: interview questions and answers

Answers describe this repository's current implementation. Suggested production changes are explicitly labeled as future work.

## 1. Is this a trained classifier?

No. It uses three fixed keyword sets for billing, access, and outage. There is no training pipeline, fitted model, probability calibration, or hosted inference call.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 2. How is text tokenized?

The regular expression `[a-z0-9]+` extracts lowercase alphanumeric tokens. Punctuation is discarded, and a token such as `500s` is distinct from the configured keyword `500`.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 3. How are label scores calculated?

Each token occurrence matching a label keyword contributes one count. Repeating the same word therefore increases that label count; this is not a set of unique matches or a confidence probability.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 4. How are tied labels resolved?

`max` compares `(counts[name], name)`. For equal counts the lexicographically greatest label wins. For example, one billing hit and one outage hit yields outage.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 5. When is unknown returned?

If all three counts are zero, the label is replaced with `unknown`. An empty input is different: it raises `InputError` and the handler returns 422.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 6. What does the response explain?

It contains the chosen label, all category counts, and the total token count. These values show the keyword evidence but do not establish that the routing decision is correct.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 7. What case would you use in a demo?

`Cannot login with SSO` returns access because both `login` and `sso` match. `The API is down with 500s` still returns outage because `down` matches even though `500s` does not match `500`.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 8. How would you improve this baseline?

Create a labeled evaluation set, measure per-category precision and recall, review unknown and tied cases, and compare improvements with the baseline. Keep human review available for uncertain routing.

Source: [src/tickets/classify.py](src/tickets/classify.py).

## 9. How are the domain API and ops plane connected?

The app registers the ops router under `/v1`, alongside the domain endpoint. Creating or approving a job updates ops records; it does not call the domain function. There is no background worker or job executor.

Source: [src/tickets/main.py](src/tickets/main.py).

## 10. Does X-Tenant-Id authenticate a user?

No. It is a caller-supplied header defaulting to `default`. Workspace and job reads filter by that value, but a caller can choose another value. Real identity and authorization would need to precede this lab tenant selector.

Source: [src/tickets/ops.py](src/tickets/ops.py).

## 11. What survives a process restart?

Nothing in the ops dictionaries or audit list is persisted. Multiple server workers would also have separate state. Durable storage, transactions, and a shared job queue are future changes.

Source: [src/tickets/ops.py](src/tickets/ops.py).

## 12. What happens when a production job is approved?

Targets exactly equal to `prod` or `production` create a `pending_approval` job and approval returns HTTP 403. Other target strings are queued. Approval of a lab job changes its status only; it does not execute a workload.

Source: [src/tickets/ops.py](src/tickets/ops.py).

## 13. Are audit and metrics equally tenant-scoped?

Audit results filter events by the tenant and its workspace/job identifiers. `/v1/metrics` returns process-wide counters without tenant filtering, so it is not a tenant-specific dashboard. Domain requests are not automatically audited.

Source: [src/tickets/ops.py](src/tickets/ops.py).

## 14. What would you prioritize before a customer deployment?

Define authenticated identities and permission checks, durable state, typed domain inputs, bounded requests, concurrency behavior, and observable execution semantics. Use the existing tests as a baseline, then test failure and access boundaries rather than claiming the lab is production-ready.

Source: [src/tickets/ops.py](src/tickets/ops.py).
