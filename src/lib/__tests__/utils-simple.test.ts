// Simple test to verify basic functionality
jest.unmock('../utils');

import {
  cn,
  formatDate,
  extractDomain,
  isValidUrl,
  sanitizeFilename,
  truncateText,
  capitalizeFirst,
  getInitials,
  parseError,
} from '../utils';

describe('Utils - Core Functions', () => {
  describe('cn', () => {
    it('should merge class names', () => {
      const result = cn('text-red-500', 'bg-blue-500');
      expect(result).toContain('text-red-500');
      expect(result).toContain('bg-blue-500');
    });
  });

  describe('formatDate', () => {
    it('should format date', () => {
      const result = formatDate('2024-01-15');
      expect(result).toContain('2024');
      expect(result).toContain('January');
    });
  });

  describe('extractDomain', () => {
    it('should extract domain from URL', () => {
      expect(extractDomain('https://example.com/path')).toBe('example.com');
      expect(extractDomain('http://subdomain.example.com')).toBe('subdomain.example.com');
    });

    it('should handle invalid URLs', () => {
      expect(extractDomain('invalid-url')).toBe('invalid-url');
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

  describe('getInitials', () => {
    it('should get initials from name', () => {
      expect(getInitials('John Doe')).toBe('JD');
      expect(getInitials('John')).toBe('J');
      expect(getInitials('')).toBe('');
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
});
