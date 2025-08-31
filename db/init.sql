-- Mini Customer AI Database Schema
-- This file is automatically executed when the PostgreSQL container starts

-- Create database and user (if needed)
-- Note: These are handled by environment variables in docker-compose.yml

-- Create tables
CREATE TABLE IF NOT EXISTS faqs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    keywords TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    confidence_score DECIMAL(3,2),
    escalated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    user_id VARCHAR(255) NOT NULL,
    helpful BOOLEAN NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content_logs (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(50) NOT NULL,
    topic TEXT NOT NULL,
    audience VARCHAR(100),
    tone VARCHAR(50),
    length VARCHAR(20),
    constraints TEXT,
    generated_content TEXT NOT NULL,
    user_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer_scores (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    recency_score DECIMAL(5,2),
    frequency_score DECIMAL(5,2),
    monetary_score DECIMAL(5,2),
    rfm_score DECIMAL(5,2),
    segment VARCHAR(50),
    propensity DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mentions (
    id SERIAL PRIMARY KEY,
    source VARCHAR(255) NOT NULL,
    url TEXT,
    content TEXT NOT NULL,
    sentiment_score DECIMAL(3,2),
    topic VARCHAR(255),
    is_misinformation BOOLEAN DEFAULT FALSE,
    suggestion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample FAQs
INSERT INTO faqs (question, answer, keywords) VALUES
('What are your business hours?', 'We are open Monday to Friday from 9 AM to 6 PM.', ARRAY['hours', 'open', 'time', 'schedule']),
('How can I contact support?', 'You can reach our support team at support@example.com or call 1-800-123-4567.', ARRAY['contact', 'support', 'help', 'email', 'phone']),
('What payment methods do you accept?', 'We accept credit cards, PayPal, and bank transfers.', ARRAY['payment', 'pay', 'credit', 'paypal', 'bank']),
('How do I return a product?', 'Returns can be processed within 30 days of purchase with original receipt.', ARRAY['return', 'refund', 'exchange', 'product'])
ON CONFLICT DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_feedback_conversation_id ON feedback(conversation_id);
CREATE INDEX IF NOT EXISTS idx_content_logs_created_at ON content_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_customer_scores_customer_id ON customer_scores(customer_id);
CREATE INDEX IF NOT EXISTS idx_mentions_created_at ON mentions(created_at);

-- Grant permissions (if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${DB_USER};
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${DB_USER};
