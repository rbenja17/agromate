/**
 * API client for Agromate backend.
 * All functions use native fetch to communicate with the FastAPI backend.
 */

import { NewsListResponse, SentimentStats, PipelineResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Fetch news articles from the API with optional filters.
 * 
 * @param limit - Maximum number of articles to fetch (default: 50)
 * @param filters - Optional filter parameters
 * @returns Promise with news list response
 */
export async function fetchNews(
    limit: number = 50,
    filters?: {
        sentiment?: string;
        source?: string;
        dateFrom?: string;
        dateTo?: string;
    }
): Promise<NewsListResponse> {
    try {
        const params = new URLSearchParams({
            limit: limit.toString(),
        });

        if (filters?.sentiment) {
            params.append('sentiment', filters.sentiment);
        }
        if (filters?.source) {
            params.append('source', filters.source);
        }
        if (filters?.dateFrom) {
            params.append('date_from', filters.dateFrom);
        }
        if (filters?.dateTo) {
            params.append('date_to', filters.dateTo);
        }

        const response = await fetch(`${API_BASE_URL}/api/news?${params}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: NewsListResponse = await response.json();
        return data;

    } catch (error) {
        console.error('Error fetching news:', error);
        throw new Error('Failed to fetch news. Make sure the backend is running on port 8000.');
    }
}

/**
 * Fetch sentiment statistics from the API.
 * 
 * @returns Promise with sentiment statistics
 */
export async function fetchStats(): Promise<SentimentStats> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/stats`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: SentimentStats = await response.json();
        return data;

    } catch (error) {
        console.error('Error fetching stats:', error);
        throw new Error('Failed to fetch statistics. Make sure the backend is running on port 8000.');
    }
}

/**
 * Trigger the pipeline to scrape and analyze new articles.
 * 
 * @returns Promise with pipeline response
 */
export async function triggerPipeline(): Promise<PipelineResponse> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/pipeline/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: PipelineResponse = await response.json();
        return data;

    } catch (error) {
        console.error('Error triggering pipeline:', error);
        throw new Error('Failed to trigger pipeline. Make sure the backend is running on port 8000.');
    }
}

/**
 * Fetch recent news from the last N hours.
 * 
 * @param hours - Number of hours to look back (default: 24)
 * @returns Promise with news list response
 */
export async function fetchRecentNews(hours: number = 24): Promise<NewsListResponse> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/recent?hours=${hours}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: NewsListResponse = await response.json();
        return data;

    } catch (error) {
        console.error('Error fetching recent news:', error);
        throw new Error('Failed to fetch recent news. Make sure the backend is running on port 8000.');
    }
}

/**
 * Fetch daily sentiment trends.
 * 
 * @param days - Number of days to look back (default: 7)
 * @param filters - Optional filters to apply
 * @returns Promise with daily trend data
 */
export async function fetchDailyTrends(
    days: number = 7,
    filters?: {
        sentiment?: string;
        source?: string;
        dateFrom?: string;
        dateTo?: string;
    }
) {
    try {
        const params = new URLSearchParams();
        params.append('days', days.toString());

        if (filters?.sentiment) {
            params.append('sentiment', filters.sentiment);
        }
        if (filters?.source) {
            params.append('source', filters.source);
        }
        if (filters?.dateFrom) {
            params.append('date_from', filters.dateFrom);
        }
        if (filters?.dateTo) {
            params.append('date_to', filters.dateTo);
        }

        const response = await fetch(`${API_BASE_URL}/api/trends/daily?${params.toString()}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error('Error fetching daily trends:', error);
        throw new Error('Failed to fetch daily trends.');
    }
}

/**
 * Fetch sentiment distribution by source.
 * 
 * @param filters - Optional filters to apply
 * @returns Promise with source distribution data
 */
export async function fetchSourceTrends(
    filters?: {
        sentiment?: string;
        source?: string;
        dateFrom?: string;
        dateTo?: string;
    }
) {
    try {
        const params = new URLSearchParams();

        if (filters?.sentiment) {
            params.append('sentiment', filters.sentiment);
        }
        if (filters?.source) {
            params.append('source', filters.source);
        }
        if (filters?.dateFrom) {
            params.append('date_from', filters.dateFrom);
        }
        if (filters?.dateTo) {
            params.append('date_to', filters.dateTo);
        }

        const queryString = params.toString();
        const url = queryString ? `${API_BASE_URL}/api/trends/by-source?${queryString}` : `${API_BASE_URL}/api/trends/by-source`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error('Error fetching source trends:', error);
        throw new Error('Failed to fetch source trends.');
    }
}

/**
 * Fetch sentiment score timeline.
 * 
 * @param days - Number of days to look back (default: 7)
 * @param filters - Optional filters to apply
 * @returns Promise with timeline data
 */
export async function fetchSentimentTimeline(
    days: number = 7,
    filters?: {
        sentiment?: string;
        source?: string;
        dateFrom?: string;
        dateTo?: string;
    }
) {
    try {
        const params = new URLSearchParams();
        params.append('days', days.toString());

        if (filters?.sentiment) {
            params.append('sentiment', filters.sentiment);
        }
        if (filters?.source) {
            params.append('source', filters.source);
        }
        if (filters?.dateFrom) {
            params.append('date_from', filters.dateFrom);
        }
        if (filters?.dateTo) {
            params.append('date_to', filters.dateTo);
        }

        const response = await fetch(`${API_BASE_URL}/api/trends/timeline?${params.toString()}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error('Error fetching sentiment timeline:', error);
        throw new Error('Failed to fetch sentiment timeline.');
    }
}

/**
 * Fetch available news sources.
 * 
 * @returns Promise with list of source names
 */
export async function fetchSources(): Promise<string[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/sources`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.sources;

    } catch (error) {
        console.error('Error fetching sources:', error);
        return [];
    }
}
