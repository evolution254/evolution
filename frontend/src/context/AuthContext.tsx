import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../types';
import { userStorage, clearAllStorage } from '../utils/storage';
import { API_ENDPOINTS, apiRequest } from '../config/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored user data and validate token
    const initializeAuth = async () => {
      try {
        const storedUser = userStorage.get();
        const token = localStorage.getItem('evolutionMarketToken');
        
        if (storedUser && token) {
          // For demo mode, just use stored user data
          setUser(storedUser);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        // In demo mode, don't clear storage on network errors
        const storedUser = userStorage.get();
        if (storedUser) {
          setUser(storedUser);
        }
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string): Promise<void> => {
    try {
      // Demo mode: Create a mock user for any valid email/password
      if (!email || !password) {
        throw new Error('Email and password are required');
      }

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      const userData: User = {
        id: '1',
        name: email.split('@')[0] || 'User',
        email: email,
        avatar: `https://images.pexels.com/photos/1040880/pexels-photo-1040880.jpeg?auto=compress&cs=tinysrgb&w=100`,
        isVerified: true,
        isAdmin: false,
        contactNumber: '+1234567890',
        createdAt: new Date().toISOString()
      };

      const token = `demo_token_${Date.now()}`;

      setUser(userData);
      userStorage.save(userData);
      localStorage.setItem('evolutionMarketToken', token);

    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (name: string, email: string, password: string): Promise<void> => {
    try {
      // Demo mode: Create a mock user for registration
      if (!name || !email || !password) {
        throw new Error('All fields are required');
      }

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1500));

      const userData: User = {
        id: `user_${Date.now()}`,
        name: name,
        email: email,
        avatar: `https://images.pexels.com/photos/1040880/pexels-photo-1040880.jpeg?auto=compress&cs=tinysrgb&w=100`,
        isVerified: false,
        isAdmin: false,
        contactNumber: '',
        createdAt: new Date().toISOString()
      };

      const token = `demo_token_${Date.now()}`;

      setUser(userData);
      userStorage.save(userData);
      localStorage.setItem('evolutionMarketToken', token);

    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Demo mode: Just clear local data
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always clear local data
      setUser(null);
      clearAllStorage();
    }
  };

  const updateUser = async (userData: Partial<User>) => {
    if (!user) return;

    try {
      // Demo mode: Update locally
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      userStorage.save(updatedUser);
      
    } catch (error) {
      console.error('Update user error:', error);
      // Fallback to local update
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      userStorage.save(updatedUser);
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      login,
      register,
      logout,
      updateUser,
      isLoading
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};