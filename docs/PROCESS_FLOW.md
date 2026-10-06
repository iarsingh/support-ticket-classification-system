# Support Ticket Classification System: process flows

## Domain request

Endpoint: `POST /classify`. Input: ticket text. The processing stages below summarize [classify.py](../src/tickets/classify.py); they are local function behavior, not externally executed tools.

```mermaid
flowchart TD
  A["POST /classify"] --> B{"Non-empty string text?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes"| T["Extract lowercase alphanumeric tokens"]
  T --> C["Count billing, access, and outage keyword occurrences"]
  C --> D{"All counts zero?"}
  D -->|"Yes"| U["Label unknown"]
  D -->|"No"| L["Highest count; lexical label breaks ties"]
  U --> O["Return label, matched evidence, and review signals"]
  L --> O
```

Refusal responses, where implemented, are normal domain results rather than successful execution of a requested write. Detailed edge cases are covered in [INTERVIEW_QA.md](../INTERVIEW_QA.md).

## Workspace and job approval

```mermaid
flowchart TD
  C["Create tenant-scoped workspace"] --> J["Submit job: workspace + payload + target"]
  J --> V{"Workspace belongs to selected tenant?"}
  V -->|"No"| E["HTTP 404"]
  V -->|"Yes"| P{"Normalized target is prod or production?"}
  P -->|"Yes"| Q["pending_approval"]
  P -->|"No"| L["queued"]
  Q --> A["Approval request"]
  A --> X["HTTP 403: production apply disabled"]
  L --> B["Approval request"]
  B --> K["approved: status update only"]
  K --> S["No executor / no production apply"]
```

Approval first checks job ownership using the selected tenant. Status changes and audit records remain in memory. Repeated lab approval returns the original approval without duplicating its event or counter. Ops transitions are protected by an in-process lock. The domain request flow and this job-record flow are independent. Source: [ops.py](../src/tickets/ops.py).
