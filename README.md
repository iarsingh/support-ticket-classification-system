# Support Ticket Classification System

Level: 3 — Machine Learning

Skills: Python, a lexicon, empty refusal

Label a ticket as billing, access, or outage from a lexicon.

```bash
pip install -r requirements.txt
pytest -q
```

This is a local laptop proof. It does not call a hosted model and it does not apply production changes.

## Ops plane

Workspaces, tenant isolation, job approval, and audit live under `/v1`. Production apply is refused. See `docs/ARCHITECTURE.md`.

## Project documentation

- [Project architecture and component diagram](PROJECT_ARCHITECTURE.md)
- [Domain request and job approval flows](docs/PROCESS_FLOW.md)
- [Project-specific interview questions and answers](INTERVIEW_QA.md)
