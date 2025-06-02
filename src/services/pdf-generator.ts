import puppeteer from 'puppeteer';
import { createServerSupabase } from '@/lib/supabase-server';
import { uploadFile } from '@/lib/storage';

export class PDFGeneratorService {
  async generatePresentationPDF(presentationId: string): Promise<string> {
    const supabase = createServerSupabase();
    
    // Get presentation data
    const { data: presentation, error } = await supabase
      .from('presentations')
      .select('*')
      .eq('id', presentationId)
      .single();

    if (error || !presentation) {
      throw new Error('Presentation not found');
    }

    if (!presentation.export_url) {
      throw new Error('Presentation HTML not available');
    }

    // Get HTML content from storage
    const { data: htmlFile, error: fileError } = await supabase.storage
      .from('presentations')
      .download(presentation.export_url.replace('presentations/', ''));

    if (fileError || !htmlFile) {
      throw new Error('Failed to load presentation HTML');
    }

    const htmlContent = await htmlFile.text();

    // Launch Puppeteer
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    try {
      const page = await browser.newPage();
      
      // Set page size for presentation format
      await page.setViewport({ width: 1920, height: 1080 });
      
      // Load HTML content
      await page.setContent(htmlContent, {
        waitUntil: 'networkidle0',
        timeout: 30000,
      });

      // Add print styles
      await page.addStyleTag({
        content: `
          @media print {
            .slide {
              page-break-after: always;
              min-height: 100vh;
              display: flex;
              flex-direction: column;
              justify-content: center;
              padding: 40px;
            }
            .slide:last-child {
              page-break-after: avoid;
            }
            body {
              margin: 0;
              padding: 0;
            }
          }
        `,
      });

      // Generate PDF
      const pdfBuffer = await page.pdf({
        format: 'A4',
        landscape: true,
        printBackground: true,
        margin: {
          top: '20px',
          right: '20px',
          bottom: '20px',
          left: '20px',
        },
      });

      // Upload PDF to storage
      const filename = `${presentationId}/presentation.pdf`;
      await uploadFile('presentations', filename, pdfBuffer, {
        contentType: 'application/pdf',
      });

      // Update presentation record
      await supabase
        .from('presentations')
        .update({
          pdf_url: `presentations/${filename}`,
          updated_at: new Date().toISOString(),
        })
        .eq('id', presentationId);

      return filename;

    } finally {
      await browser.close();
    }
  }

  async generateBrandReportPDF(brandId: string): Promise<string> {
    const supabase = createServerSupabase();
    
    // Get brand data with analyses
    const { data: brand, error } = await supabase
      .from('brands')
      .select(`
        *,
        analyses (*),
        assets (*),
        projects (
          name,
          organizations (name)
        )
      `)
      .eq('id', brandId)
      .single();

    if (error || !brand) {
      throw new Error('Brand not found');
    }

    // Generate HTML report
    const htmlContent = this.generateBrandReportHTML(brand);

    // Launch Puppeteer
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    try {
      const page = await browser.newPage();
      
      await page.setViewport({ width: 1200, height: 800 });
      
      await page.setContent(htmlContent, {
        waitUntil: 'networkidle0',
        timeout: 30000,
      });

      // Generate PDF
      const pdfBuffer = await page.pdf({
        format: 'A4',
        printBackground: true,
        margin: {
          top: '40px',
          right: '40px',
          bottom: '40px',
          left: '40px',
        },
      });

      // Upload PDF to storage
      const filename = `brands/${brandId}/report.pdf`;
      await uploadFile('presentations', filename, pdfBuffer, {
        contentType: 'application/pdf',
      });

      return filename;

    } finally {
      await browser.close();
    }
  }

