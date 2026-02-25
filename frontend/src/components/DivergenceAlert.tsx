"use client";

import React, { useState, useEffect } from 'react';
import { fetchDivergence } from '@/lib/api';

interface DivergenceData {
    divergence_type: string;
    commodity: string;
    sentiment_score: number;
    price_change_pct: number;
    signal_strength: number;
    news_count: number;
    description: string;
}

export default function DivergenceAlert() {
    const [alerts, setAlerts] = useState<DivergenceData[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const commodities = ['soja', 'maiz', 'trigo'];

        Promise.all(commodities.map(c => fetchDivergence(c, 7)))
            .then(results => {
                const divergences = results.filter(
                    (r): r is DivergenceData =>
                        r !== null &&
                        (r.divergence_type === 'BULLISH_DIVERGENCE' || r.divergence_type === 'BEARISH_DIVERGENCE')
                );
                setAlerts(divergences);
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading || alerts.length === 0) return null;

    return (
        <div className="mb-6 space-y-3">
            {alerts.map((alert, idx) => {
                const isBullish = alert.divergence_type === 'BULLISH_DIVERGENCE';
                const bgColor = isBullish
                    ? 'bg-amber-50 border-amber-400 dark:bg-amber-900/20 dark:border-amber-600'
                    : 'bg-purple-50 border-purple-400 dark:bg-purple-900/20 dark:border-purple-600';
                const textColor = isBullish
                    ? 'text-amber-800 dark:text-amber-300'
                    : 'text-purple-800 dark:text-purple-300';

                return (
                    <div key={idx} className={`rounded-lg p-4 border-l-4 ${bgColor}`}>
                        <div className="flex items-start gap-3">
                            <span className="text-2xl flex-shrink-0">
                                {isBullish ? '⚠️' : '🔮'}
                            </span>
                            <div>
                                <h4 className={`font-bold ${textColor}`}>
                                    {isBullish ? 'Divergencia Alcista' : 'Divergencia Bajista'} — {alert.commodity}
                                </h4>
                                <p className={`text-sm mt-1 ${textColor} opacity-90`}>
                                    {alert.description}
                                </p>
                                <div className="flex gap-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                                    <span>Sentimiento: {alert.sentiment_score > 0 ? '+' : ''}{alert.sentiment_score.toFixed(2)}</span>
                                    <span>Precio: {alert.price_change_pct > 0 ? '+' : ''}{alert.price_change_pct.toFixed(1)}%</span>
                                    <span>Señal: {'🔥'.repeat(alert.signal_strength)}</span>
                                    <span>{alert.news_count} noticias</span>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
