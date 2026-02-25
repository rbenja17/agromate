"use client";

import React, { useState, useEffect } from 'react';
import { fetchDailySummary } from '@/lib/api';

interface DailySummaryData {
    summary: string;
    sentiment_score: number;
    stats: { alcista: number; bajista: number; neutral: number; total: number };
    top_commodities?: Record<string, number>;
    generated_at: string;
}

export default function DailySummary() {
    const [data, setData] = useState<DailySummaryData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        fetchDailySummary()
            .then(setData)
            .catch(() => setError(true))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 border border-gray-200 dark:border-gray-700 animate-pulse">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-4"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
            </div>
        );
    }

    if (error || !data) return null;

    const getEmoji = (score: number) => {
        if (score > 0.3) return '🟢';
        if (score < -0.3) return '🔴';
        return '⚪';
    };

    const getMood = (score: number) => {
        if (score > 0.3) return 'Alcista';
        if (score < -0.3) return 'Bajista';
        return 'Mixto';
    };

    const moodColor = data.sentiment_score > 0.3
        ? 'border-green-400 bg-green-50 dark:bg-green-900/20'
        : data.sentiment_score < -0.3
            ? 'border-red-400 bg-red-50 dark:bg-red-900/20'
            : 'border-gray-300 bg-gray-50 dark:bg-gray-800';

    return (
        <div className={`rounded-lg shadow-md p-6 mb-6 border-l-4 ${moodColor}`}>
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                    {getEmoji(data.sentiment_score)} Resumen del Mercado
                    <span className="text-sm font-normal text-gray-500 dark:text-gray-400">
                        — Ánimo: {getMood(data.sentiment_score)} ({data.sentiment_score > 0 ? '+' : ''}{data.sentiment_score.toFixed(2)})
                    </span>
                </h3>
            </div>

            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                {data.summary}
            </p>

            {data.top_commodities && Object.keys(data.top_commodities).length > 0 && (
                <div className="mt-3 flex gap-2 flex-wrap">
                    {Object.entries(data.top_commodities).map(([commodity, count]) => (
                        <span key={commodity} className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300">
                            {commodity}: {count} noticias
                        </span>
                    ))}
                </div>
            )}
        </div>
    );
}
