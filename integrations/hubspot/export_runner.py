#!/usr/bin/env python3
import os
import time
import requests
import json
from integrations.hubspot.export import opportunity_to_deal_payload, create_deal

API_BASE = os.environ.get('MISSION_CONTROL_API', 'http://guenther.tail360cf1.ts.net:8090')

# Simple exponential backoff
def backoff_sleep(attempt):
    time.sleep(min(60, (2 ** attempt) + (0.1 * attempt)))


def get_closed_won_opportunities():
    r = requests.get(f"{API_BASE}/opportunities")
    if r.status_code != 200:
        raise RuntimeError('failed to fetch opportunities')
    data = r.json()
    return [o for o in data if o.get('stage') == 'closed_won' and not o.get('hubspot_deal_id')]


def mark_exported(opportunity_id, hubspot_id):
    payload = { 'hubspot_deal_id': hubspot_id, 'hubspot_exported_at': time.strftime('%Y-%m-%dT%H:%M:%SZ') }
    requests.patch(f"{API_BASE}/opportunities/{opportunity_id}", json=payload)


def mark_error(opportunity_id, error_text):
    payload = { 'hubspot_error': error_text }
    requests.patch(f"{API_BASE}/opportunities/{opportunity_id}", json=payload)


def run_once():
    items = get_closed_won_opportunities()
    if not items:
        print('No closed_won opportunities to export')
        return
    for o in items:
        attempt = 0
        while attempt < 5:
            try:
                payload = opportunity_to_deal_payload(o)
                created = create_deal(payload)
                hubspot_id = created.get('id')
                mark_exported(o['id'], hubspot_id)
                print(f"Exported opportunity {o['id']} -> hubspot {hubspot_id}")
                break
            except RuntimeError as e:\n                err = str(e)\n                if 'rate_limited' in err:
                    attempt += 1
                    backoff_sleep(attempt)
                    continue
                else:
                    mark_error(o['id'], err)
                    print(f"Failed export {o['id']}: {err}")
                    break
            except Exception as e:\n                mark_error(o['id'], str(e))\n                print(f"Unexpected error exporting {o['id']}: {e}")
                break


if __name__ == '__main__':
    run_once()
