import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable static exports for better Netlify compatibility
  output: 'standalone',
  
  // Disable image optimization for static export
  images: {
    unoptimized: true
  },
  
  // Enable experimental features needed for app directory
  experimental: {
    serverComponentsExternalPackages: ['puppeteer']
  },
  
  // Configure webpack for browser compatibility
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  }
};

export default nextConfig;
