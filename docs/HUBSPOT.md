# HubSpot Integration — Docs (MVP)

Goal
- MVP: one‑way export of closed_won opportunities → HubSpot Deals (server → HubSpot).
- Phase 2: add webhooks & two‑way sync, contact mapping, association sync.

Security & auth
- Use HubSpot Private App (recommended) or OAuth if multi-user.
- Required secret (store in vault / env): HUBSPOT_PRIVATE_APP_KEY (starts with `pat-`)
- Required scopes for MVP: crm.objects.deals.write, crm.objects.contacts.read, webhooks

Mapping (MVP)
- Local opportunity -> HubSpot deal fields
  - title -> dealname
  - company -> associations.company (optional)
  - owner -> hubspot owner id mapping (map in config)
  - value -> amount (HubSpot expects a number)
  - currency -> deal currency
  - close_date -> closedate (ms since epoch)
  - notes -> description

Rate limits & retry
- HubSpot enforces per‑app rate limits. Implement client with:
  - exponential backoff on 429/5xx
  - jittered sleep
  - configurable concurrency (default 1-2 parallel requests)
- Use the Limits Tracking API in Phase 2 for monitoring.

Resiliency & idempotency
- Store hubspot_deal_id on opportunities after successful export (DB column added by migration).
- On failure, record hubspot_error and retry later.
- Use unique externalId or dedupe by checking for existing deals by external id (optional).

Operational
- Runner: `integrations/hubspot/export_runner.py` (CLI), scheduled via cron or systemd timer.
- Schedule: every 5 minutes to start, adjust once stable.

Acceptance criteria
- Closed_won opportunities are exported to HubSpot within 5–15 minutes of reaching stage.
- Exported opportunities have hubspot_deal_id set and no repeated duplicates.
- Export job logs successes/failures and pushes errors to alerting (Slack/email) if failure rate > 5% in 1h.

Environment variables
- HUBSPOT_PRIVATE_APP_KEY (required)
- HUBSPOT_API_URL (optional, default https://api.hubapi.com)
- HUBSPOT_OWNER_MAP (optional JSON mapping local_owner -> hubspot_owner_id)

Files added
- `migrations/20260605_add_hubspot_fields.sql` — adds hubspot_deal_id/hubspot_exported_at/hubspot_error
- `integrations/hubspot/export.py` — client helper functions
- `integrations/hubspot/export_runner.py` — runner CLI to export closed_won opportunities
- `tests/integrations/test_hubspot_export.py` — test skeleton

Notes
- This integration does not include sending secrets. Add HUBSPOT_PRIVATE_APP_KEY to vault and set appropriate ACLs.
- For Phase 2, add webhook receiver to process HubSpot events and reconcile state.
