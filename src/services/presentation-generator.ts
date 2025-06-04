import { createServerSupabase } from '@/lib/supabase-server';
import { uploadFile } from '@/lib/storage';
import type { 
  PositioningAnalysis, 
  VisualAnalysis, 
  CompetitiveAnalysis, 
  SentimentAnalysis 
} from '@/types';

export interface PresentationTemplate {
  id: string;
  name: string;
  description: string;
  slides: SlideTemplate[];
}

export interface SlideTemplate {
  id: string;
  title: string;
  type: 'title' | 'content' | 'comparison' | 'chart' | 'image' | 'conclusion';
  layout: string;
  dataSource?: string;
}

export interface PresentationData {
  projectId: string;
  projectName: string;
  brands: Array<{
    id: string;
    name: string;
    websiteUrl: string;
    logoUrl?: string;
    analyses: {
      positioning?: PositioningAnalysis;
      visual?: VisualAnalysis;
      competitive?: CompetitiveAnalysis;
      sentiment?: SentimentAnalysis;
    };
    assets: Array<{
      type: string;
      url: string;
      filename: string;
    }>;
  }>;
  generatedAt: string;
}

export class PresentationGeneratorService {
  private templates: PresentationTemplate[] = [
    {
      id: 'competitive-analysis',
      name: 'Competitive Analysis Report',
      description: 'Comprehensive competitive brand analysis presentation',
      slides: [
        { id: '1', title: 'Executive Summary', type: 'title', layout: 'title-slide' },
        { id: '2', title: 'Project Overview', type: 'content', layout: 'content-slide', dataSource: 'project' },
        { id: '3', title: 'Brand Landscape', type: 'content', layout: 'grid-slide', dataSource: 'brands' },
        { id: '4', title: 'Positioning Analysis', type: 'comparison', layout: 'comparison-slide', dataSource: 'positioning' },
        { id: '5', title: 'Visual Identity Analysis', type: 'image', layout: 'image-grid-slide', dataSource: 'visual' },
        { id: '6', title: 'Competitive Positioning', type: 'chart', layout: 'chart-slide', dataSource: 'competitive' },
        { id: '7', title: 'Sentiment Analysis', type: 'chart', layout: 'sentiment-slide', dataSource: 'sentiment' },
        { id: '8', title: 'Key Insights', type: 'content', layout: 'insights-slide', dataSource: 'insights' },
        { id: '9', title: 'Recommendations', type: 'content', layout: 'recommendations-slide', dataSource: 'recommendations' },
        { id: '10', title: 'Next Steps', type: 'conclusion', layout: 'conclusion-slide' },
      ],
    },
    {
      id: 'brand-audit',
      name: 'Brand Audit Report',
      description: 'Individual brand audit and analysis',
      slides: [
        { id: '1', title: 'Brand Overview', type: 'title', layout: 'brand-title-slide' },
        { id: '2', title: 'Brand Positioning', type: 'content', layout: 'positioning-slide', dataSource: 'positioning' },
        { id: '3', title: 'Visual Identity', type: 'image', layout: 'visual-slide', dataSource: 'visual' },
        { id: '4', title: 'Digital Presence', type: 'content', layout: 'digital-slide', dataSource: 'assets' },
        { id: '5', title: 'Competitive Analysis', type: 'comparison', layout: 'competitive-slide', dataSource: 'competitive' },
        { id: '6', title: 'Recommendations', type: 'content', layout: 'recommendations-slide', dataSource: 'recommendations' },
      ],
    },
  ];

  async generatePresentation(
    projectId: string,
    templateId: string,
    userId: string
  ): Promise<string> {
    try {
      const supabase = createServerSupabase();

      // Get project data
      const presentationData = await this.gatherPresentationData(projectId);
      
      // Get template
      const template = this.templates.find(t => t.id === templateId);
      if (!template) {
        throw new Error('Template not found');
      }

      // Create presentation record
      const { data: presentation, error: createError } = await supabase
        .from('presentations')
        .insert({
          project_id: projectId,
          name: `${presentationData.projectName} - ${template.name}`,
          template: templateId,
          status: 'generating',
          created_by: userId,
        })
        .select()
        .single();

      if (createError) {
        throw new Error(`Failed to create presentation: ${createError.message}`);
      }

      // Generate slides
      const slides = await this.generateSlides(template, presentationData);

      // Create HTML presentation
      const htmlContent = this.generateHTML(template, slides, presentationData);

      // Upload HTML file
      const filename = `${presentation.id}/presentation.html`;
      await uploadFile('presentations', filename, Buffer.from(htmlContent), {
        contentType: 'text/html',
      });

      // Update presentation with slides data and export URL
      await supabase
        .from('presentations')
        .update({
          status: 'completed',
          slides_data: { slides, template: template.id },
          export_url: `presentations/${filename}`,
          updated_at: new Date().toISOString(),
        })
        .eq('id', presentation.id);

      return presentation.id;

    } catch (error) {
      console.error('Presentation generation failed:', error);
      throw error;
    }
  }

