"use client";

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

interface TimelineData {
    date: string;
    sentiment_score: number;
}

interface SentimentTimelineProps {
    data: TimelineData[];
}

export default function SentimentTimeline({ data }: SentimentTimelineProps) {
    if (!data || data.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Score de Sentimiento</h3>
                <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
                    <p className="font-medium">No hay datos de tendencia para este período</p>
                </div>
            </div>
        );
    }

    const gradientOffset = () => {
        const dataMax = Math.max(...data.map((i) => i.sentiment_score));
        const dataMin = Math.min(...data.map((i) => i.sentiment_score));
        if (dataMax <= 0) return 0;
        if (dataMin >= 0) return 1;
        return dataMax / (dataMax - dataMin);
    };

    const off = gradientOffset();

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Score de Sentimiento</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                +1 = Muy Alcista | 0 = Neutral | -1 = Muy Bajista (ponderado por confianza)
            </p>

            <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                        <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                            <stop offset={off} stopColor="#10b981" stopOpacity={1} />
                            <stop offset={off} stopColor="#ef4444" stopOpacity={1} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                        dataKey="date"
                        stroke="#9ca3af"
                        tick={{ fill: '#9ca3af' }}
                        tickFormatter={(date) => format(parseISO(date), 'dd/MM', { locale: es })}
                    />
                    <YAxis domain={[-1, 1]} stroke="#9ca3af" tick={{ fill: '#9ca3af' }} />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1f2937',
                            border: '1px solid #374151',
                            borderRadius: '8px',
                            color: '#fff'
                        }}
                        labelFormatter={(date) => format(parseISO(date as string), "dd 'de' MMMM", { locale: es })}
                        formatter={(value: number) => [value.toFixed(2), 'Score']}
                    />
                    <ReferenceLine y={0} stroke="#9ca3af" strokeDasharray="3 3" />
                    <Area
                        type="monotone"
                        dataKey="sentiment_score"
                        stroke="url(#splitColor)"
                        fill="url(#splitColor)"
                        fillOpacity={0.3}
                        strokeWidth={3}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}
