CREATE TABLE IF NOT EXISTS emails (
  id VARCHAR PRIMARY KEY,
  message_id VARCHAR NULL,
  from_email VARCHAR NOT NULL,
  from_name VARCHAR NULL,
  subject VARCHAR NOT NULL,
  body TEXT NOT NULL,
  received_at TIMESTAMP NOT NULL,
  status VARCHAR NOT NULL,
  ticket_id VARCHAR NULL,
  processing_time_ms INTEGER NULL,
  ai_analysis JSON NULL,
  transport_mode VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS knowledge_base (
  id VARCHAR PRIMARY KEY,
  category VARCHAR NOT NULL,
  intent VARCHAR NOT NULL,
  keywords JSON NOT NULL,
  problem_summary TEXT NOT NULL,
  solution_template TEXT NOT NULL,
  variables_used JSON NOT NULL,
  confidence_threshold INTEGER NOT NULL,
  use_count INTEGER NOT NULL,
  success_rate FLOAT NOT NULL,
  last_updated TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS auto_replies (
  id VARCHAR PRIMARY KEY,
  email_id VARCHAR NOT NULL,
  kb_id VARCHAR NULL,
  generated_reply TEXT NOT NULL,
  ai_confidence INTEGER NOT NULL,
  match_method VARCHAR NOT NULL,
  sent_at TIMESTAMP NOT NULL,
  delivery_status VARCHAR NOT NULL,
  delivery_method VARCHAR(20) DEFAULT 'simulator',
  real_delivered BOOLEAN DEFAULT FALSE,
  delivery_error TEXT NULL,
  model_used VARCHAR NOT NULL,
  tokens_used INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
  id VARCHAR PRIMARY KEY,
  ticket_number VARCHAR UNIQUE NOT NULL,
  email_id VARCHAR NOT NULL,
  category VARCHAR NULL,
  status VARCHAR NOT NULL,
  auto_resolved BOOLEAN NOT NULL,
  escalated_reason TEXT NULL
);

CREATE TABLE IF NOT EXISTS system_config (
  id VARCHAR PRIMARY KEY,
  company_name VARCHAR NOT NULL,
  support_email VARCHAR NOT NULL,
  gmail_connected BOOLEAN NOT NULL,
  auto_reply_enabled BOOLEAN NOT NULL,
  confidence_threshold INTEGER NOT NULL,
  signature_template TEXT NOT NULL,
  logo_url VARCHAR NOT NULL,
  email_poll_interval_seconds INTEGER NOT NULL
);
