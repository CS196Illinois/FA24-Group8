// app/page.tsx
"use client"

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/signup', {
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

      setMessage(data.message);
      setEmail('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to register');
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Header */}
        <header className="flex justify-between items-center">
          <div className="flex items-center">
            <Link href="/" className="flex items-center">
              <div className="flex items-center cursor-pointer">
                <Image
                  src="/logo.svg"
                  alt="Nexus Scholar"
                  width={32}
                  height={32}
                />
                <span className="ml-2 text-xl font-semibold">Nexus Scholar</span>
              </div>
            </Link>
          </div>
          
          <div>
            <span className="text-gray-400">Already joined? </span>
            <Link href="/login" className="text-white hover:underline">
              Log in
            </Link>
          </div>
        </header>

        {/* Main Content */}
        <main className="grid grid-cols-1 lg:grid-cols-2 gap-12 mt-20">
          {/* Left Column */}
          <div className="flex flex-col justify-center">
            <h1 className="text-3xl md:text-4xl font-medium mb-6">
              Nexus Scholar is a platform to assist undergrads in their search for research opportunities
            </h1>
            <p className="text-gray-400 text-lg">
              Built by UIUC Students
            </p>
          </div>

          {/* Right Column */}
          <div className="flex flex-col justify-rigth lg:items-start">
            <div className="w-full max-w-md">
              <h2 className="text-2xl md:text-3xl font-semibold mb-4">
                Try Nexus Scholar for Free
              </h2>
              <p className="text-gray-400 mb-6">
                Enter your email address to sign up and find new opportunities.
              </p>

              {message && (
                <div className="mb-4 p-4 bg-green-500/10 border border-green-500 rounded-lg text-green-500">
                  {message}
                </div>
              )}

              {error && (
                <div className="mb-4 p-4 bg-red-500/10 border border-red-500 rounded-lg text-red-500">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg 
                             focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-white text-black py-3 px-4 rounded-lg font-medium
                           hover:bg-gray-100 transition-colors"
                >
                  Get Started
                </button>
              </form>

              <p className="mt-4 text-sm text-gray-400">
                By continuing, you agree to our{' '}
                <Link href="/terms" className="text-gray-300 hover:underline">
                  Terms of Service
                </Link>
                {' '}and{' '}
                <Link href="/privacy" className="text-gray-300 hover:underline">
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