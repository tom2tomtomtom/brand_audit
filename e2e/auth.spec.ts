import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display landing page', async ({ page }) => {
    await expect(page.getByText('Brand Audit Tool')).toBeVisible();
    await expect(page.getByText('Comprehensive competitive brand analysis')).toBeVisible();
  });

  test('should navigate to login page', async ({ page }) => {
    await page.getByRole('button', { name: /get started/i }).click();
    await expect(page).toHaveURL('/auth/login');
    await expect(page.getByText('Sign in to your account')).toBeVisible();
  });

  test('should show login form', async ({ page }) => {
    await page.goto('/auth/login');
    
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /sign in with google/i })).toBeVisible();
  });

  test('should validate login form', async ({ page }) => {
    await page.goto('/auth/login');
    
    // Try to submit empty form
    await page.getByRole('button', { name: /sign in/i }).click();
    
    // Should show validation errors
    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();
  });

  test('should handle invalid login credentials', async ({ page }) => {
    await page.goto('/auth/login');
    
    await page.getByLabel('Email').fill('invalid@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: /sign in/i }).click();
    
    // Should show error message
    await expect(page.getByText(/invalid login credentials/i)).toBeVisible();
  });

  test('should navigate to register page', async ({ page }) => {
    await page.goto('/auth/login');
    
    await page.getByRole('link', { name: /sign up/i }).click();
    await expect(page).toHaveURL('/auth/register');
    await expect(page.getByText('Create your account')).toBeVisible();
  });

  test('should show register form', async ({ page }) => {
    await page.goto('/auth/register');
    
    await expect(page.getByLabel('Full Name')).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByLabel('Confirm Password')).toBeVisible();
    await expect(page.getByRole('button', { name: /create account/i })).toBeVisible();
  });

  test('should validate register form', async ({ page }) => {
    await page.goto('/auth/register');
    
    // Try to submit empty form
    await page.getByRole('button', { name: /create account/i }).click();
    
    // Should show validation errors
    await expect(page.getByText('Name is required')).toBeVisible();
    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();
  });

  test('should validate password confirmation', async ({ page }) => {
    await page.goto('/auth/register');
    
    await page.getByLabel('Full Name').fill('Test User');
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByLabel('Confirm Password').fill('differentpassword');
    
    await page.getByRole('button', { name: /create account/i }).click();
    
    await expect(page.getByText('Passwords do not match')).toBeVisible();
  });

  test('should handle password visibility toggle', async ({ page }) => {
    await page.goto('/auth/login');
    
    const passwordInput = page.getByLabel('Password');
    const toggleButton = page.getByRole('button', { name: /toggle password visibility/i });
    
    // Initially password should be hidden
    await expect(passwordInput).toHaveAttribute('type', 'password');
    
    // Click toggle to show password
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'text');
    
    // Click toggle to hide password again
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'password');
  });

  test('should redirect to dashboard after successful login', async ({ page }) => {
    // This test would require a test user account
    // For now, we'll test the redirect logic with mocked authentication
    
    await page.goto('/auth/login');
    
    // Mock successful authentication by setting up route interception
    await page.route('**/auth/v1/token**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          access_token: 'mock-token',
          user: { id: 'test-user-id', email: 'test@example.com' }
        })
      });
    });
    
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: /sign in/i }).click();
    
    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
  });

  test('should handle Google OAuth flow', async ({ page }) => {
    await page.goto('/auth/login');
    
    // Mock Google OAuth redirect
    await page.route('**/auth/v1/authorize**', async route => {
      await route.fulfill({
        status: 302,
        headers: {
          'Location': '/auth/callback?code=mock-auth-code'
        }
      });
    });
    
    const googleButton = page.getByRole('button', { name: /sign in with google/i });
    await googleButton.click();
    
    // Should initiate OAuth flow
    await expect(page).toHaveURL(/auth\/callback/);
  });

  test('should handle logout', async ({ page }) => {
    // First, simulate being logged in
    await page.goto('/dashboard');
    
    // Mock authentication state
    await page.addInitScript(() => {
      localStorage.setItem('supabase.auth.token', JSON.stringify({
        access_token: 'mock-token',
        user: { id: 'test-user-id' }
      }));
    });
    
    // Find and click logout button
    await page.getByRole('button', { name: /logout/i }).click();
    
    // Should redirect to landing page
    await expect(page).toHaveURL('/');
  });

  test('should protect dashboard route', async ({ page }) => {
    // Try to access dashboard without authentication
    await page.goto('/dashboard');
    
    // Should redirect to login
    await expect(page).toHaveURL('/auth/login');
  });

  test('should remember user preference for theme', async ({ page }) => {
    await page.goto('/');
    
    // Toggle theme
    const themeToggle = page.getByRole('button', { name: /toggle theme/i });
    if (await themeToggle.isVisible()) {
      await themeToggle.click();
      
      // Check if theme preference is saved
      const theme = await page.evaluate(() => localStorage.getItem('theme'));
      expect(theme).toBeTruthy();
    }
  });
});