  private async gatherPresentationData(projectId: string): Promise<PresentationData> {
    const supabase = createServerSupabase();

    const { data: project, error } = await supabase
      .from('projects')
      .select(`
        *,
        brands (
          *,
          analyses (*),
          assets (*)
        )
      `)
      .eq('id', projectId)
      .single();

    if (error || !project) {
      throw new Error('Project not found');
    }

    return {
      projectId: project.id,
      projectName: project.name,
      brands: project.brands.map((brand: any) => ({
        id: brand.id,
        name: brand.name,
        websiteUrl: brand.website_url,
        logoUrl: brand.logo_url,
        analyses: this.groupAnalyses(brand.analyses),
        assets: brand.assets || [],
      })),
      generatedAt: new Date().toISOString(),
    };
  }

  private groupAnalyses(analyses: any[]): any {
    return analyses.reduce((acc, analysis) => {
      acc[analysis.type] = analysis.results;
      return acc;
    }, {});
  }

  private async generateSlides(
    template: PresentationTemplate,
    data: PresentationData
  ): Promise<any[]> {
    const slides = [];

    for (const slideTemplate of template.slides) {
      const slide = await this.generateSlide(slideTemplate, data);
      slides.push(slide);
    }

    return slides;
  }

  private async generateSlide(slideTemplate: SlideTemplate, data: PresentationData): Promise<any> {
    const slide = {
      id: slideTemplate.id,
      title: slideTemplate.title,
      type: slideTemplate.type,
      layout: slideTemplate.layout,
      content: {},
    };

    switch (slideTemplate.dataSource) {
      case 'project':
        slide.content = {
          projectName: data.projectName,
          brandCount: data.brands.length,
          generatedAt: new Date(data.generatedAt).toLocaleDateString(),
        };
        break;

      case 'brands':
        slide.content = {
          brands: data.brands.map(brand => ({
            name: brand.name,
            url: brand.websiteUrl,
            logo: brand.logoUrl,
            hasAnalysis: Object.keys(brand.analyses).length > 0,
          })),
        };
        break;

      case 'positioning':
        slide.content = {
          brands: data.brands.map(brand => ({
            name: brand.name,
            positioning: brand.analyses.positioning,
          })).filter(b => b.positioning),
        };
        break;

      case 'visual':
        slide.content = {
          brands: data.brands.map(brand => ({
            name: brand.name,
            visual: brand.analyses.visual,
            assets: brand.assets.filter(a => a.type === 'logo' || a.type === 'image'),
          })).filter(b => b.visual),
        };
        break;

      case 'competitive':
        slide.content = {
          brands: data.brands.map(brand => ({
            name: brand.name,
            competitive: brand.analyses.competitive,
          })).filter(b => b.competitive),
        };
        break;

      case 'sentiment':
        slide.content = {
          brands: data.brands.map(brand => ({
            name: brand.name,
            sentiment: brand.analyses.sentiment,
          })).filter(b => b.sentiment),
        };
        break;

      case 'insights':
        slide.content = {
          insights: this.generateInsights(data),
        };
        break;

      case 'recommendations':
        slide.content = {
          recommendations: this.generateRecommendations(data),
        };
        break;

      default:
        slide.content = {
          title: slideTemplate.title,
          subtitle: `Generated on ${new Date(data.generatedAt).toLocaleDateString()}`,
        };
    }

    return slide;
  }

  private generateInsights(data: PresentationData): string[] {
    const insights = [];

    // Analyze positioning patterns
    const positioningData = data.brands
      .map(b => b.analyses.positioning)
      .filter(Boolean);

    if (positioningData.length > 0) {
      insights.push(`Analyzed ${positioningData.length} brand positioning strategies`);
    }

    // Analyze visual consistency
    const visualData = data.brands
      .map(b => b.analyses.visual)
      .filter(Boolean);

    if (visualData.length > 0) {
      const avgConsistency = visualData.reduce((sum, v) => sum + (v?.consistencyScore || 0), 0) / visualData.length;
      insights.push(`Average visual consistency score: ${avgConsistency.toFixed(1)}%`);
    }

    // Competitive landscape
    const competitiveData = data.brands
      .map(b => b.analyses.competitive)
      .filter(Boolean);

    if (competitiveData.length > 0) {
      insights.push(`Identified competitive landscape across ${competitiveData.length} brands`);
    }

    return insights;
  }

