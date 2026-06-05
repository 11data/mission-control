import os
import time
import requests

HUBSPOT_API_URL = os.environ.get('HUBSPOT_API_URL', 'https://api.hubapi.com')
HUBSPOT_KEY = os.environ.get('HUBSPOT_PRIVATE_APP_KEY')

if not HUBSPOT_KEY:
    # not fatal on import; runner should check and exit early
    HUBSPOT_KEY = None

HEADERS = lambda: {
    'Authorization': f'Bearer {HUBSPOT_KEY}',
    'Content-Type': 'application/json'
}

DEALS_ENDPOINT = f"{HUBSPOT_API_URL}/crm/v3/objects/deals"

def create_deal(payload):
    """Create a deal in HubSpot. Returns the created deal object or raises."""
    if not HUBSPOT_KEY:
        raise RuntimeError('HUBSPOT_PRIVATE_APP_KEY not set')
    r = requests.post(DEALS_ENDPOINT, json=payload, headers=HEADERS(), timeout=30)
    if r.status_code in (200,201):
        return r.json()
    elif r.status_code == 429:
        raise RuntimeError('rate_limited')
    else:
        r.raise_for_status()

# Helper to convert opportunity -> hubspot payload

def opportunity_to_deal_payload(opp):
    properties = {
        'dealname': opp.get('title'),
        'amount': str(opp.get('value') or 0),
        'currency': opp.get('currency') or 'EUR',
        'closedate': None,
        'description': opp.get('notes') or ''
    }
    if opp.get('close_date'):
        # HubSpot expects ms since epoch
        try:
            t = time.mktime(time.strptime(opp['close_date'], '%Y-%m-%d'))
            properties['closedate'] = int(t * 1000)
        except Exception:
            properties['closedate'] = None
    payload = {'properties': {k: v for k,v in properties.items() if v is not None}}
    return payload
