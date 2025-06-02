import { test, expect } from '@playwright/test';

test.describe('Project Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock authentication
    await page.addInitScript(() => {
      localStorage.setItem('supabase.auth.token', JSON.stringify({
        access_token: 'mock-token',
        user: { id: 'test-user-id', email: 'test@example.com' }
      }));
    });

    // Mock API responses
    await page.route('**/api/projects', async route => {
      if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            projects: [
              {
                id: 'project-1',
                name: 'Test Project',
                description: 'Test description',
                brand_count: 2,
                completed_analyses: 1,
                created_at: '2024-01-01T00:00:00Z'
              }
            ]
          })
        });
      } else if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 201,
          contentType: 'application/json',
          body: JSON.stringify({
            project: {
              id: 'new-project-id',
              name: 'New Project',
              description: 'New project description',
              brands: []
            }
          })
        });
      }
    });

    await page.goto('/dashboard');
  });

  test('should display dashboard with projects', async ({ page }) => {
    await expect(page.getByText('Dashboard')).toBeVisible();
    await expect(page.getByText('Test Project')).toBeVisible();
    await expect(page.getByText('2 brands')).toBeVisible();
  });

  test('should create new project', async ({ page }) => {
    await page.getByRole('button', { name: /new project/i }).click();
    
    await expect(page.getByText('Create New Project')).toBeVisible();
    
    // Fill project form
    await page.getByLabel('Project Name').fill('E2E Test Project');
    await page.getByLabel('Description').fill('End-to-end test project');
    
    // Add first brand
    await page.getByLabel('Brand Name').first().fill('Nike');
    await page.getByLabel('Website URL').first().fill('https://nike.com');
    await page.getByLabel('Industry').first().fill('Sports & Fashion');
    
    // Add second brand
    await page.getByRole('button', { name: /add another brand/i }).click();
    await page.getByLabel('Brand Name').nth(1).fill('Adidas');
    await page.getByLabel('Website URL').nth(1).fill('https://adidas.com');
    
    // Submit form
    await page.getByRole('button', { name: /create project/i }).click();
    
    // Should redirect to project page
    await expect(page).toHaveURL(/\/projects\/new-project-id/);
  });

  test('should validate project form', async ({ page }) => {
    await page.getByRole('button', { name: /new project/i }).click();
    
    // Try to submit empty form
    await page.getByRole('button', { name: /create project/i }).click();
    
    await expect(page.getByText('Project name is required')).toBeVisible();
    await expect(page.getByText('At least one brand is required')).toBeVisible();
  });

  test('should validate brand URLs', async ({ page }) => {
    await page.getByRole('button', { name: /new project/i }).click();
    
    await page.getByLabel('Project Name').fill('Test Project');
    await page.getByLabel('Brand Name').first().fill('Test Brand');
    await page.getByLabel('Website URL').first().fill('invalid-url');
    
    await page.getByRole('button', { name: /create project/i }).click();
    
    await expect(page.getByText('Valid URL is required')).toBeVisible();
  });

  test('should navigate to project details', async ({ page }) => {
    // Mock project details API
    await page.route('**/api/projects/project-1', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          project: {
            id: 'project-1',
            name: 'Test Project',
            description: 'Test description',
            brands: [
              {
                id: 'brand-1',
                name: 'Nike',
                website_url: 'https://nike.com',
                status: 'pending',
                scraping_status: 'pending',
                analysis_status: 'pending'
              }
            ]
          }
        })
      });
    });

    await page.getByText('Test Project').click();
    
    await expect(page).toHaveURL('/projects/project-1');
    await expect(page.getByText('Test Project')).toBeVisible();
    await expect(page.getByText('Nike')).toBeVisible();
  });

  test('should start brand scraping', async ({ page }) => {
    // Navigate to project details
    await page.route('**/api/projects/project-1', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          project: {
            id: 'project-1',
            name: 'Test Project',
            brands: [
              {
                id: 'brand-1',
                name: 'Nike',
                website_url: 'https://nike.com',
                status: 'pending',
                scraping_status: 'pending'
              }
            ]
          }
        })
      });
    });

    // Mock scraping API
    await page.route('**/api/scraping', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          message: 'Scraping started',
          jobId: 'scraping-job-1'
        })
      });
    });

    await page.goto('/projects/project-1');
    
    await page.getByRole('button', { name: /start scraping/i }).first().click();
    
    await expect(page.getByText('Scraping started')).toBeVisible();
  });

  test('should start AI analysis', async ({ page }) => {
    // Mock project with completed scraping
    await page.route('**/api/projects/project-1', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          project: {
            id: 'project-1',
            name: 'Test Project',
            brands: [
              {
                id: 'brand-1',
                name: 'Nike',
                website_url: 'https://nike.com',
                status: 'completed',
                scraping_status: 'completed',
                analysis_status: 'pending'
              }
            ]
          }
        })
      });
    });

    // Mock analysis API
    await page.route('**/api/analysis', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          message: 'Analysis started',
          jobId: 'analysis-job-1'
        })
      });
    });

    await page.goto('/projects/project-1');
    
    await page.getByRole('button', { name: /start analysis/i }).first().click();
    
    await expect(page.getByText('Analysis started')).toBeVisible();
  });

  test('should view analysis results', async ({ page }) => {
    // Mock analysis results API
    await page.route('**/api/brands/brand-1/analyses', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          brand: {
            id: 'brand-1',
            name: 'Nike',
            websiteUrl: 'https://nike.com'
          },
          analyses: {
            positioning: {
              brandVoice: 'Inspirational and empowering',
              targetAudience: 'Athletes and fitness enthusiasts',
              valueProposition: 'Just Do It mentality'
            },
            visual: {
              colorPalette: ['#000000', '#FFFFFF'],
              consistencyScore: 95
            }
          }
        })
      });
    });

    await page.goto('/brands/brand-1/results');
    
    await expect(page.getByText('Nike')).toBeVisible();
    await expect(page.getByText('Inspirational and empowering')).toBeVisible();
    await expect(page.getByText('95')).toBeVisible(); // Consistency score
  });

  test('should generate presentation', async ({ page }) => {
    // Mock presentation generation API
    await page.route('**/api/presentations', async route => {
      await route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({
          presentation: {
            id: 'presentation-1',
            name: 'Test Project Report',
            status: 'completed',
            export_url: '/presentations/test-report.html'
          }
        })
      });
    });

    await page.goto('/projects/project-1');
    
    await page.getByRole('button', { name: /generate report/i }).click();
    
    // Fill presentation form
    await page.getByLabel('Report Name').fill('Q1 Competitive Analysis');
    await page.getByRole('button', { name: /generate presentation/i }).click();
    
    await expect(page.getByText('Presentation generated successfully')).toBeVisible();
  });

  test('should handle errors gracefully', async ({ page }) => {
    // Mock API error
    await page.route('**/api/projects', async route => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({
            error: 'Internal server error'
          })
        });
      }
    });

    await page.getByRole('button', { name: /new project/i }).click();
    
    await page.getByLabel('Project Name').fill('Test Project');
    await page.getByLabel('Brand Name').first().fill('Test Brand');
    await page.getByLabel('Website URL').first().fill('https://test.com');
    
    await page.getByRole('button', { name: /create project/i }).click();
    
    await expect(page.getByText('Failed to create project')).toBeVisible();
  });

  test('should show loading states', async ({ page }) => {
    // Mock delayed API response
    await page.route('**/api/projects', async route => {
      if (route.request().method() === 'POST') {
        await new Promise(resolve => setTimeout(resolve, 1000));
        await route.fulfill({
          status: 201,
          contentType: 'application/json',
          body: JSON.stringify({ project: { id: 'new-project' } })
        });
      }
    });

    await page.getByRole('button', { name: /new project/i }).click();
    
    await page.getByLabel('Project Name').fill('Test Project');
    await page.getByLabel('Brand Name').first().fill('Test Brand');
    await page.getByLabel('Website URL').first().fill('https://test.com');
    
    const submitButton = page.getByRole('button', { name: /create project/i });
    await submitButton.click();
    
    // Should show loading state
    await expect(submitButton).toBeDisabled();
    await expect(page.getByText('Creating...')).toBeVisible();
  });
});
