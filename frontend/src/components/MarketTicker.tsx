"use client";

import React from 'react';
import { TickerTape } from "react-ts-tradingview-widgets";

export default function MarketTicker() {
    return (
        <div className="w-full bg-white border-b border-gray-200">
            <div className="h-12">
                <TickerTape
                    colorTheme="light"
                    displayMode="regular"
                    showSymbolLogo={true}
                    symbols={[
                        {
                            proName: "ZS1!",
                            title: "Soja (Futuro)"
                        },
                        {
                            proName: "FX_IDC:USDARS",
                            title: "Dólar Oficial"
                        },
                        {
                            proName: "BCBA:SOJ.ROS", // Try specific local symbol if available on TV, else keep futures
                            title: "Soja (Futuro)"
                        }
                    ]}
                />
            </div>
        </div>
    );
}
