import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
import { createServerSupabase } from '@/lib/supabase-server';
import {
  openaiRateLimiter,
  anthropicRateLimiter,
  checkRateLimit,
  costTracker,
  handleAPIError,
  retryWithBackoff,
  APIError
} from '@/lib/rate-limiter';
import type {
  PositioningAnalysis,
  VisualAnalysis,
  CompetitiveAnalysis,
  SentimentAnalysis
} from '@/types';

export interface AnalysisInput {
  brandId: string;
  brandName: string;
  websiteUrl: string;
  textContent: string[];
  assets: Array<{
    type: string;
    url: string;
    filename: string;
    alt_text?: string;
  }>;
  competitors?: string[];
}

export class AIAnalyzerService {
  private openai: OpenAI;
  private anthropic: Anthropic;
  private userId: string;

  constructor(userId?: string) {
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    this.userId = userId || 'anonymous';
  }

  async analyzePositioning(input: AnalysisInput): Promise<PositioningAnalysis> {
    // Check rate limit
    await checkRateLimit(anthropicRateLimiter, this.userId, 'positioning analysis');

    // Check cost limit
    if (!costTracker.checkCostLimit(this.userId)) {
      throw new APIError('Monthly cost limit exceeded', 429, 'COST_LIMIT_EXCEEDED');
    }

    const prompt = `
Analyze the brand positioning for ${input.brandName} based on the following information:

Website: ${input.websiteUrl}
Content: ${input.textContent.join('\n')}

Please provide a comprehensive brand positioning analysis including:
1. Brand voice and tone
2. Target audience segments
3. Value proposition
4. Key messages
5. Competitive differentiation
6. Brand personality traits

Format your response as JSON with the following structure:
{
  "brandVoice": "description of brand voice",
  "targetAudience": ["audience segment 1", "audience segment 2"],
  "valueProposition": "main value proposition",
  "keyMessages": ["message 1", "message 2"],
  "competitiveDifferentiation": "what makes this brand unique",
  "brandPersonality": ["trait 1", "trait 2"]
}
`;

    try {
      const analysis = await retryWithBackoff(async () => {
        const response = await this.anthropic.messages.create({
          model: 'claude-3-sonnet-20240229',
          max_tokens: 2000,
          messages: [{ role: 'user', content: prompt }],
        });

        const content = response.content[0];
        if (content.type === 'text') {
          // Track usage (estimate tokens)
          const estimatedTokens = prompt.length / 4 + content.text.length / 4;
          costTracker.trackAnthropicUsage(this.userId, estimatedTokens);

          return JSON.parse(content.text);
        }

        throw new Error('Invalid response format');
      });

      await this.saveAnalysis(input.brandId, 'positioning', analysis, 0.85);
      return analysis;
    } catch (error) {
      const apiError = handleAPIError(error);
      console.error('Positioning analysis failed:', apiError);
      throw apiError;
    }
  }

  async analyzeVisualIdentity(input: AnalysisInput): Promise<VisualAnalysis> {
    // Filter for visual assets
    const visualAssets = input.assets.filter(asset => 
      asset.type === 'logo' || asset.type === 'image'
    );

    const prompt = `
Analyze the visual identity for ${input.brandName} based on the following:

Website: ${input.websiteUrl}
Visual Assets: ${visualAssets.map(a => `${a.filename} (${a.alt_text || 'no description'})`).join(', ')}
Content Context: ${input.textContent.slice(0, 5).join(' ')}

Please analyze:
1. Color palette (primary and secondary colors)
2. Typography style and characteristics
3. Logo analysis and brand mark evaluation
4. Overall visual style and aesthetic
5. Visual consistency score (0-100)

Format as JSON:
{
  "colorPalette": ["#color1", "#color2"],
  "typography": ["font style 1", "font style 2"],
  "logoAnalysis": "detailed logo analysis",
  "visualStyle": "overall visual style description",
  "consistencyScore": 85
}
`;

    try {
      const response = await this.openai.chat.completions.create({
        model: 'gpt-4-vision-preview',
        messages: [
          {
            role: 'user',
            content: prompt,
          },
        ],
        max_tokens: 1500,
      });

      const content = response.choices[0]?.message?.content;
      if (content) {
        const analysis = JSON.parse(content);
        await this.saveAnalysis(input.brandId, 'visual', analysis, 0.80);
        return analysis;
      }
      
      throw new Error('No response content');
    } catch (error) {
      console.error('Visual analysis failed:', error);
      throw error;
    }
  }

