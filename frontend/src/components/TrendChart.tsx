"use client";

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

interface DailyTrendData {
    date: string;
    alcista: number;
    bajista: number;
    neutral: number;
}

interface TrendChartProps {
    data: DailyTrendData[];
}

export default function TrendChart({ data }: TrendChartProps) {
    // Empty state
    if (!data || data.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Tendencia Diaria</h3>
                <div className="flex items-center justify-center h-64 text-gray-500">
                    <div className="text-center">
                        <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <p className="font-medium">No hay datos de tendencia para este período</p>
                        <p className="text-sm mt-2">Ejecutá "Actualizar Análisis" para obtener datos</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Tendencia Diaria</h3>

            <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={data}>
                    <defs>
                        <linearGradient id="colorAlcista" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorBajista" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorNeutral" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#6b7280" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#6b7280" stopOpacity={0} />
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
                    />
                    <Legend />
                    <Area
                        type="monotone"
                        dataKey="alcista"
                        stroke="#10b981"
                        fillOpacity={1}
                        fill="url(#colorAlcista)"
                        name="Alcista"
                    />
                    <Area
                        type="monotone"
                        dataKey="bajista"
                        stroke="#ef4444"
                        fillOpacity={1}
                        fill="url(#colorBajista)"
                        name="Bajista"
                    />
                    <Area
                        type="monotone"
                        dataKey="neutral"
                        stroke="#6b7280"
                        fillOpacity={1}
                        fill="url(#colorNeutral)"
                        name="Neutral"
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}
