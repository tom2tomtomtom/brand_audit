import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    
    const htmlReport = generateHTMLReport(data);
    
    return new NextResponse(htmlReport, {
      headers: {
        'Content-Type': 'text/html',
        'Content-Disposition': `attachment; filename="brand-analysis-${new Date().toISOString().split('T')[0]}.html"`,
      },
    });

  } catch (error) {
    console.error('HTML export error:', error);
    return NextResponse.json(
      { error: 'Failed to generate HTML export' },
      { status: 500 }
    );
  }
}

interface ReportData {
  brands: BrandAnalysis[];
  competitiveInsights: string[];
  summary?: {
    averageScore?: number;
  };
  industry?: string;
}

interface BrandAnalysis {
  name: string;
  website?: string;
  score: number;
  error?: string;
  overview?: {
    industry?: string;
    description?: string;
    revenue?: string;
    employees?: string;
    founded?: string;
  };
  positioning?: {
    statement?: string;
    valueProposition?: string;
    targetAudience?: string;
    personality?: string;
  };
  digital?: {
    seoScore?: number;
    uxScore?: number;
    socialScore?: number;
    contentScore?: number;
  };
  visual?: {
    logo?: string;
    colors?: string[];
  };
  strengths?: string[];
  weaknesses?: string[];
  opportunities?: string[];
  threats?: string[];
  recommendations?: string[];
}

