import { NextRequest, NextResponse } from 'next/server';
import { analyzeWebsite } from '@/lib/websiteAnalyzer';
import { extractVisualAssets } from '@/lib/visualExtractor';
import { generateAIInsights } from '@/lib/aiAnalyzer';

export async function POST(request: NextRequest) {
  try {
    const { brands } = await request.json();

    if (!brands || !Array.isArray(brands) || brands.length === 0) {
      return NextResponse.json(
        { error: 'Please provide an array of brands to analyze' },
        { status: 400 }
      );
    }

    console.log(`🚀 Starting REAL analysis for ${brands.length} brands:`, brands);

    const analysisResults = [];

    for (const brandInput of brands) {
      try {
        console.log(`🔍 Analyzing brand: ${brandInput}`);
        
        // Normalize brand input (handle both "company.com" and "Company Name" formats)
        const website = brandInput.toLowerCase().includes('.') 
          ? (brandInput.startsWith('http') ? brandInput : `https://${brandInput}`)
          : `https://${brandInput.toLowerCase().replace(/\s+/g, '')}.com`;

        const brandName = brandInput.includes('.') 
          ? brandInput.split('.')[0] 
          : brandInput;

        // 1. Analyze website structure and content
        console.log(`Step 1: Analyzing website structure for ${brandName}`);
        const websiteData = await analyzeWebsite(website);
        console.log(`Website data extracted:`, {
          title: websiteData.title || 'No title',
          description: websiteData.metaDescription ? 'Found' : 'None',
          contentLength: websiteData.content?.length || 0,
          industry: websiteData.detectedIndustry || 'Not detected'
        });

        // 2. Extract visual assets (logos, colors, fonts)
        console.log(`Step 2: Extracting visual assets for ${brandName}`);
        const visualAssets = await extractVisualAssets(website, websiteData);
        console.log(`Visual assets:`, {
          logo: visualAssets.logo ? 'Found' : 'None',
          colors: visualAssets.colors?.length || 0,
          fonts: visualAssets.fonts?.length || 0
        });

        // 3. Generate AI-powered insights
        console.log(`Step 3: Generating AI insights for ${brandName}`);
        const aiInsights = await generateAIInsights(websiteData, visualAssets, brandName);
        console.log(`AI insights generated:`, {
          hasOverallScore: !!aiInsights.overallScore,
          hasIndustry: !!aiInsights.industry,
          hasDescription: !!aiInsights.description
        });

        // 4. Compile comprehensive brand analysis
        const brandAnalysis = {
          name: brandName,
          website: website,
          score: aiInsights.overallScore || null, // Only real scores
          error: undefined, // Explicitly add error property
          
          // Company Overview - ONLY real data
          overview: {
            industry: aiInsights.industry || websiteData.detectedIndustry || null,
            description: aiInsights.description || websiteData.metaDescription || null,
            founded: aiInsights.founded || null,
            revenue: aiInsights.revenue || null,
            employees: aiInsights.employees || null,
          },

          // Brand Positioning - ONLY real data
          positioning: {
            statement: aiInsights.positioning || null,
            valueProposition: aiInsights.valueProposition || null,
            targetAudience: aiInsights.targetAudience || null,
            personality: aiInsights.brandPersonality || null,
            marketPosition: aiInsights.marketPosition || null,
          },

          // Digital Presence Scores - ONLY real analysis
          digital: {
            seoScore: aiInsights.seoScore || null,
            uxScore: aiInsights.uxScore || null,
            socialScore: aiInsights.socialScore || null,
            contentScore: aiInsights.contentScore || null,
          },

          // Visual Identity - ONLY real extracted data  
          visual: {
            logo: visualAssets.logo || null,
            colors: visualAssets.colors || [],
            fonts: visualAssets.fonts || [],
            screenshots: visualAssets.screenshots || [],
          },

          // SWOT Analysis - ONLY real AI analysis
          strengths: aiInsights.strengths || [],
          weaknesses: aiInsights.weaknesses || [],
          opportunities: aiInsights.opportunities || [],
          threats: aiInsights.threats || [],
          recommendations: aiInsights.recommendations || [],

          // Recent Brand Work (from content analysis)
          recentWork: websiteData.recentContent || [],
          
          // Analysis metadata
          analyzedAt: new Date().toISOString(),
          analysisVersion: '1.0'
        };

        analysisResults.push(brandAnalysis);
        console.log(`Completed analysis for ${brandName}`);

      } catch (brandError) {
        console.error(`Error analyzing brand ${brandInput}:`, brandError);
        
        // Add error entry but continue with other brands
        analysisResults.push({
          name: brandInput,
          website: brandInput,
          score: 0,
          error: `Failed to analyze: ${brandError instanceof Error ? brandError.message : 'Unknown error'}`,
          analyzedAt: new Date().toISOString()
        });
      }
    }

    // Generate competitive insights
    const competitiveInsights = generateCompetitiveInsights(analysisResults.filter((r) => !r.error));

    const finalReport = {
      brands: analysisResults,
      industry: detectOverallIndustry(analysisResults),
      competitiveInsights,
      summary: {
        totalBrands: analysisResults.length,
        successfulAnalyses: analysisResults.filter((r) => !r.error).length,
        averageScore: null, // No fake average scores
        analysisDate: new Date().toISOString(),
      },
      generatedAt: new Date().toISOString()
    };

    console.log('Analysis complete:', finalReport.summary);
    return NextResponse.json(finalReport);

  } catch (error) {
    console.error('Analysis failed:', error);
    return NextResponse.json(
      { error: `Analysis failed: ${error instanceof Error ? error.message : 'Unknown error'}` },
      { status: 500 }
    );
  }
}

