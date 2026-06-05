-- Migration: create opportunities and opportunity_tasks tables

CREATE TABLE IF NOT EXISTS opportunities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  company TEXT,
  contact_id UUID,
  owner TEXT,
  value NUMERIC,
  currency TEXT DEFAULT 'EUR',
  stage TEXT DEFAULT 'lead',
  status TEXT DEFAULT 'open',
  close_date DATE,
  source TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS opportunity_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
  task_id UUID NOT NULL,
  role TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_opportunities_owner ON opportunities(owner);
CREATE INDEX IF NOT EXISTS idx_opportunities_stage ON opportunities(stage);
CREATE INDEX IF NOT EXISTS idx_opportunity_tasks_opp ON opportunity_tasks(opportunity_id);