function generateHTMLReport(data: ReportData): string {
  const brands = data.brands || [];
  const competitiveInsights = data.competitiveInsights || [];
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brand Analysis Report - ${new Date().toLocaleDateString()}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6; 
            color: #333; 
            background: #f8fafc;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .content { padding: 40px; }
        .section { margin-bottom: 40px; }
        .section h2 { color: #2d3748; font-size: 1.8rem; margin-bottom: 20px; border-bottom: 3px solid #4299e1; padding-bottom: 10px; }
        .section h3 { color: #4a5568; font-size: 1.4rem; margin-bottom: 15px; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .summary-card { background: #f7fafc; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #4299e1; }
        .summary-card .number { font-size: 2rem; font-weight: bold; color: #2b6cb0; }
        .summary-card .label { color: #718096; margin-top: 5px; }
        .brand-card { background: #f8f9fa; border: 1px solid #e2e8f0; border-radius: 8px; padding: 30px; margin-bottom: 30px; }
        .brand-header { display: flex; justify-content: between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; }
        .brand-name { font-size: 1.6rem; font-weight: bold; color: #2d3748; }
        .brand-score { font-size: 1.8rem; font-weight: bold; padding: 10px 20px; border-radius: 50px; color: white; }
        .score-high { background: #38a169; }
        .score-medium { background: #d69e2e; }
        .score-low { background: #e53e3e; }
        .brand-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .brand-section { background: white; padding: 20px; border-radius: 6px; border-left: 4px solid #4299e1; }
        .brand-section h4 { color: #2d3748; margin-bottom: 10px; font-size: 1.1rem; }
        .brand-section ul { list-style: none; }
        .brand-section li { padding: 4px 0; }
        .brand-section li:before { content: "•"; color: #4299e1; margin-right: 8px; }
        .visual-section { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .color-palette { display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap; }
        .color-swatch { width: 40px; height: 40px; border-radius: 4px; border: 2px solid #e2e8f0; display: flex; align-items: center; justify-content: center; color: white; font-size: 10px; text-shadow: 1px 1px 1px rgba(0,0,0,0.5); }
        .insights-list { background: #edf2f7; padding: 20px; border-radius: 6px; }
        .insights-list li { padding: 8px 0; border-bottom: 1px solid #cbd5e0; }
        .insights-list li:last-child { border-bottom: none; }
        .logo-display { text-align: center; margin: 20px 0; }
        .logo-display img { max-height: 60px; max-width: 200px; object-fit: contain; background: white; padding: 10px; border-radius: 4px; border: 1px solid #e2e8f0; }
        @media print { body { background: white; padding: 0; } .container { box-shadow: none; } }
        @media (max-width: 768px) { .brand-header { flex-direction: column; align-items: flex-start; gap: 15px; } .summary-grid, .brand-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Brand Analysis Report</h1>
            <p>Comprehensive competitive analysis • Generated ${new Date().toLocaleDateString()}</p>
        </div>
        
        <div class="content">
            <!-- Executive Summary -->
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="number">${brands.length}</div>
                        <div class="label">Brands Analyzed</div>
                    </div>
                    <div class="summary-card">
                        <div class="number">${data.summary?.averageScore || 'N/A'}/100</div>
                        <div class="label">Average Score</div>
                    </div>
                    <div class="summary-card">
                        <div class="number">${data.industry || 'Multi-industry'}</div>
                        <div class="label">Industry Focus</div>
                    </div>
                    <div class="summary-card">
                        <div class="number">${new Date().toLocaleDateString()}</div>
                        <div class="label">Analysis Date</div>
                    </div>
                </div>
                
                ${competitiveInsights.length > 0 ? `
                <h3>🎯 Key Competitive Insights</h3>
                <div class="insights-list">
                    <ul>
                        ${competitiveInsights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
            </div>

            <!-- Brand Profiles -->
            <div class="section">
                <h2>🏢 Brand Analysis Profiles</h2>
                ${brands.map(brand => `
                    <div class="brand-card">
                        <div class="brand-header">
                            <div>
                                ${brand.visual?.logo ? `
                                <div class="logo-display">
                                    <img src="${brand.visual.logo}" alt="${brand.name} logo" />
                                </div>
                                ` : ''}
                                <div class="brand-name">${brand.name}</div>
                                <div style="color: #718096; margin-top: 5px;">${brand.website || ''}</div>
                            </div>
                            <div class="brand-score ${
                                brand.score >= 80 ? 'score-high' : 
                                brand.score >= 60 ? 'score-medium' : 'score-low'
                            }">
                                ${brand.score || 'N/A'}/100
                            </div>
                        </div>

                        ${brand.overview ? `
                        <div style="background: #edf2f7; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
                            <h4 style="color: #2d3748; margin-bottom: 10px;">Company Overview</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.9rem;">
                                <div><strong>Industry:</strong> ${brand.overview.industry || 'Not specified'}</div>
                                <div><strong>Revenue:</strong> ${brand.overview.revenue || 'Not specified'}</div>
                                <div><strong>Employees:</strong> ${brand.overview.employees || 'Not specified'}</div>
                                <div><strong>Founded:</strong> ${brand.overview.founded || 'Not specified'}</div>
                            </div>
                            ${brand.overview.description ? `<p style="margin-top: 10px; color: #4a5568;">${brand.overview.description}</p>` : ''}
                        </div>
                        ` : ''}

                        ${brand.positioning ? `
                        <div style="background: #f0fff4; padding: 15px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #38a169;">
                            <h4 style="color: #2f855a; margin-bottom: 10px;">Brand Positioning</h4>
                            <div style="font-size: 0.9rem; line-height: 1.5;">
                                <div style="margin-bottom: 8px;"><strong>Positioning:</strong> ${brand.positioning.statement || 'Not analyzed'}</div>
                                <div style="margin-bottom: 8px;"><strong>Value Proposition:</strong> ${brand.positioning.valueProposition || 'Not analyzed'}</div>
                                <div style="margin-bottom: 8px;"><strong>Target Audience:</strong> ${brand.positioning.targetAudience || 'Not analyzed'}</div>
                                <div><strong>Brand Personality:</strong> ${brand.positioning.personality || 'Not analyzed'}</div>
                            </div>
                        </div>
                        ` : ''}

                        ${brand.digital ? `
                        <div style="background: #ebf8ff; padding: 15px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #3182ce;">
                            <h4 style="color: #2c5282; margin-bottom: 10px;">Digital Presence Scores</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; text-align: center;">
                                <div>
                                    <div style="font-size: 1.5rem; font-weight: bold; color: #3182ce;">${brand.digital.seoScore || 'N/A'}/10</div>
                                    <div style="font-size: 0.8rem; color: #4a5568;">SEO Score</div>
                                </div>
                                <div>
                                    <div style="font-size: 1.5rem; font-weight: bold; color: #3182ce;">${brand.digital.uxScore || 'N/A'}/10</div>
                                    <div style="font-size: 0.8rem; color: #4a5568;">UX Score</div>
                                </div>
                                <div>
                                    <div style="font-size: 1.5rem; font-weight: bold; color: #3182ce;">${brand.digital.socialScore || 'N/A'}/10</div>
                                    <div style="font-size: 0.8rem; color: #4a5568;">Social Score</div>
                                </div>
                                <div>
                                    <div style="font-size: 1.5rem; font-weight: bold; color: #3182ce;">${brand.digital.contentScore || 'N/A'}/10</div>
                                    <div style="font-size: 0.8rem; color: #4a5568;">Content Score</div>
                                </div>
                            </div>
                        </div>
                        ` : ''}

                        ${brand.visual?.colors ? `
                        <div style="background: #faf5ff; padding: 15px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #805ad5;">
                            <h4 style="color: #553c9a; margin-bottom: 10px;">Brand Colors</h4>
                            <div class="color-palette">
                                ${brand.visual.colors.map(color => `
                                    <div class="color-swatch" style="background-color: ${color};" title="${color}">${color}</div>
                                `).join('')}
                            </div>
                        </div>
                        ` : ''}

                        <div class="brand-grid">
                            <div class="brand-section" style="border-left-color: #38a169;">
                                <h4>✅ Strengths</h4>
                                <ul>
                                    ${(brand.strengths || ['No strengths identified']).map(strength => `<li>${strength}</li>`).join('')}
                                </ul>
                            </div>
                            
                            <div class="brand-section" style="border-left-color: #e53e3e;">
                                <h4>⚠️ Areas for Improvement</h4>
                                <ul>
                                    ${(brand.weaknesses || ['No weaknesses identified']).map(weakness => `<li>${weakness}</li>`).join('')}
                                </ul>
                            </div>
                            
                            <div class="brand-section" style="border-left-color: #3182ce;">
                                <h4>🌟 Opportunities</h4>
                                <ul>
                                    ${(brand.opportunities || ['No opportunities identified']).map(opportunity => `<li>${opportunity}</li>`).join('')}
                                </ul>
                            </div>
                            
                            <div class="brand-section" style="border-left-color: #d69e2e;">
                                <h4>⚡ Threats</h4>
                                <ul>
                                    ${(brand.threats || ['No threats identified']).map(threat => `<li>${threat}</li>`).join('')}
                                </ul>
                            </div>
                        </div>

                        ${brand.recommendations ? `
                        <div style="background: #f0fff4; padding: 15px; border-radius: 6px; margin-top: 20px; border-left: 4px solid #38a169;">
                            <h4 style="color: #2f855a; margin-bottom: 10px;">💡 Strategic Recommendations</h4>
                            <ul style="list-style: none;">
                                ${brand.recommendations.map(rec => `<li style="padding: 4px 0;"><span style="color: #38a169; margin-right: 8px;">•</span>${rec}</li>`).join('')}
                            </ul>
                        </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>

            <!-- Footer -->
            <div style="text-align: center; padding: 30px; border-top: 1px solid #e2e8f0; color: #718096; font-size: 0.9rem;">
                <p>Generated by Universal Brand Audit Tool • ${new Date().toLocaleDateString()}</p>
                <p style="margin-top: 5px;">Comprehensive brand analysis and competitive intelligence</p>
            </div>
        </div>
    </div>
</body>
</html>`;
}