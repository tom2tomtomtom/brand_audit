import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    
    // Create a formatted JSON export
    const exportData = {
      report: {
        metadata: {
          title: 'Brand Analysis Report',
          generatedAt: data.generatedAt || new Date().toISOString(),
          version: '1.0',
          brands: data.brands?.length || 0
        },
        summary: data.summary,
        industry: data.industry,
        competitiveInsights: data.competitiveInsights,
        brands: data.brands
      }
    };

    const jsonString = JSON.stringify(exportData, null, 2);
    
    return new NextResponse(jsonString, {
      headers: {
        'Content-Type': 'application/json',
        'Content-Disposition': `attachment; filename="brand-analysis-${new Date().toISOString().split('T')[0]}.json"`,
      },
    });

  } catch (error) {
    console.error('JSON export error:', error);
    return NextResponse.json(
      { error: 'Failed to generate JSON export' },
      { status: 500 }
    );
  }
}