  private generateRecommendations(data: PresentationData): string[] {
    const recommendations = [];

    // Based on analysis results
    data.brands.forEach(brand => {
      if (brand.analyses.visual?.consistencyScore && brand.analyses.visual.consistencyScore < 70) {
        recommendations.push(`${brand.name}: Improve visual consistency across touchpoints`);
      }

      if (brand.analyses.competitive?.weaknesses?.length && brand.analyses.competitive.weaknesses.length > 0) {
        recommendations.push(`${brand.name}: Address competitive weaknesses in positioning`);
      }

      if (brand.analyses.sentiment?.overallSentiment === 'negative') {
        recommendations.push(`${brand.name}: Focus on improving brand sentiment and messaging`);
      }
    });

    if (recommendations.length === 0) {
      recommendations.push('Continue monitoring brand performance and competitive landscape');
      recommendations.push('Regular brand audits recommended every 6 months');
    }

    return recommendations;
  }

  private generateHTML(template: PresentationTemplate, slides: any[], data: PresentationData): string {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${data.projectName} - ${template.name}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        .presentation { max-width: 1200px; margin: 0 auto; }
        .slide { min-height: 100vh; padding: 60px; page-break-after: always; }
        .slide h1 { font-size: 2.5em; color: #2563eb; margin-bottom: 30px; }
        .slide h2 { font-size: 2em; color: #1e40af; margin-bottom: 20px; }
        .slide h3 { font-size: 1.5em; color: #3730a3; margin-bottom: 15px; }
        .brand-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        .brand-card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; }
        .brand-logo { width: 100px; height: 60px; object-fit: contain; margin-bottom: 15px; }
        .insight-list { list-style: none; padding: 0; }
        .insight-list li { background: #f3f4f6; padding: 15px; margin: 10px 0; border-radius: 6px; }
        .footer { text-align: center; color: #6b7280; font-size: 0.9em; margin-top: 40px; }
    </style>
</head>
<body>
    <div class="presentation">
        ${slides.map(slide => this.generateSlideHTML(slide)).join('')}
    </div>
</body>
</html>
    `;
  }

  private generateSlideHTML(slide: any): string {
    switch (slide.type) {
      case 'title':
        return `
          <div class="slide">
            <h1>${slide.title}</h1>
            <h2>${slide.content.subtitle || ''}</h2>
            <div class="footer">Generated by Brand Audit Tool</div>
          </div>
        `;

      case 'content':
        return `
          <div class="slide">
            <h1>${slide.title}</h1>
            ${this.renderContent(slide.content)}
          </div>
        `;

      case 'comparison':
        return `
          <div class="slide">
            <h1>${slide.title}</h1>
            <div class="brand-grid">
              ${slide.content.brands?.map((brand: any) => `
                <div class="brand-card">
                  <h3>${brand.name}</h3>
                  ${this.renderAnalysisData(brand)}
                </div>
              `).join('') || ''}
            </div>
          </div>
        `;

      default:
        return `
          <div class="slide">
            <h1>${slide.title}</h1>
            <p>Content for ${slide.type} slide</p>
          </div>
        `;
    }
  }

  private renderContent(content: any): string {
    if (content.brands) {
      return `
        <div class="brand-grid">
          ${content.brands.map((brand: any) => `
            <div class="brand-card">
              ${brand.logo ? `<img src="${brand.logo}" alt="${brand.name}" class="brand-logo">` : ''}
              <h3>${brand.name}</h3>
              <p><a href="${brand.url}" target="_blank">${brand.url}</a></p>
              <p>Analysis: ${brand.hasAnalysis ? '✅ Complete' : '⏳ Pending'}</p>
            </div>
          `).join('')}
        </div>
      `;
    }

    if (content.insights) {
      return `
        <ul class="insight-list">
          ${content.insights.map((insight: string) => `<li>${insight}</li>`).join('')}
        </ul>
      `;
    }

    if (content.recommendations) {
      return `
        <ul class="insight-list">
          ${content.recommendations.map((rec: string) => `<li>${rec}</li>`).join('')}
        </ul>
      `;
    }

    return `<p>${JSON.stringify(content, null, 2)}</p>`;
  }

  private renderAnalysisData(brand: any): string {
    let html = '';

    if (brand.positioning) {
      html += `
        <h4>Positioning</h4>
        <p><strong>Voice:</strong> ${brand.positioning.brandVoice}</p>
        <p><strong>Value Prop:</strong> ${brand.positioning.valueProposition}</p>
      `;
    }

    if (brand.visual) {
      html += `
        <h4>Visual Identity</h4>
        <p><strong>Style:</strong> ${brand.visual.visualStyle}</p>
        <p><strong>Consistency:</strong> ${brand.visual.consistencyScore}%</p>
      `;
    }

    if (brand.competitive) {
      html += `
        <h4>Competitive Position</h4>
        <p><strong>Position:</strong> ${brand.competitive.marketPosition}</p>
      `;
    }

    return html;
  }
}
