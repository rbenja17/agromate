"use client";

import { useEffect, useState } from 'react';
import { fetchMarketData } from '@/lib/api';

interface MarketData {
    price: number;
    currency: string;
    change_percent: number;
    symbol: string;
}

interface MarketResponse {
    timestamp: string;
    data: {
        [key: string]: MarketData | { error: string, symbol: string };
    };
}

export default function MarketOverview() {
    const [data, setData] = useState<MarketResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadMarket = async () => {
            try {
                const result = await fetchMarketData();
                setData(result);
            } catch (err) {
                setError("Datos no disponibles");
            } finally {
                setLoading(false);
            }
        };

        loadMarket();
        // Refresh every 60 seconds
        const interval = setInterval(loadMarket, 60000);
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-100 dark:border-gray-700 animate-pulse">
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
                        <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                    </div>
                ))}
            </div>
        );
    }

    if (error || !data || !data.data) {
        return (
            <div className="bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 p-4 rounded-lg mb-8 text-center text-sm">
                Datos de mercado no disponibles
            </div>
        );
    }

    const commodities = [
        { key: 'soja_rosario', name: 'Soja (CBOT)', icon: '🌱' },
        { key: 'maiz_rosario', name: 'Maíz (CBOT)', icon: '🌽' },
        { key: 'trigo_rosario', name: 'Trigo (CBOT)', icon: '🌾' },
        { key: 'dolar', name: 'Dólar Oficial', icon: '💵' },
        { key: 'dolar_blue', name: 'Dólar Blue', icon: '💸' }
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            {commodities.map((item) => {
                const info = data.data[item.key] as MarketData;

                if (!info || 'error' in info) {
                    return (
                        <div key={item.key} className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-100 dark:border-gray-700">
                            <h3 className="text-gray-500 dark:text-gray-400 font-medium text-sm flex items-center gap-2 uppercase tracking-wide">
                                <span>{item.icon}</span> {item.name}
                            </h3>
                            <p className="text-gray-400 mt-2 text-sm">No disponible</p>
                        </div>
                    );
                }

                const isPositive = info.change_percent >= 0;
                const isArs = info.currency === 'ARS';

                return (
                    <div key={item.key} className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
                        <h3 className="text-gray-500 dark:text-gray-400 font-medium text-sm flex items-center gap-2 uppercase tracking-wide">
                            <span>{item.icon}</span> {item.name}
                        </h3>

                        <div className="mt-2 flex items-baseline gap-2">
                            <span className="text-2xl font-bold text-gray-900 dark:text-white">
                                {isArs ? '$' : 'US$ '}
                                {info.price.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                            </span>
                        </div>

                        <div className={`mt-2 text-sm font-medium flex items-center gap-1 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                            <span>{isPositive ? '↑' : '↓'}</span>
                            <span>{Math.abs(info.change_percent).toFixed(2)}%</span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
