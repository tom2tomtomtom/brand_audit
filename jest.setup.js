import '@testing-library/jest-dom'

// Polyfill Web APIs for Jest environment
global.Request = class Request {
  constructor(input, init = {}) {
    this.url = typeof input === 'string' ? input : input.url;
    this.method = init.method || 'GET';
    this.headers = new Headers(init.headers);
    this.body = init.body;
  }
};

global.Response = class Response {
  constructor(body, init = {}) {
    this._body = body;
    this.status = init.status || 200;
    this.headers = new Headers(init.headers);
    this.ok = this.status >= 200 && this.status < 300;
  }

  static json(data, init) {
    const response = new Response(JSON.stringify(data), init);
    response.headers.set('Content-Type', 'application/json');
    return response;
  }

  async json() {
    return JSON.parse(this._body);
  }

  async text() {
    return this._body;
  }
};

global.Headers = class Headers {
  constructor(init = {}) {
    this._headers = new Map();
    if (init) {
      for (const [key, value] of Object.entries(init)) {
        this.set(key, value);
      }
    }
  }

  set(key, value) {
    this._headers.set(key.toLowerCase(), value);
  }

  get(key) {
    return this._headers.get(key.toLowerCase());
  }

  has(key) {
    return this._headers.has(key.toLowerCase());
  }
};

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
      forward: jest.fn(),
      refresh: jest.fn(),
    }
  },
  useSearchParams() {
    return new URLSearchParams()
  },
  usePathname() {
    return '/'
  },
}))

// Mock Supabase
jest.mock('src/lib/supabase', () => ({
  createClientSupabase: jest.fn(() => ({
    auth: {
      getUser: jest.fn(),
      signInWithPassword: jest.fn(),
      signUp: jest.fn(),
      signOut: jest.fn(),
      onAuthStateChange: jest.fn(),
      signInWithOAuth: jest.fn(),
    },
    from: jest.fn(() => ({
      select: jest.fn().mockReturnThis(),
      insert: jest.fn().mockReturnThis(),
      update: jest.fn().mockReturnThis(),
      delete: jest.fn().mockReturnThis(),
      eq: jest.fn().mockReturnThis(),
      order: jest.fn().mockReturnThis(),
      single: jest.fn().mockResolvedValue({ data: null, error: null }),
    })),
    storage: {
      from: jest.fn(() => ({
        upload: jest.fn(),
        download: jest.fn(),
        remove: jest.fn(),
      })),
    },
  })),
}))

// Mock server Supabase
jest.mock('src/lib/supabase-server', () => ({
  createServerSupabase: jest.fn(() => ({
    auth: {
      getUser: jest.fn(),
    },
    from: jest.fn(() => ({
      select: jest.fn().mockReturnThis(),
      insert: jest.fn().mockReturnThis(),
      update: jest.fn().mockReturnThis(),
      delete: jest.fn().mockReturnThis(),
      eq: jest.fn().mockReturnThis(),
      order: jest.fn().mockReturnThis(),
      single: jest.fn().mockResolvedValue({ data: null, error: null }),
      rpc: jest.fn(),
    })),
    storage: {
      from: jest.fn(() => ({
        upload: jest.fn(),
        download: jest.fn(),
        remove: jest.fn(),
      })),
    },
  })),
}))

// Mock environment variables
process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co'
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key'
process.env.SUPABASE_SERVICE_ROLE_KEY = 'test-service-role-key'
process.env.OPENAI_API_KEY = 'test-openai-key'
process.env.ANTHROPIC_API_KEY = 'test-anthropic-key'

// Mock toast notifications
jest.mock('react-hot-toast', () => ({
  __esModule: true,
  default: {
    success: jest.fn(),
    error: jest.fn(),
    loading: jest.fn(),
  },
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    loading: jest.fn(),
  },
}))

// Mock Puppeteer
jest.mock('puppeteer', () => ({
  launch: jest.fn(() => Promise.resolve({
    newPage: jest.fn(() => Promise.resolve({
      goto: jest.fn(),
      content: jest.fn(),
      close: jest.fn(),
      setUserAgent: jest.fn(),
      setViewport: jest.fn(),
      waitForTimeout: jest.fn(),
      pdf: jest.fn(),
      addStyleTag: jest.fn(),
      setContent: jest.fn(),
      screenshot: jest.fn().mockResolvedValue(Buffer.from('fake-screenshot')),
      evaluate: jest.fn().mockResolvedValue({}),
    })),
    close: jest.fn(),
  })),
}))

// Mock OpenAI
jest.mock('openai', () => {
  return jest.fn().mockImplementation(() => ({
    chat: {
      completions: {
        create: jest.fn(),
      },
    },
  }))
})

// Mock Anthropic
jest.mock('@anthropic-ai/sdk', () => {
  return jest.fn().mockImplementation(() => ({
    messages: {
      create: jest.fn(),
    },
  }))
})

// Mock storage
jest.mock('src/lib/storage', () => ({
  uploadFile: jest.fn(),
  downloadFile: jest.fn(),
  deleteFile: jest.fn(),
}))

// Mock rate limiter
jest.mock('src/lib/rate-limiter', () => ({
  openaiRateLimiter: { checkLimit: jest.fn(() => true) },
  anthropicRateLimiter: { checkLimit: jest.fn(() => true) },
  checkRateLimit: jest.fn(() => true),
  costTracker: {
    trackCost: jest.fn(),
    checkCostLimit: jest.fn(() => true),
    getCostUsage: jest.fn(() => ({ used: 0, limit: 100 }))
  },
  handleAPIError: jest.fn(),
  retryWithBackoff: jest.fn((fn) => fn()),
  APIError: class extends Error {
    constructor(message, status, code) {
      super(message);
      this.status = status;
      this.code = code;
    }
  },
}))

// Mock utils
jest.mock('src/lib/utils', () => ({
  cn: jest.fn((...args) => args.join(' ')),
  formatDate: jest.fn((date) => new Date(date).toLocaleDateString()),
  formatFileSize: jest.fn((size) => `${size} B`),
  extractDomain: jest.fn((url) => {
    try {
      return new URL(url).hostname;
    } catch {
      return '';
    }
  }),
  isValidUrl: jest.fn((url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }),
  sanitizeFilename: jest.fn((name) => name.replace(/[<>:"/\\|?*]/g, '')),
  truncateText: jest.fn((text, length) => text.length > length ? text.slice(0, length) + '...' : text),
  capitalizeFirst: jest.fn((str) => str.charAt(0).toUpperCase() + str.slice(1)),
  debounce: jest.fn((fn) => fn),
  throttle: jest.fn((fn) => fn),
  sleep: jest.fn((ms) => Promise.resolve()),
  getInitials: jest.fn((name) => name.split(' ').map(n => n[0]).join('').toUpperCase()),
  generateId: jest.fn(() => 'test-id'),
  parseError: jest.fn((error) => error instanceof Error ? error.message : String(error)),
  formatCurrency: jest.fn((amount) => `$${amount}`),
  formatNumber: jest.fn((num) => num.toString()),
  getColorFromString: jest.fn(() => 'hsl(0, 70%, 50%)'),
}))

// Global test timeout
jest.setTimeout(30000)
