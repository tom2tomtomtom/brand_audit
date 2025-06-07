import { Suspense } from 'react';

export default function PresentationsPage() {
  return (
    <div className="container mx-auto py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Presentations</h1>
        <p className="text-muted-foreground">
          Manage and view your brand analysis presentations
        </p>
      </div>
      
      <Suspense fallback={<div>Loading presentations...</div>}>
        <div className="text-center py-12">
          <p className="text-muted-foreground">
            No presentations available yet. Create a project to generate presentations.
          </p>
        </div>
      </Suspense>
    </div>
  );
}