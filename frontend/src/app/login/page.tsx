'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import Link from 'next/link'

export default function LoginPage() {
  const router = useRouter()
  const [isSignUp, setIsSignUp] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setMessage('')
    setLoading(true)

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) throw error

      // Check if user is admin
      if (data.user?.user_metadata?.role === 'admin' || data.user?.email === 'admin@fito.com') {
        router.push('/admin')
      } else {
        setError('Access denied. Admin privileges required.')
        await supabase.auth.signOut()
      }
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setMessage('')
    setLoading(true)

    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      setLoading(false)
      return
    }

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
            role: 'user' // Default role, admin needs to be set manually
          }
        }
      })

      if (error) throw error

      setMessage('Account created successfully! Please check your email to verify your account.')
      setEmail('')
      setPassword('')
      setConfirmPassword('')
      setFullName('')
      
      // Switch to sign in after 3 seconds
      setTimeout(() => {
        setIsSignUp(false)
        setMessage('')
      }, 3000)
    } catch (err: any) {
      setError(err.message || 'Sign up failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background matching the site style */}
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: 'url(/tomato_bg_all.jpg)',
          backgroundAttachment: 'fixed'
        }}
      />
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

      {/* Login Container - Minimalist, no card */}
      <div className="relative z-10 w-full max-w-md px-6 py-8">
        
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-semibold text-white mb-3 font-montserrat">
            {isSignUp ? 'Create Account' : 'Welcome Back'}
          </h1>
          <p className="text-gray-300 text-lg">
            {isSignUp ? 'Sign up to access the admin dashboard' : 'Sign in to access the admin dashboard'}
          </p>
        </div>

        {/* Form */}
        <form onSubmit={isSignUp ? handleSignUp : handleSignIn} className="space-y-6">
          
          {/* Full Name (Sign Up Only) */}
          {isSignUp && (
            <div>
              <label htmlFor="fullName" className="block text-sm font-medium text-white/90 mb-2">
                Full Name
              </label>
              <input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/30 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#47f793] focus:border-transparent transition-all"
                placeholder="John Doe"
              />
            </div>
          )}

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-white/90 mb-2">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/30 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#47f793] focus:border-transparent transition-all"
              placeholder="admin@fito.com"
            />
          </div>

          {/* Password */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-white/90 mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/30 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#47f793] focus:border-transparent transition-all"
              placeholder="••••••••"
            />
          </div>

          {/* Confirm Password (Sign Up Only) */}
          {isSignUp && (
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-white/90 mb-2">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/30 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#47f793] focus:border-transparent transition-all"
                placeholder="••••••••"
              />
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-500/20 backdrop-blur-md border border-red-500/50 text-red-200 px-4 py-3 rounded-md text-sm">
              {error}
            </div>
          )}

          {/* Success Message */}
          {message && (
            <div className="bg-green-500/20 backdrop-blur-md border border-green-500/50 text-green-200 px-4 py-3 rounded-md text-sm">
              {message}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#47f793] text-gray-900 py-3 rounded-md font-semibold hover:bg-white transition-all duration-300 ease-out hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {loading ? (isSignUp ? 'Creating Account...' : 'Signing In...') : (isSignUp ? 'Sign Up' : 'Sign In')}
          </button>
        </form>

        {/* Toggle Sign In / Sign Up */}
        <div className="mt-8 text-center">
          <button
            onClick={() => {
              setIsSignUp(!isSignUp)
              setError('')
              setMessage('')
              setEmail('')
              setPassword('')
              setConfirmPassword('')
              setFullName('')
            }}
            className="text-white/90 hover:text-[#47f793] transition-colors duration-300 text-sm font-medium"
          >
            {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
          </button>
        </div>

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <Link 
            href="/home" 
            className="inline-flex items-center text-sm text-white/70 hover:text-white transition-colors duration-300"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}