  async analyzeCompetitive(input: AnalysisInput): Promise<CompetitiveAnalysis> {
    const competitors = input.competitors || [];
    
    const prompt = `
Perform a competitive analysis for ${input.brandName} in their market:

Brand: ${input.brandName}
Website: ${input.websiteUrl}
Brand Content: ${input.textContent.join(' ').substring(0, 1000)}
Known Competitors: ${competitors.join(', ')}

Analyze:
1. Direct competitors (similar products/services)
2. Indirect competitors (alternative solutions)
3. Market position relative to competitors
4. Competitive strengths
5. Competitive weaknesses
6. Market opportunities
7. Potential threats

Format as JSON:
{
  "directCompetitors": ["competitor 1", "competitor 2"],
  "indirectCompetitors": ["alternative 1", "alternative 2"],
  "marketPosition": "position description",
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "opportunities": ["opportunity 1", "opportunity 2"],
  "threats": ["threat 1", "threat 2"]
}
`;

    try {
      const response = await this.anthropic.messages.create({
        model: 'claude-3-sonnet-20240229',
        max_tokens: 2000,
        messages: [{ role: 'user', content: prompt }],
      });

      const content = response.content[0];
      if (content.type === 'text') {
        const analysis = JSON.parse(content.text);
        await this.saveAnalysis(input.brandId, 'competitive', analysis, 0.75);
        return analysis;
      }
      
      throw new Error('Invalid response format');
    } catch (error) {
      console.error('Competitive analysis failed:', error);
      throw error;
    }
  }

  async analyzeSentiment(input: AnalysisInput): Promise<SentimentAnalysis> {
    const prompt = `
Analyze the sentiment and emotional tone of ${input.brandName} based on their content:

Brand: ${input.brandName}
Content: ${input.textContent.join('\n')}

Analyze:
1. Overall sentiment (positive, neutral, negative)
2. Emotional tone and mood
3. Brand perception indicators
4. Customer-facing messaging sentiment
5. Emotional appeal strategies

Format as JSON:
{
  "overallSentiment": "positive|neutral|negative",
  "emotionalTone": ["tone 1", "tone 2"],
  "brandPerception": "perception description",
  "customerFeedback": ["insight 1", "insight 2"]
}
`;

    try {
      const response = await this.openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'user',
            content: prompt,
          },
        ],
        max_tokens: 1000,
      });

      const content = response.choices[0]?.message?.content;
      if (content) {
        const analysis = JSON.parse(content);
        await this.saveAnalysis(input.brandId, 'sentiment', analysis, 0.90);
        return analysis;
      }
      
      throw new Error('No response content');
    } catch (error) {
      console.error('Sentiment analysis failed:', error);
      throw error;
    }
  }

  async runFullAnalysis(brandId: string): Promise<{
    positioning?: PositioningAnalysis;
    visual?: VisualAnalysis;
    competitive?: CompetitiveAnalysis;
    sentiment?: SentimentAnalysis;
    errors: string[];
  }> {
    const errors: string[] = [];
    const results: any = {};

    try {
      // Get brand data
      const input = await this.prepareBrandData(brandId);
      
      // Update brand status
      await this.updateBrandStatus(brandId, 'in_progress');

      // Run all analyses
      const analyses = [
        { type: 'positioning', fn: () => this.analyzePositioning(input) },
        { type: 'visual', fn: () => this.analyzeVisualIdentity(input) },
        { type: 'competitive', fn: () => this.analyzeCompetitive(input) },
        { type: 'sentiment', fn: () => this.analyzeSentiment(input) },
      ];

      for (const analysis of analyses) {
        try {
          results[analysis.type] = await analysis.fn();
        } catch (error) {
          errors.push(`${analysis.type} analysis failed: ${error}`);
        }
      }

      // Update brand status
      await this.updateBrandStatus(brandId, 'completed');

    } catch (error) {
      errors.push(`Full analysis failed: ${error}`);
      await this.updateBrandStatus(brandId, 'failed');
    }

    return { ...results, errors };
  }

  private async prepareBrandData(brandId: string): Promise<AnalysisInput> {
    const supabase = createServerSupabase();

    const { data: brand, error } = await supabase
      .from('brands')
      .select(`
        *,
        assets (*),
        projects (
          name,
          brands (name, website_url)
        )
      `)
      .eq('id', brandId)
      .single();

    if (error || !brand) {
      throw new Error('Brand not found');
    }

    // Get competitors from the same project
    const competitors = brand.projects.brands
      ?.filter((b: any) => b.name !== brand.name)
      .map((b: any) => b.name) || [];

    return {
      brandId,
      brandName: brand.name,
      websiteUrl: brand.website_url,
      textContent: [], // Would be populated from scraping results
      assets: brand.assets || [],
      competitors,
    };
  }

  private async saveAnalysis(
    brandId: string,
    type: 'positioning' | 'visual' | 'competitive' | 'sentiment',
    results: any,
    confidenceScore: number
  ): Promise<void> {
    const supabase = createServerSupabase();

    await supabase.from('analyses').insert({
      brand_id: brandId,
      type,
      status: 'completed',
      results,
      confidence_score: confidenceScore,
    });
  }

  private async updateBrandStatus(
    brandId: string,
    status: 'pending' | 'in_progress' | 'completed' | 'failed'
  ): Promise<void> {
    const supabase = createServerSupabase();
    
    await supabase
      .from('brands')
      .update({ 
        analysis_status: status,
        updated_at: new Date().toISOString(),
      })
      .eq('id', brandId);
  }
}
