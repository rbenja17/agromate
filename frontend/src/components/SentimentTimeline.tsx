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
    // Empty state
    if (!data || data.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Score de Sentimiento</h3>
                <div className="flex items-center justify-center h-64 text-gray-500">
                    <div className="text-center">
                        <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                        <p className="font-medium">No hay datos de tendencia para este período</p>
                        <p className="text-sm mt-2">Ejecutá "Actualizar Análisis" para obtener datos</p>
                    </div>
                </div>
            </div>
        );
    }

    // Calcular offset para el gradiente (dónde está el 0 en el eje Y)
    const gradientOffset = () => {
        const dataMax = Math.max(...data.map((i) => i.sentiment_score));
        const dataMin = Math.min(...data.map((i) => i.sentiment_score));

        if (dataMax <= 0) return 0;
        if (dataMin >= 0) return 1;

        return dataMax / (dataMax - dataMin);
    };

    const off = gradientOffset();

    return (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-xl font-bold text-gray-900 mb-2">Score de Sentimiento</h3>
            <p className="text-sm text-gray-600 mb-4">
                +1 = Muy Alcista | 0 = Neutral | -1 = Muy Bajista (ponderado por confianza)
            </p>

            <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                        {/* Gradiente condicional: verde arriba de 0, rojo abajo */}
                        <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                            <stop offset={off} stopColor="#10b981" stopOpacity={1} />
                            <stop offset={off} stopColor="#ef4444" stopOpacity={1} />
                        </linearGradient>
                    </defs>

                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis
                        dataKey="date"
                        stroke="#6b7280"
                        tick={{ fill: '#4b5563' }}
                        tickFormatter={(date) => format(parseISO(date), 'dd/MM', { locale: es })}
                    />
                    <YAxis
                        domain={[-1, 1]}
                        stroke="#6b7280"
                        tick={{ fill: '#4b5563' }}
                    />
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
                    {/* Usamos el gradiente splitColor */}
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
