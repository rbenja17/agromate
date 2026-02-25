"use client";

import React, { useState, useEffect } from 'react';
import { fetchMarketHistory } from '@/lib/api';
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

export default function DollarCorrelation() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [period, setPeriod] = useState(30);

    useEffect(() => {
        setLoading(true);
        fetchMarketHistory(period, 'soja')
            .then(res => {
                const filtered = (res.data || []).filter(
                    (d: any) => d.soja_usd || d.dolar_oficial || d.brecha_pct
                );
                setData(filtered);
            })
            .catch(() => { })
            .finally(() => setLoading(false));
    }, [period]);

    return (
        <div className="glass-card rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                    💱 Correlación Dólar / Soja
                </h3>
                <div className="flex gap-2">
                    {[7, 30, 90].map(d => (
                        <button
                            key={d}
                            onClick={() => setPeriod(d)}
                            className={`px-3 py-1 text-sm rounded-full transition-colors ${period === d
                                ? 'bg-amber-500 text-white'
                                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                                }`}
                        >
                            {d}d
                        </button>
                    ))}
                </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Precio Soja (USD/ton) vs Brecha Cambiaria (%)
            </p>

            {loading ? (
                <div className="flex items-center justify-center h-64">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
                </div>
            ) : data.length === 0 ? (
                <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
                    No hay datos disponibles para este período
                </div>
            ) : (
                <ResponsiveContainer width="100%" height={300}>
                    <ComposedChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                        <XAxis
                            dataKey="date"
                            stroke="#9ca3af"
                            tick={{ fill: '#9ca3af' }}
                            tickFormatter={(date) => {
                                try {
                                    return format(parseISO(date), 'dd/MM', { locale: es });
                                } catch { return date; }
                            }}
                        />
                        <YAxis
                            yAxisId="left"
                            stroke="#22c55e"
                            tick={{ fill: '#22c55e' }}
                            label={{ value: 'USD/ton', angle: -90, position: 'insideLeft', fill: '#22c55e' }}
                        />
                        <YAxis
                            yAxisId="right"
                            orientation="right"
                            stroke="#f59e0b"
                            tick={{ fill: '#f59e0b' }}
                            label={{ value: 'Brecha %', angle: 90, position: 'insideRight', fill: '#f59e0b' }}
                        />
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
                        <Line
                            yAxisId="left"
                            type="monotone"
                            dataKey="soja_usd"
                            stroke="#22c55e"
                            name="Soja (USD/ton)"
                            strokeWidth={2}
                            dot={false}
                            connectNulls
                        />
                        <Bar
                            yAxisId="right"
                            dataKey="brecha_pct"
                            fill="#f59e0b"
                            name="Brecha Cambiaria (%)"
                            opacity={0.5}
                        />
                    </ComposedChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}
