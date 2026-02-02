/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,

    // Static HTML export for Cloudflare Pages
    output: 'export',

    // Required for static export - disables Image Optimization API
    images: {
        unoptimized: true
    },

    // Trailing slash for better static hosting compatibility
    trailingSlash: true,

    // Environment variable for API URL (set in Cloudflare Pages dashboard)
    // NEXT_PUBLIC_API_URL will be available at build time
};

export default nextConfig;
