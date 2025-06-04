// Application-wide constants
export const APP_CONSTANTS = {
  // Application metadata
  APP_NAME: 'Brand Audit Tool',
  APP_VERSION: '1.0.0',
  APP_DESCRIPTION: 'Comprehensive brand analysis and competitive intelligence platform',
  
  // API Configuration
  API: {
    VERSION: 'v1',
    BASE_PATH: '/api',
    TIMEOUT: 30000, // 30 seconds
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000, // 1 second
  },
  
  // Rate Limiting
  RATE_LIMITS: {
    // General API rate limits
    API_REQUESTS_PER_MINUTE: 100,
    API_REQUESTS_PER_HOUR: 1000,
    
    // AI Service specific limits
    OPENAI_REQUESTS_PER_HOUR: 50,
    ANTHROPIC_REQUESTS_PER_HOUR: 30,
    
    // Scraping limits
    SCRAPING_REQUESTS_PER_HOUR: 20,
    CONCURRENT_SCRAPING_JOBS: 3,
    
    // Analysis limits
    ANALYSIS_REQUESTS_PER_DAY: 100,
    CONCURRENT_ANALYSIS_JOBS: 2,
  },
  
  // AI Analysis Configuration
  AI_ANALYSIS: {
    // Token limits
    MAX_TOKENS: {
      OPENAI_GPT4: 8000,
      OPENAI_GPT35: 4000,
      ANTHROPIC_CLAUDE: 8000,
    },
    
    // Confidence thresholds
    CONFIDENCE_THRESHOLD: {
      HIGH: 0.85,
      MEDIUM: 0.70,
      LOW: 0.50,
    },
    
    // Retry configuration
    MAX_RETRY_ATTEMPTS: 3,
    RETRY_DELAY_MS: 2000,
    EXPONENTIAL_BACKOFF: true,
    
    // Analysis types
    ANALYSIS_TYPES: {
      BRAND_POSITIONING: 'brand_positioning',
      VISUAL_IDENTITY: 'visual_identity',
      CONTENT_ANALYSIS: 'content_analysis',
      COMPETITIVE_ANALYSIS: 'competitive_analysis',
      COMPREHENSIVE: 'comprehensive',
    },
    
    // Analysis depth levels
    DEPTH_LEVELS: {
      SHALLOW: 'shallow',
      MEDIUM: 'medium',
      DEEP: 'deep',
    },
  },
  
  // Scraping Configuration
  SCRAPING: {
    // Timeouts
    PAGE_TIMEOUT: 30000, // 30 seconds
    NAVIGATION_TIMEOUT: 15000, // 15 seconds
    ELEMENT_TIMEOUT: 5000, // 5 seconds
    
    // Delays
    DELAY_BETWEEN_REQUESTS: 2000, // 2 seconds
    DELAY_AFTER_LOAD: 3000, // 3 seconds
    
    // Limits
    MAX_PAGES_PER_SITE: 10,
    MAX_CONCURRENT_PAGES: 3,
    MAX_ASSETS_PER_PAGE: 50,
    
    // Browser configuration
    VIEWPORT: {
      WIDTH: 1920,
      HEIGHT: 1080,
    },
    
    // User agents
    USER_AGENTS: [
      'Mozilla/5.0 (compatible; BrandAuditBot/1.0)',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    ],
    
    // Asset types to collect
    ASSET_TYPES: {
      IMAGES: 'image',
      LOGOS: 'logo',
      DOCUMENTS: 'document',
      VIDEOS: 'video',
      FONTS: 'font',
    },
  },
  
  // File and Storage Configuration
  STORAGE: {
    // File size limits (in bytes)
    MAX_FILE_SIZE: {
      IMAGE: 10 * 1024 * 1024, // 10MB
      DOCUMENT: 50 * 1024 * 1024, // 50MB
      VIDEO: 100 * 1024 * 1024, // 100MB
      GENERAL: 25 * 1024 * 1024, // 25MB
    },
    
    // Allowed file types
    ALLOWED_MIME_TYPES: {
      IMAGES: [
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
        'image/svg+xml',
      ],
      DOCUMENTS: [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
      ],
      VIDEOS: [
        'video/mp4',
        'video/webm',
        'video/ogg',
      ],
    },
    
    // Storage buckets
    BUCKETS: {
      BRAND_LOGOS: 'brand-logos',
      CAMPAIGN_ASSETS: 'campaign-assets',
      SCREENSHOTS: 'screenshots',
      PRESENTATIONS: 'presentations',
      EXPORTS: 'exports',
    },
  },
  
  // Database Configuration
  DATABASE: {
    // Connection settings
    MAX_CONNECTIONS: 20,
    CONNECTION_TIMEOUT: 10000, // 10 seconds
    IDLE_TIMEOUT: 30000, // 30 seconds
    
    // Query limits
    MAX_QUERY_RESULTS: 1000,
    DEFAULT_PAGE_SIZE: 20,
    MAX_PAGE_SIZE: 100,
    
    // Batch operation limits
    MAX_BATCH_SIZE: 100,
    MAX_BULK_INSERT: 500,
  },
  
  // Cost Tracking
  COST_TRACKING: {
    // Monthly limits (in USD)
    MONTHLY_BUDGET_LIMIT: 1000,
    WARNING_THRESHOLD: 0.80, // 80% of budget
    CRITICAL_THRESHOLD: 0.95, // 95% of budget
    
    // Cost per operation (in USD)
    COSTS: {
      OPENAI_GPT4_PER_1K_TOKENS: 0.03,
      OPENAI_GPT35_PER_1K_TOKENS: 0.002,
      ANTHROPIC_CLAUDE_PER_1K_TOKENS: 0.008,
      SCRAPING_PER_PAGE: 0.01,
      STORAGE_PER_GB_MONTH: 0.02,
    },
  },
  
  // User and Organization Limits
  LIMITS: {
    // Free tier limits
    FREE_TIER: {
      BRANDS_PER_ORG: 5,
      ANALYSES_PER_MONTH: 10,
      STORAGE_GB: 1,
      TEAM_MEMBERS: 3,
    },
    
    // Pro tier limits
    PRO_TIER: {
      BRANDS_PER_ORG: 50,
      ANALYSES_PER_MONTH: 100,
      STORAGE_GB: 10,
      TEAM_MEMBERS: 10,
    },
    
    // Enterprise tier limits
    ENTERPRISE_TIER: {
      BRANDS_PER_ORG: 500,
      ANALYSES_PER_MONTH: 1000,
      STORAGE_GB: 100,
      TEAM_MEMBERS: 100,
    },
  },
  
  // Cache Configuration
  CACHE: {
    // TTL values (in seconds)
    TTL: {
      SHORT: 300, // 5 minutes
      MEDIUM: 1800, // 30 minutes
      LONG: 3600, // 1 hour
      VERY_LONG: 86400, // 24 hours
    },
    
    // Cache keys
    KEYS: {
      USER_SESSION: 'user:session:',
      BRAND_DATA: 'brand:data:',
      ANALYSIS_RESULT: 'analysis:result:',
      ORGANIZATION_DATA: 'org:data:',
    },
  },
  
  // Monitoring and Logging
  MONITORING: {
    // Log levels
    LOG_LEVELS: {
      ERROR: 'error',
      WARN: 'warn',
      INFO: 'info',
      DEBUG: 'debug',
    },
    
    // Metrics collection intervals (in milliseconds)
    METRICS_INTERVAL: 60000, // 1 minute
    HEALTH_CHECK_INTERVAL: 30000, // 30 seconds
    
    // Alert thresholds
    ALERT_THRESHOLDS: {
      ERROR_RATE: 0.05, // 5% error rate
      RESPONSE_TIME_P95: 2000, // 2 seconds
      MEMORY_USAGE: 0.85, // 85% memory usage
      CPU_USAGE: 0.80, // 80% CPU usage
    },
  },
  
  // Feature Flags
  FEATURES: {
    ENABLE_ANALYTICS: true,
    ENABLE_DEBUG_LOGS: false,
    ENABLE_RATE_LIMITING: true,
    ENABLE_CACHING: true,
    ENABLE_MONITORING: true,
    ENABLE_EXPERIMENTAL_AI: false,
    ENABLE_BULK_OPERATIONS: true,
    ENABLE_REAL_TIME_UPDATES: false,
  },
  
  // External Service URLs
  EXTERNAL_SERVICES: {
    OPENAI_API_BASE: 'https://api.openai.com/v1',
    ANTHROPIC_API_BASE: 'https://api.anthropic.com/v1',
    SENTRY_DSN: process.env.SENTRY_DSN,
  },
  
  // UI Configuration
  UI: {
    // Pagination
    DEFAULT_PAGE_SIZE: 20,
    PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
    
    // Timeouts for UI operations
    TOAST_DURATION: 5000, // 5 seconds
    LOADING_TIMEOUT: 30000, // 30 seconds
    
    // Animation durations (in milliseconds)
    ANIMATION: {
      FAST: 150,
      NORMAL: 300,
      SLOW: 500,
    },
  },
} as const;

// Export specific constant groups for easier imports
export const { AI_ANALYSIS, SCRAPING, STORAGE, RATE_LIMITS, COST_TRACKING } = APP_CONSTANTS;

// Type definitions for constants
export type AnalysisType = typeof APP_CONSTANTS.AI_ANALYSIS.ANALYSIS_TYPES[keyof typeof APP_CONSTANTS.AI_ANALYSIS.ANALYSIS_TYPES];
export type DepthLevel = typeof APP_CONSTANTS.AI_ANALYSIS.DEPTH_LEVELS[keyof typeof APP_CONSTANTS.AI_ANALYSIS.DEPTH_LEVELS];
export type AssetType = typeof APP_CONSTANTS.SCRAPING.ASSET_TYPES[keyof typeof APP_CONSTANTS.SCRAPING.ASSET_TYPES];
export type StorageBucket = typeof APP_CONSTANTS.STORAGE.BUCKETS[keyof typeof APP_CONSTANTS.STORAGE.BUCKETS];
