// app/page.tsx
"use client"

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import logo from './logo.svg'
import { log } from 'console';

export default function Signup() {
  // Form state management
  const [formData, setFormData] = useState({
    email: '',
    message: '',
    error: '',
    isLoading: false
  });

  const { email, message, error, isLoading } = formData;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    setFormData(prev => ({
      ...prev,
      message: '',
      error: '',
      isLoading: true
    }));

    try {
      const response = await fetch('/api/signup', {  // Removed hardcoded localhost URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      setFormData(prev => ({
        ...prev,
        message: data.message,
        email: '',
        isLoading: false
      }));
    } catch (err) {
      setFormData(prev => ({
        ...prev,
        error: err instanceof Error ? err.message : 'Failed to register',
        isLoading: false
      }));
    }
  };

  // Alert component to handle both success and error messages
  const Alert = ({ type, message }: { type: 'success' | 'error'; message: string }) => {
    const styles = {
      success: 'bg-green-500/10 border-green-500 text-green-500',
      error: 'bg-red-500/10 border-red-500 text-red-500'
    };

    return message ? (
      <div className={`mb-4 p-4 border rounded-lg ${styles[type]}`}>
        {message}
      </div>
    ) : null;
  };
  
  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Header */}
        <header className="flex justify-between items-center">
          <Link href="/" className="flex items-center group">
            <div className="flex items-center">
              <div className="relative w-8 h-8">
                <Image
                  src={logo}
                  alt="/logo.svg"
                  fill
                  sizes="124px"
                  className="object-contain"
                  priority
                />
              </div>
              <span className="ml-2 text-xl font-semibold group-hover:text-gray-300 transition-colors">
                Nexus Scholar
              </span>
            </div>
          </Link>
          
          <div>
            <span className="text-gray-400">Already joined? </span>
            <Link 
              href="/login" 
              className="text-white hover:text-gray-300 hover:underline transition-colors"
            >
              Log in
            </Link>
          </div>
        </header>

        {/* Main Content */}
        <main className="grid grid-cols-1 lg:grid-cols-2 gap-12 mt-20">
          {/* Left Column */}
          <div className="flex flex-col justify-center space-y-6">
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-medium">
              Nexus Scholar is a platform to assist undergrads in their search for research opportunities
            </h1>
            <p className="text-gray-400 text-lg md:text-xl">
              Built by UIUC Students
            </p>
          </div>

          {/* Right Column */}
          <div className="flex flex-col justify-right lg:items-start">
            <div className="w-full max-w-md space-y-6">
              <div className="space-y-2">
                <h2 className="text-2xl md:text-3xl font-semibold">
                  Try Nexus Scholar for Free
                </h2>
                <p className="text-gray-400">
                  Enter your email address to sign up and find new opportunities.
                </p>
              </div>

              <Alert type="success" message={message} />
              <Alert type="error" message={error} />

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <label 
                    htmlFor="email" 
                    className="block text-sm font-medium"
                  >
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={email}
                    onChange={(e) => setFormData(prev => ({
                      ...prev,
                      email: e.target.value
                    }))}
                    placeholder="name@example.com"
                    className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg 
                             focus:ring-2 focus:ring-blue-500 focus:border-transparent
                             transition-colors"
                    required
                    disabled={isLoading}
                  />
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-white text-black py-3 px-4 rounded-lg font-medium
                           hover:bg-gray-100 transition-colors disabled:opacity-50
                           disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Signing up...' : 'Get Started'}
                </button>
              </form>

              <p className="text-sm text-gray-400">
                By continuing, you agree to our{' '}
                <Link 
                  href="/terms" 
                  className="text-gray-300 hover:text-white hover:underline transition-colors"
                >
                  Terms of Service
                </Link>
                {' '}and{' '}
                <Link 
                  href="/privacy" 
                  className="text-gray-300 hover:text-white hover:underline transition-colors"
                >
                  Privacy Policy
                </Link>
                .
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}