def test_opportunity_to_deal_payload():
    from integrations.hubspot.export import opportunity_to_deal_payload
    opp = { 'title': 'X', 'value': 1000, 'currency': 'EUR', 'close_date': '2026-07-01', 'notes': 'note' }
    p = opportunity_to_deal_payload(opp)
    assert 'properties' in p
    assert p['properties'].get('dealname') == 'X'
