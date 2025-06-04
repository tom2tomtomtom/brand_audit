/**
 * Bundle Optimization Configuration
 * Advanced Next.js optimizations for production builds
 */

import { NextConfig } from 'next';
// import CompressionPlugin from 'compression-webpack-plugin';
// import TerserPlugin from 'terser-webpack-plugin';
// import CssMinimizerPlugin from 'css-minimizer-webpack-plugin';
// import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer';
// import LodashModuleReplacementPlugin from 'lodash-webpack-plugin';

const isDev = process.env.NODE_ENV !== 'production';
const isAnalyze = process.env.ANALYZE === 'true';

export const optimizationConfig: Partial<NextConfig> = {
  // Optimize production builds
  productionBrowserSourceMaps: false,
  compress: true,
  poweredByHeader: false,
  generateEtags: true,

  // Modern build optimizations
  swcMinify: true,
  compiler: {
    removeConsole: !isDev,
    reactRemoveProperties: !isDev,
  },

  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60,
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },

  // Experimental features for performance
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
    gzipSize: true,
    craCompat: false,
    esmExternals: true,
    isrMemoryCacheSize: 0, // Disable in-memory cache for ISR
    largePageDataBytes: 128 * 1024, // 128KB
  },

  // Webpack configuration
  webpack: (config, { isServer }) => {
    // Optimization settings
    config.optimization = {
      ...config.optimization,
      minimize: !isDev,
      minimizer: [
        // TerserPlugin and CssMinimizerPlugin are handled by Next.js by default
        // new TerserPlugin({...}),
        // new CssMinimizerPlugin({...}),
      ],
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          default: false,
          vendors: false,
          framework: {
            name: 'framework',
            chunks: 'all',
            test: /[\\/]node_modules[\\/](react|react-dom|scheduler|prop-types|use-subscription)[\\/]/,
            priority: 40,
            enforce: true,
          },
          lib: {
            test(module: any) {
              return module.size() > 160000 &&
                /node_modules[/\\]/.test(module.identifier());
            },
            name(module: any) {
              const hash = require('crypto')
                .createHash('sha1')
                .update(module.identifier())
                .digest('hex');
              return `lib-${hash.substring(0, 8)}`;
            },
            priority: 30,
            minChunks: 1,
            reuseExistingChunk: true,
          },
          commons: {
            name: 'commons',
            chunks: 'all',
            minChunks: 2,
            priority: 20,
          },
          shared: {
            name(module: any, chunks: any[]) {
              return 'shared-' +
                require('crypto')
                  .createHash('sha1')
                  .update(chunks.reduce((acc, chunk) => acc + chunk.name, ''))
                  .digest('hex')
                  .substring(0, 8);
            },
            priority: 10,
            minChunks: 2,
            reuseExistingChunk: true,
          },
        },
        maxAsyncRequests: 30,
        maxInitialRequests: 30,
      },
      runtimeChunk: isServer ? false : {
        name: 'runtime',
      },
      moduleIds: 'deterministic',
    };

    // Add plugins
    if (!isServer) {
      // Plugins are commented out to avoid build issues
      // Compression and optimization are handled by Next.js and deployment platform

      // Bundle analyzer in analyze mode (optional)
      // if (isAnalyze) {
      //   config.plugins.push(
      //     new BundleAnalyzerPlugin({
      //       analyzerMode: 'static',
      //       reportFilename: './analyze.html',
      //       openAnalyzer: true,
      //     })
      //   );
      // }
    }

    // Module resolution optimizations
    config.resolve = {
      ...config.resolve,
      alias: {
        ...config.resolve.alias,
        // Use smaller lodash builds
        'lodash': 'lodash-es',
        // Use preact in production for smaller bundle
        ...(isDev ? {} : {
          'react': 'preact/compat',
          'react-dom': 'preact/compat',
        }),
      },
    };

    // Performance hints
    config.performance = {
      hints: isDev ? false : 'warning',
      maxEntrypointSize: 512000,
      maxAssetSize: 512000,
    };

    return config;
  },

  // Headers for caching and security
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains',
          },
        ],
      },
      // Static assets caching
      {
        source: '/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      // Image caching
      {
        source: '/_next/image(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      // Font caching
      {
        source: '/fonts/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },

  // Redirects and rewrites
  async rewrites() {
    return {
      beforeFiles: [
        // API versioning
        {
          source: '/api/v1/:path*',
          destination: '/api/:path*',
        },
      ],
      afterFiles: [
        // Handle trailing slashes
        {
          source: '/:path*/',
          destination: '/:path*',
        },
      ],
      fallback: [],
    };
  },
};

// Preload critical resources
export const preloadResources = [
  // Fonts
  {
    rel: 'preload',
    href: '/fonts/inter-var.woff2',
    as: 'font',
    type: 'font/woff2',
    crossOrigin: 'anonymous',
  },
  // Critical CSS
  {
    rel: 'preload',
    href: '/_next/static/css/app.css',
    as: 'style',
  },
  // Critical JS
  {
    rel: 'preload',
    href: '/_next/static/chunks/framework.js',
    as: 'script',
  },
];

// Service Worker configuration
export const serviceWorkerConfig = {
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
      handler: 'CacheFirst',
      options: {
        cacheName: 'google-fonts-cache',
        expiration: {
          maxEntries: 10,
          maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
        },
      },
    },
    {
      urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
      handler: 'CacheFirst',
      options: {
        cacheName: 'gstatic-fonts-cache',
        expiration: {
          maxEntries: 10,
          maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
        },
      },
    },
    {
      urlPattern: /^https:\/\/.*\.supabase\.co\/.*/i,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'api-cache',
        expiration: {
          maxEntries: 50,
          maxAgeSeconds: 5 * 60, // 5 minutes
        },
      },
    },
    {
      urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp|avif)$/i,
      handler: 'CacheFirst',
      options: {
        cacheName: 'image-cache',
        expiration: {
          maxEntries: 100,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
        },
      },
    },
  ],
};
