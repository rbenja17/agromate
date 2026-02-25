"use client";

import React, { useState, useEffect } from 'react';
import { fetchMarketHistory } from '@/lib/api';
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

export default function DollarCorrelation() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMarketHistory(30, 'soja')
            .then(res => {
                // Ensure we have dollar data for the chart
                const filtered = (res.data || []).filter(
                    (d: any) => d.soja_usd || d.dolar_oficial || d.brecha_pct
                );
                setData(filtered);
            })
            .catch(() => { })
            .finally(() => setLoading(false));
    }, []);

    if (loading || data.length === 0) return null;

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                💱 Correlación Dólar / Soja
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Precio Soja (USD/ton) vs Brecha Cambiaria (%) — Últimos 30 días
            </p>

            <ResponsiveContainer width="100%" height={300}>
                <ComposedChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
        </div>
    );
}
