# Brand Audit Tool

A comprehensive web application for competitive brand analysis powered by AI. Automatically collect brand assets, analyze positioning, and generate professional presentations.

## 🚀 Features

- **Intelligent Web Scraping**: Automatically collect brand assets, logos, and positioning statements
- **AI-Powered Analysis**: Leverage LLM technology for brand positioning and competitive analysis
- **Visual Asset Management**: Organize and categorize collected brand assets
- **Automated Presentations**: Generate professional presentation decks with multiple templates
- **Real-time Collaboration**: Work with your team with role-based access control
- **Secure Cloud Storage**: All data stored securely with Supabase

## 🛠 Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Shadcn/ui
- **Backend**: Next.js API Routes, Supabase
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Supabase Auth
- **Storage**: Supabase Storage
- **Deployment**: Netlify
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Node.js 18+ 
- npm or yarn
- Supabase account
- Git

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd brand-audit-tool
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   
   Fill in your environment variables:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

4. **Set up the database**
   ```bash
   # Install Supabase CLI
   npm install -g supabase
   
   # Run migrations
   supabase db push
   ```

5. **Start the development server**
   ```bash
   npm run dev
   ```

6. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🗄️ Database Setup

The application uses Supabase with the following key tables:

- `users` - User profiles and authentication
- `organizations` - Multi-tenant organization structure
- `projects` - Brand analysis projects
- `brands` - Companies being analyzed
- `assets` - Collected brand assets (images, documents)
- `analyses` - AI-generated analysis results
- `presentations` - Generated presentation decks

### Running Migrations

```bash
# Apply all migrations
npm run db:migrate

# Reset database (development only)
npm run db:reset

# Generate TypeScript types
npm run db:generate
```

## 🚀 Deployment

### Netlify Deployment

1. **Connect your repository to Netlify**
2. **Set environment variables in Netlify dashboard**
3. **Configure build settings**:
   - Build command: `npm run build`
   - Publish directory: `.next`
4. **Deploy**

### Environment Variables for Production

```env
NEXT_PUBLIC_SUPABASE_URL=your_production_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_production_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_production_service_role_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking
- `npm run db:migrate` - Run database migrations
- `npm run db:generate` - Generate TypeScript types from database

## 🏗️ Project Structure

```
src/
├── app/                    # Next.js 14 app directory
│   ├── api/               # API routes
│   ├── auth/              # Authentication pages
│   ├── dashboard/         # Dashboard pages
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── ui/               # Base UI components
│   ├── dashboard/        # Dashboard-specific components
│   ├── forms/            # Form components
│   └── layout/           # Layout components
├── lib/                  # Utility libraries
├── types/                # TypeScript type definitions
├── utils/                # Utility functions
├── hooks/                # Custom React hooks
├── stores/               # State management
└── services/             # External service integrations
```

## 🔐 Authentication

The application uses Supabase Auth with support for:

- Email/password authentication
- OAuth providers (Google)
- Email verification
- Password reset
- Role-based access control

## 🎨 UI Components

Built with Shadcn/ui components:

- Consistent design system
- Accessible components
- Dark mode support
- Responsive design
- Custom animations

## 🧪 Testing

```bash
# Run unit tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e
```

## 📊 Monitoring

- Error tracking with Sentry
- Performance monitoring
- Real user monitoring (RUM)
- API performance tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@brandaudittool.com or join our Slack channel.

## 🗺️ Roadmap

- [ ] Advanced AI analysis models
- [ ] Social media integration
- [ ] Video asset analysis
- [ ] Advanced presentation templates
- [ ] API for third-party integrations
- [ ] Mobile application

---

Built with ❤️ by the Brand Audit Tool team
