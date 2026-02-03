/**
 * TypeScript type definitions for Agromate API.
 * These interfaces match the API response schemas from the backend.
 */

export interface Article {
    id: string;
    title: string;
    source: string;
    url: string;
    published_at: string | null;
    sentiment: 'ALCISTA' | 'BAJISTA' | 'NEUTRAL' | null;
    confidence: number | null;
    commodity: string;
    created_at: string;
    updated_at: string;
}

export interface NewsListResponse {
    total: number;
    articles: Article[];
}

export interface SentimentStats {
    total: number;
    alcista: number;
    bajista: number;
    neutral: number;
    null: number;
    alcista_percentage: number;
    bajista_percentage: number;
    neutral_percentage: number;
}

export interface PipelineResponse {
    status: string;
    message: string;
}

export interface HealthResponse {
    status: string;
    timestamp: string;
    database: string;
}

export type SentimentType = 'ALCISTA' | 'BAJISTA' | 'NEUTRAL';

export interface FilterState {
    source: string[] | null;  // Cambiado de string a string[]
    sentiment: SentimentType | null;
    commodity: string | null;
    dateFrom: string | null;  // ISO format YYYY-MM-DD
    dateTo: string | null;    // ISO format YYYY-MM-DD
}

export interface SourcesResponse {
    sources: string[];
}
