import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Agromate - Análisis de Sentimiento Agropecuario",
    description: "Análisis de sentimiento del mercado agropecuario argentino (Matba Rofex)",
};

import MarketTicker from "@/components/MarketTicker";

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="es">
            <body className={inter.className}>
                <MarketTicker />
                {children}
            </body>
        </html>
    );
}
