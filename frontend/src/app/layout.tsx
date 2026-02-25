import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
    title: "Agromate - Análisis de Sentimiento Agropecuario",
    description: "Análisis de sentimiento del mercado agropecuario argentino (Matba Rofex)",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="es" suppressHydrationWarning>
            <head>
                <script dangerouslySetInnerHTML={{
                    __html: `
                        (function() {
                            var theme = localStorage.getItem('theme');
                            if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                                document.documentElement.classList.add('dark');
                            }
                        })();
                    `
                }} />
            </head>
            <body className={`${inter.variable} ${jetbrainsMono.variable} ${inter.className}`}>
                {children}
            </body>
        </html>
    );
}