  private generateBrandReportHTML(brand: any): string {
    const analyses = brand.analyses || [];
    const positioning = analyses.find((a: any) => a.type === 'positioning');
    const visual = analyses.find((a: any) => a.type === 'visual');
    const competitive = analyses.find((a: any) => a.type === 'competitive');
    const sentiment = analyses.find((a: any) => a.type === 'sentiment');

    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${brand.name} - Brand Analysis Report</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 40px; 
            line-height: 1.6;
            color: #333;
        }
        .header { 
            text-align: center; 
            margin-bottom: 40px; 
            border-bottom: 2px solid #2563eb;
            padding-bottom: 20px;
        }
        .header h1 { 
            color: #2563eb; 
            margin: 0;
            font-size: 2.5em;
        }
        .header p { 
            color: #666; 
            margin: 10px 0 0 0;
            font-size: 1.1em;
        }
        .section { 
            margin-bottom: 40px; 
            page-break-inside: avoid;
        }
        .section h2 { 
            color: #1e40af; 
            border-left: 4px solid #2563eb;
            padding-left: 15px;
            margin-bottom: 20px;
        }
        .analysis-grid { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 30px; 
        }
        .analysis-card { 
            border: 1px solid #e5e7eb; 
            border-radius: 8px; 
            padding: 20px;
            background: #f9fafb;
        }
        .analysis-card h3 { 
            color: #3730a3; 
            margin-top: 0;
        }
        .status-badge { 
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .status-completed { 
            background: #dcfce7; 
            color: #166534; 
        }
        .status-pending { 
            background: #fef3c7; 
            color: #92400e; 
        }
        .status-failed { 
            background: #fee2e2; 
            color: #991b1b; 
        }
        .footer { 
            text-align: center; 
            color: #6b7280; 
            font-size: 0.9em; 
            margin-top: 60px;
            border-top: 1px solid #e5e7eb;
            padding-top: 20px;
        }
        ul { 
            padding-left: 20px; 
        }
        li { 
            margin-bottom: 5px; 
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>${brand.name}</h1>
        <p>Brand Analysis Report</p>
        <p>${brand.website_url}</p>
        <p>Generated on ${new Date().toLocaleDateString()}</p>
    </div>

    <div class="section">
        <h2>Brand Overview</h2>
        <p><strong>Industry:</strong> ${brand.industry || 'Not specified'}</p>
        <p><strong>Description:</strong> ${brand.description || 'No description provided'}</p>
        <p><strong>Scraping Status:</strong> <span class="status-badge status-${brand.scraping_status}">${brand.scraping_status}</span></p>
        <p><strong>Analysis Status:</strong> <span class="status-badge status-${brand.analysis_status}">${brand.analysis_status}</span></p>
        <p><strong>Assets Collected:</strong> ${brand.assets?.length || 0}</p>
    </div>

    <div class="section">
        <h2>Analysis Results</h2>
        <div class="analysis-grid">
            ${positioning ? `
            <div class="analysis-card">
                <h3>Brand Positioning</h3>
                <p><strong>Status:</strong> <span class="status-badge status-${positioning.status}">${positioning.status}</span></p>
                ${positioning.results ? `
                <p><strong>Brand Voice:</strong> ${positioning.results.brandVoice || 'Not analyzed'}</p>
                <p><strong>Value Proposition:</strong> ${positioning.results.valueProposition || 'Not analyzed'}</p>
                <p><strong>Target Audience:</strong></p>
                <ul>
                    ${positioning.results.targetAudience?.map((audience: string) => `<li>${audience}</li>`).join('') || '<li>Not analyzed</li>'}
                </ul>
                ` : '<p>Analysis not completed</p>'}
            </div>
            ` : '<div class="analysis-card"><h3>Brand Positioning</h3><p>Not analyzed</p></div>'}

            ${visual ? `
            <div class="analysis-card">
                <h3>Visual Identity</h3>
                <p><strong>Status:</strong> <span class="status-badge status-${visual.status}">${visual.status}</span></p>
                ${visual.results ? `
                <p><strong>Visual Style:</strong> ${visual.results.visualStyle || 'Not analyzed'}</p>
                <p><strong>Consistency Score:</strong> ${visual.results.consistencyScore || 'N/A'}%</p>
                <p><strong>Color Palette:</strong> ${visual.results.colorPalette?.join(', ') || 'Not analyzed'}</p>
                ` : '<p>Analysis not completed</p>'}
            </div>
            ` : '<div class="analysis-card"><h3>Visual Identity</h3><p>Not analyzed</p></div>'}

            ${competitive ? `
            <div class="analysis-card">
                <h3>Competitive Analysis</h3>
                <p><strong>Status:</strong> <span class="status-badge status-${competitive.status}">${competitive.status}</span></p>
                ${competitive.results ? `
                <p><strong>Market Position:</strong> ${competitive.results.marketPosition || 'Not analyzed'}</p>
                <p><strong>Key Strengths:</strong></p>
                <ul>
                    ${competitive.results.strengths?.map((strength: string) => `<li>${strength}</li>`).join('') || '<li>Not analyzed</li>'}
                </ul>
                ` : '<p>Analysis not completed</p>'}
            </div>
            ` : '<div class="analysis-card"><h3>Competitive Analysis</h3><p>Not analyzed</p></div>'}

            ${sentiment ? `
            <div class="analysis-card">
                <h3>Sentiment Analysis</h3>
                <p><strong>Status:</strong> <span class="status-badge status-${sentiment.status}">${sentiment.status}</span></p>
                ${sentiment.results ? `
                <p><strong>Overall Sentiment:</strong> ${sentiment.results.overallSentiment || 'Not analyzed'}</p>
                <p><strong>Brand Perception:</strong> ${sentiment.results.brandPerception || 'Not analyzed'}</p>
                ` : '<p>Analysis not completed</p>'}
            </div>
            ` : '<div class="analysis-card"><h3>Sentiment Analysis</h3><p>Not analyzed</p></div>'}
        </div>
    </div>

    <div class="footer">
        <p>Generated by Brand Audit Tool</p>
        <p>Project: ${brand.projects?.name || 'Unknown'} | Organization: ${brand.projects?.organizations?.name || 'Unknown'}</p>
    </div>
</body>
</html>
    `;
  }
}
