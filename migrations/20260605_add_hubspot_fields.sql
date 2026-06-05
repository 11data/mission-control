-- Migration: add HubSpot fields to opportunities

ALTER TABLE opportunities
  ADD COLUMN IF NOT EXISTS hubspot_deal_id TEXT,
  ADD COLUMN IF NOT EXISTS hubspot_exported_at TIMESTAMP WITH TIME ZONE,
  ADD COLUMN IF NOT EXISTS hubspot_error TEXT;

CREATE INDEX IF NOT EXISTS idx_opportunities_hubspot_deal_id ON opportunities(hubspot_deal_id);
