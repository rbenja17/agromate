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
                            proName: "CBOT:ZS1!",
                            title: "Soja (Futuro)"
                        },
                        {
                            proName: "CBOT:ZC1!",
                            title: "Maíz (Futuro)"
                        },
                        {
                            proName: "CBOT:ZW1!",
                            title: "Trigo (Futuro)"
                        },
                        {
                            proName: "FX_IDC:USDARS",
                            title: "USD/ARS"
                        }
                    ]}
                />
            </div>
        </div>
    );
}
