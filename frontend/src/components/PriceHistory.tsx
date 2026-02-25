"use client";

import React, { useState, useEffect } from 'react';
import { fetchMarketHistory } from '@/lib/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

const COMMODITY_COLORS: Record<string, string> = {
    soja_usd: '#22c55e',
    maiz_usd: '#eab308',
    trigo_usd: '#3b82f6',
};

const COMMODITY_LABELS: Record<string, string> = {
    soja_usd: 'Soja',
    maiz_usd: 'Maíz',
    trigo_usd: 'Trigo',
};

export default function PriceHistory() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [period, setPeriod] = useState(30);
    const [error, setError] = useState(false);

    useEffect(() => {
        setLoading(true);
        fetchMarketHistory(period)
            .then(res => setData(res.data || []))
            .catch(() => setError(true))
            .finally(() => setLoading(false));
    }, [period]);

    if (error) return null;

    return (
        <div className="glass-card rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                    📈 Precios Históricos (USD/ton)
                </h3>
                <div className="flex gap-2">
                    {[7, 30, 90].map(d => (
                        <button
                            key={d}
                            onClick={() => setPeriod(d)}
                            className={`px-3 py-1 text-sm rounded-full transition-colors ${period === d
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                                }`}
                        >
                            {d}d
                        </button>
                    ))}
                </div>
            </div>

            {loading ? (
                <div className="flex items-center justify-center h-64">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
            ) : data.length === 0 ? (
                <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
                    No hay datos históricos disponibles
                </div>
            ) : (
                <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis
                            dataKey="date"
                            stroke="#6b7280"
                            tick={{ fill: '#4b5563' }}
                            tickFormatter={(date) => {
                                try {
                                    return format(parseISO(date), 'dd/MM', { locale: es });
                                } catch { return date; }
                            }}
                        />
                        <YAxis stroke="#6b7280" tick={{ fill: '#4b5563' }} />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#1f2937',
                                border: '1px solid #374151',
                                borderRadius: '8px',
                                color: '#fff'
                            }}
                            labelFormatter={(date) => {
                                try {
                                    return format(parseISO(date as string), "dd 'de' MMMM", { locale: es });
                                } catch { return date as string; }
                            }}
                        />
                        <Legend />
                        {Object.entries(COMMODITY_COLORS).map(([key, color]) => (
                            <Line
                                key={key}
                                type="monotone"
                                dataKey={key}
                                stroke={color}
                                name={COMMODITY_LABELS[key]}
                                strokeWidth={2}
                                dot={false}
                                connectNulls
                            />
                        ))}
                    </LineChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}