interface BrandAnalysis {
  name: string;
  website?: string;
  score: number;
  error?: string;
  digital?: {
    seoScore?: number;
    uxScore?: number;
    socialScore?: number;
    contentScore?: number;
  };
  overview?: {
    industry?: string;
    description?: string;
    founded?: string;
    revenue?: string;
    employees?: string;
  };
  positioning?: any;
  visual?: any;
  strengths?: string[];
  weaknesses?: string[];
  opportunities?: string[];
  threats?: string[];
  recommendations?: string[];
  recentWork?: any[];
  analyzedAt?: string;
  analysisVersion?: string;
}

function generateCompetitiveInsights(brands: any[]): string[] {
  if (brands.length === 0) return ['No successful analyses to compare'];
  
  const insights = [];
  
  if (brands.length > 1) {
    const topBrand = brands.reduce((top, current) => 
      current.score > top.score ? current : top
    );
    insights.push(`${topBrand.name} leads the competitive analysis with a score of ${topBrand.score}/100`);
    
    const avgScore = Math.round(brands.reduce((sum, brand) => sum + brand.score, 0) / brands.length);
    insights.push(`Average competitive score across analyzed brands is ${avgScore}/100`);
    
    if (brands.some(b => b.digital?.seoScore >= 8)) {
      const seoLeader = brands.reduce((top, current) => 
        (current.digital?.seoScore || 0) > (top.digital?.seoScore || 0) ? current : top
      );
      insights.push(`${seoLeader.name} demonstrates strongest SEO performance`);
    }
    
    insights.push('Market shows opportunities for digital experience enhancement and brand differentiation');
  } else {
    insights.push(`Analysis of ${brands[0].name} reveals strong market positioning opportunities`);
    insights.push('Single brand analysis provides foundation for competitive benchmarking');
  }
  
  return insights;
}

function detectOverallIndustry(brands: any[]): string {
  const industries = brands
    .filter((b) => b.overview?.industry)
    .map((b) => b.overview!.industry);
  
  if (industries.length === 0) return 'Multi-industry';
  
  // Find most common industry
  const industryCount = industries.reduce((acc, industry) => {
    acc[industry] = (acc[industry] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return Object.entries(industryCount)
    .sort(([,a], [,b]) => (b as number) - (a as number))[0][0] || 'Multi-industry';
}