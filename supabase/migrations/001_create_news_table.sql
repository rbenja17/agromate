-- Agromate Database Schema
-- Migration: 001_create_news_table.sql

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create news table
CREATE TABLE IF NOT EXISTS news (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    source VARCHAR(100) NOT NULL,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMPTZ,
    
    -- Sentiment analysis fields
    sentiment VARCHAR(20),  -- 'ALCISTA', 'BAJISTA', 'NEUTRAL'
    confidence DECIMAL(4,2), -- 0.00 - 1.00
    
    -- Metadata
    commodity VARCHAR(50) DEFAULT 'SOJA',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_news_published_at ON news(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_sentiment ON news(sentiment);
CREATE INDEX IF NOT EXISTS idx_news_source ON news(source);
CREATE INDEX IF NOT EXISTS idx_news_commodity ON news(commodity);
CREATE INDEX IF NOT EXISTS idx_news_created_at ON news(created_at DESC);

-- Create unique index on URL to prevent duplicates
CREATE UNIQUE INDEX IF NOT EXISTS idx_news_url_unique ON news(url);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at
DROP TRIGGER IF EXISTS update_news_updated_at ON news;
CREATE TRIGGER update_news_updated_at
    BEFORE UPDATE ON news
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE news IS 'Agricultural news articles with sentiment analysis';
COMMENT ON COLUMN news.sentiment IS 'Market sentiment: ALCISTA (bullish), BAJISTA (bearish), NEUTRAL';
COMMENT ON COLUMN news.confidence IS 'Confidence score of sentiment analysis (0.00-1.00)';
COMMENT ON COLUMN news.commodity IS 'Related commodity (default: SOJA/Soybean)';
