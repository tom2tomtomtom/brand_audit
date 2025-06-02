'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import { User } from '@supabase/supabase-js';
import { useRouter } from 'next/navigation';
import type { User as AppUser, Organization } from '@/types';

interface AuthContextType {
  user: User | null;
  appUser: AppUser | null;
  organizations: Organization[];
  currentOrganization: Organization | null;
  loading: boolean;
  signOut: () => Promise<void>;
  setCurrentOrganization: (org: Organization) => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

interface ProvidersProps {
  children: React.ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <AuthProvider>
      <ThemeProvider>
        {children}
      </ThemeProvider>
    </AuthProvider>
  );
}

function AuthProvider({ children }: ProvidersProps) {
  const [user, setUser] = useState<User | null>(null);
  const [appUser, setAppUser] = useState<AppUser | null>(null);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [currentOrganization, setCurrentOrganization] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchUserData = async (userId: string, isNewUser = false) => {
    try {
      // If this is a new user, create them first
      if (isNewUser) {
        const response = await fetch('/api/auth/user', {
          method: 'POST',
        });

        if (!response.ok) {
          console.error('Failed to create user');
        }
      }

      // Fetch user data from our API
      const response = await fetch('/api/auth/user');

      if (!response.ok) {
        if (response.status === 404) {
          // User doesn't exist, try to create them
          const createResponse = await fetch('/api/auth/user', {
            method: 'POST',
          });

          if (createResponse.ok) {
            // Retry fetching user data
            const retryResponse = await fetch('/api/auth/user');
            if (retryResponse.ok) {
              const data = await retryResponse.json();
              setAppUser(data.user);
              setOrganizations(data.organizations);

              if (!currentOrganization && data.organizations.length > 0) {
                setCurrentOrganization(data.organizations[0]);
              }
            }
          }
        }
        return;
      }

      const data = await response.json();
      setAppUser(data.user);
      setOrganizations(data.organizations);

      // Set current organization if not set
      if (!currentOrganization && data.organizations.length > 0) {
        setCurrentOrganization(data.organizations[0]);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const refreshUser = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (user) {
      await fetchUserData(user.id);
    }
  };

  const handleSignOut = async () => {
    try {
      await supabase.auth.signOut();
      setUser(null);
      setAppUser(null);
      setOrganizations([]);
      setCurrentOrganization(null);
      router.push('/auth/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      if (session?.user) {
        fetchUserData(session.user.id);
      }
      setLoading(false);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (event, session) => {
      setUser(session?.user ?? null);

      if (session?.user) {
        const isNewUser = event === 'SIGNED_UP';
        await fetchUserData(session.user.id, isNewUser);
      } else {
        setAppUser(null);
        setOrganizations([]);
        setCurrentOrganization(null);
      }

      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const value = {
    user,
    appUser,
    organizations,
    currentOrganization,
    loading,
    signOut: handleSignOut,
    setCurrentOrganization,
    refreshUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

function ThemeProvider({ children }: ProvidersProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <>{children}</>;
  }

  return <>{children}</>;
}
