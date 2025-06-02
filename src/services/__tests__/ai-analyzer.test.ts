import { AIAnalyzerService, AnalysisInput } from '../ai-analyzer';
import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';

// Mock the dependencies
jest.mock('openai');
jest.mock('@anthropic-ai/sdk');
jest.mock('@/lib/supabase-server');
// Rate limiter is already mocked in jest.setup.js

const MockedOpenAI = OpenAI as jest.MockedClass<typeof OpenAI>;
const MockedAnthropic = Anthropic as jest.MockedClass<typeof Anthropic>;

describe('AIAnalyzerService', () => {
  let service: AIAnalyzerService;
  let mockOpenAI: jest.Mocked<OpenAI>;
  let mockAnthropic: jest.Mocked<Anthropic>;

  const mockAnalysisInput: AnalysisInput = {
    brandId: 'test-brand-id',
    brandName: 'Test Brand',
    websiteUrl: 'https://testbrand.com',
    textContent: ['Welcome to Test Brand', 'Quality products for everyone'],
    assets: [
      {
        type: 'logo',
        url: 'https://testbrand.com/logo.png',
        filename: 'logo.png',
        alt_text: 'Test Brand Logo',
      },
    ],
    competitors: ['Competitor A', 'Competitor B'],
  };

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Setup OpenAI mock
    mockOpenAI = {
      chat: {
        completions: {
          create: jest.fn(),
        },
      },
    } as any;

    // Setup Anthropic mock
    mockAnthropic = {
      messages: {
        create: jest.fn(),
      },
    } as any;

    MockedOpenAI.mockImplementation(() => mockOpenAI);
    MockedAnthropic.mockImplementation(() => mockAnthropic);

    service = new AIAnalyzerService();
  });

  describe('analyzePositioning', () => {
    it('should analyze brand positioning successfully', async () => {
      const mockResponse = {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              brandVoice: 'Professional and approachable',
              targetAudience: 'Young professionals',
              valueProposition: 'Quality and innovation',
              keyMessages: ['Quality first', 'Innovation driven'],
            }),
          },
        ],
      };

      mockAnthropic.messages.create.mockResolvedValue(mockResponse as any);

      const result = await service.analyzePositioning(mockAnalysisInput);

      expect(result).toEqual({
        brandVoice: 'Professional and approachable',
        targetAudience: 'Young professionals',
        valueProposition: 'Quality and innovation',
        keyMessages: ['Quality first', 'Innovation driven'],
      });

      expect(mockAnthropic.messages.create).toHaveBeenCalledWith({
        model: 'claude-3-sonnet-20240229',
        max_tokens: 2000,
        messages: [
          {
            role: 'user',
            content: expect.stringContaining('Analyze the brand positioning'),
          },
        ],
      });
    });

    it('should handle API errors gracefully', async () => {
      mockAnthropic.messages.create.mockRejectedValue(new Error('API Error'));

      await expect(service.analyzePositioning(mockAnalysisInput)).rejects.toThrow('API Error');
    });

    it('should handle invalid JSON response', async () => {
      const mockResponse = {
        content: [
          {
            type: 'text',
            text: 'Invalid JSON response',
          },
        ],
      };

      mockAnthropic.messages.create.mockResolvedValue(mockResponse as any);

      await expect(service.analyzePositioning(mockAnalysisInput)).rejects.toThrow();
    });
  });

  describe('analyzeVisualIdentity', () => {
    it('should analyze visual identity successfully', async () => {
      const mockResponse = {
        choices: [
          {
            message: {
              content: JSON.stringify({
                colorPalette: ['#FF0000', '#00FF00'],
                typography: ['Modern Sans-serif', 'Clean Typography'],
                logoAnalysis: 'Simple and memorable design',
                visualStyle: 'Modern and minimalist',
                consistencyScore: 85,
              }),
            },
          },
        ],
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse as any);

      const result = await service.analyzeVisualIdentity(mockAnalysisInput);

      expect(result).toEqual({
        colorPalette: ['#FF0000', '#00FF00'],
        typography: ['Modern Sans-serif', 'Clean Typography'],
        logoAnalysis: 'Simple and memorable design',
        visualStyle: 'Modern and minimalist',
        consistencyScore: 85,
      });

      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
        model: 'gpt-4-vision-preview',
        messages: [
          {
            role: 'user',
            content: expect.stringContaining('analyze the visual identity'),
          },
        ],
        max_tokens: 1500,
      });
    });

    it('should handle empty response', async () => {
      const mockResponse = {
        choices: [
          {
            message: {
              content: null,
            },
          },
        ],
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse as any);

      await expect(service.analyzeVisualIdentity(mockAnalysisInput)).rejects.toThrow('No response content');
    });
  });

  describe('analyzeCompetitive', () => {
    it('should analyze competitive landscape successfully', async () => {
      const mockResponse = {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              marketPosition: 'Market leader',
              strengths: ['Strong brand', 'Quality products'],
              weaknesses: ['High prices', 'Limited reach'],
              opportunities: ['New markets', 'Digital expansion'],
              threats: ['New competitors', 'Economic downturn'],
              competitiveAdvantage: 'Superior quality and brand recognition',
            }),
          },
        ],
      };

      mockAnthropic.messages.create.mockResolvedValue(mockResponse as any);

      const result = await service.analyzeCompetitive(mockAnalysisInput);

      expect(result).toEqual({
        marketPosition: 'Market leader',
        strengths: ['Strong brand', 'Quality products'],
        weaknesses: ['High prices', 'Limited reach'],
        opportunities: ['New markets', 'Digital expansion'],
        threats: ['New competitors', 'Economic downturn'],
        competitiveAdvantage: 'Superior quality and brand recognition',
      });
    });
  });

  describe('analyzeSentiment', () => {
    it('should analyze sentiment successfully', async () => {
      const mockResponse = {
        choices: [
          {
            message: {
              content: JSON.stringify({
                overallSentiment: 'positive',
                emotionalTone: 'confident',
                brandPersonality: ['trustworthy', 'innovative'],
                sentimentScore: 0.8,
              }),
            },
          },
        ],
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse as any);

      const result = await service.analyzeSentiment(mockAnalysisInput);

      expect(result).toEqual({
        overallSentiment: 'positive',
        emotionalTone: 'confident',
        brandPersonality: ['trustworthy', 'innovative'],
        sentimentScore: 0.8,
      });
    });
  });

  describe('runFullAnalysis', () => {
    it('should run all analyses and handle partial failures', async () => {
      // Mock successful positioning analysis
      mockAnthropic.messages.create.mockResolvedValueOnce({
        content: [
          {
            type: 'text',
            text: JSON.stringify({ brandVoice: 'Professional' }),
          },
        ],
      } as any);

      // Mock failed visual analysis
      mockOpenAI.chat.completions.create.mockRejectedValueOnce(new Error('Visual analysis failed'));

      // Mock successful competitive analysis
      mockAnthropic.messages.create.mockResolvedValueOnce({
        content: [
          {
            type: 'text',
            text: JSON.stringify({ marketPosition: 'Leader' }),
          },
        ],
      } as any);

      // Mock successful sentiment analysis
      mockOpenAI.chat.completions.create.mockResolvedValueOnce({
        choices: [
          {
            message: {
              content: JSON.stringify({ overallSentiment: 'positive' }),
            },
          },
        ],
      } as any);

      // Mock prepareBrandData method
      jest.spyOn(service as any, 'prepareBrandData').mockResolvedValue(mockAnalysisInput);
      jest.spyOn(service as any, 'updateBrandStatus').mockResolvedValue(undefined);

      const result = await service.runFullAnalysis('test-brand-id');

      expect(result.positioning).toEqual({ brandVoice: 'Professional' });
      expect(result.visual).toBeUndefined();
      expect(result.competitive).toEqual({ marketPosition: 'Leader' });
      expect(result.sentiment).toEqual({ overallSentiment: 'positive' });
      expect(result.errors).toHaveLength(1);
      expect(result.errors[0]).toContain('visual analysis failed');
    });
  });
});
