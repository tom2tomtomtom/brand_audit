// Import the actual functions, not mocked ones
jest.unmock('../utils');

import {
  cn,
  formatDate,
  formatFileSize,
  extractDomain,
  isValidUrl,
  sanitizeFilename,
  truncateText,
  capitalizeFirst,
  debounce,
  throttle,
  sleep,
  getInitials,
  generateId,
  parseError,
  formatCurrency,
  formatNumber,
  getColorFromString,
} from '../utils';

describe('Utils', () => {
  describe('cn', () => {
    it('should merge class names correctly', () => {
      expect(cn('text-red-500', 'bg-blue-500')).toBe('text-red-500 bg-blue-500');
      expect(cn('text-red-500', 'text-blue-500')).toBe('text-blue-500');
    });
  });

  describe('formatDate', () => {
    it('should format date correctly', () => {
      const date = new Date('2024-01-15');
      const formatted = formatDate(date);
      expect(formatted).toBe('January 15, 2024');
    });

    it('should handle string dates', () => {
      const formatted = formatDate('2024-01-15');
      expect(formatted).toBe('January 15, 2024');
    });
  });

  describe('formatFileSize', () => {
    it('should format bytes correctly', () => {
      expect(formatFileSize(1024)).toBe('1 KB');
      expect(formatFileSize(1048576)).toBe('1 MB');
      expect(formatFileSize(1073741824)).toBe('1 GB');
      expect(formatFileSize(500)).toBe('500 Bytes');
    });
  });

  describe('extractDomain', () => {
    it('should extract domain from URL', () => {
      expect(extractDomain('https://example.com/path')).toBe('example.com');
      expect(extractDomain('http://subdomain.example.com')).toBe('subdomain.example.com');
      expect(extractDomain('https://example.com:8080')).toBe('example.com');
    });

    it('should handle invalid URLs', () => {
      expect(extractDomain('invalid-url')).toBe('invalid-url');
      expect(extractDomain('')).toBe('');
    });
  });

  describe('isValidUrl', () => {
    it('should validate URLs correctly', () => {
      expect(isValidUrl('https://example.com')).toBe(true);
      expect(isValidUrl('http://example.com')).toBe(true);
      expect(isValidUrl('ftp://example.com')).toBe(false);
      expect(isValidUrl('invalid-url')).toBe(false);
      expect(isValidUrl('')).toBe(false);
    });
  });

  describe('sanitizeFilename', () => {
    it('should sanitize filenames', () => {
      expect(sanitizeFilename('file<>name.txt')).toBe('filename.txt');
      expect(sanitizeFilename('file/name\\test.txt')).toBe('filenametest.txt');
      expect(sanitizeFilename('file:name|test.txt')).toBe('filenametest.txt');
    });
  });

  describe('truncateText', () => {
    it('should truncate text correctly', () => {
      expect(truncateText('Hello World', 5)).toBe('Hello...');
      expect(truncateText('Hello', 10)).toBe('Hello');
      expect(truncateText('', 5)).toBe('');
    });
  });

  describe('capitalizeFirst', () => {
    it('should capitalize first letter', () => {
      expect(capitalizeFirst('hello')).toBe('Hello');
      expect(capitalizeFirst('HELLO')).toBe('HELLO');
      expect(capitalizeFirst('')).toBe('');
    });
  });

  describe('debounce', () => {
    jest.useFakeTimers();

    it('should debounce function calls', () => {
      const mockFn = jest.fn();
      const debouncedFn = debounce(mockFn, 100);

      debouncedFn();
      debouncedFn();
      debouncedFn();

      expect(mockFn).not.toHaveBeenCalled();

      jest.advanceTimersByTime(100);
      expect(mockFn).toHaveBeenCalledTimes(1);
    });

    afterEach(() => {
      jest.clearAllTimers();
    });
  });

  describe('throttle', () => {
    jest.useFakeTimers();

    it('should throttle function calls', () => {
      const mockFn = jest.fn();
      const throttledFn = throttle(mockFn, 100);

      throttledFn();
      throttledFn();
      throttledFn();

      expect(mockFn).toHaveBeenCalledTimes(1);

      jest.advanceTimersByTime(100);
      throttledFn();
      expect(mockFn).toHaveBeenCalledTimes(2);
    });

    afterEach(() => {
      jest.clearAllTimers();
    });
  });

  describe('sleep', () => {
    it('should resolve after specified time', async () => {
      const start = Date.now();
      await sleep(100);
      const end = Date.now();
      expect(end - start).toBeGreaterThanOrEqual(90);
    });
  });

  describe('getInitials', () => {
    it('should get initials from name', () => {
      expect(getInitials('John Doe')).toBe('JD');
      expect(getInitials('John')).toBe('J');
      expect(getInitials('John Michael Doe')).toBe('JO'); // Only first 2 initials
      expect(getInitials('')).toBe('');
    });
  });

  describe('generateId', () => {
    it('should generate unique IDs', () => {
      const id1 = generateId();
      const id2 = generateId();
      expect(id1).not.toBe(id2);
      expect(typeof id1).toBe('string');
      expect(id1.length).toBeGreaterThan(0);
    });
  });

  describe('parseError', () => {
    it('should parse different error types', () => {
      expect(parseError(new Error('Test error'))).toBe('Test error');
      expect(parseError('String error')).toBe('String error');
      expect(parseError(null)).toBe('An unknown error occurred');
      expect(parseError(undefined)).toBe('An unknown error occurred');
    });
  });

  describe('formatCurrency', () => {
    it('should format currency correctly', () => {
      expect(formatCurrency(1234.56)).toBe('$1,234.56');
      expect(formatCurrency(1234.56, 'EUR')).toBe('€1,234.56');
    });
  });

  describe('formatNumber', () => {
    it('should format numbers with commas', () => {
      expect(formatNumber(1234)).toBe('1,234');
      expect(formatNumber(1234567)).toBe('1,234,567');
    });
  });

  describe('getColorFromString', () => {
    it('should generate consistent colors from strings', () => {
      const color1 = getColorFromString('test');
      const color2 = getColorFromString('test');
      const color3 = getColorFromString('different');

      expect(color1).toBe(color2);
      expect(color1).not.toBe(color3);
      expect(color1).toMatch(/^hsl\(\d+, 70%, 50%\)$/);
    });
  });
});
