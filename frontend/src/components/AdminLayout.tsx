'use client'

import { usePathname, useRouter } from 'next/navigation'
import Link from 'next/link'
import { LayoutDashboard, Database, LogOut } from 'lucide-react'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import Image from 'next/image'

interface AdminLayoutProps {
  children: React.ReactNode
}

export default function AdminLayout({ children }: AdminLayoutProps) {
  const pathname = usePathname()
  const router = useRouter()
  const [isAdmin, setIsAdmin] = useState(false)
  const [loading, setLoading] = useState(true)
  const [userEmail, setUserEmail] = useState('')

  useEffect(() => {
    checkAdminAccess()
  }, [])

  const checkAdminAccess = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      
      if (!user) {
        router.push('/admin/login')
        return
      }

      setUserEmail(user.email || '')

      // Check if user has admin role in metadata
      const isUserAdmin = user.user_metadata?.role === 'admin' || user.email === 'admin@fito.com'
      setIsAdmin(isUserAdmin)
      
      if (!isUserAdmin) {
        router.push('/')
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      router.push('/admin/login')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-2 border-[#47f793] border-t-transparent mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Loading...</p>
        </div>
      </div>
    )
  }

  if (!isAdmin) {
    return null
  }

  const navItems = [
    { href: '/admin', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/admin/dataset', label: 'Dataset', icon: Database },
  ]

  return (
    <div className="min-h-screen bg-white">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-white border-r border-gray-200 shadow-sm z-40">
        {/* Logo Section */}
        <div className="p-6 border-b border-gray-200">
          <Link href="/admin" className="flex items-center gap-3 group">
            <div className="w-10 h-10 bg-[#47f793] rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <Image 
                src="/logo_001.png" 
                alt="FITO Logo" 
                width={24} 
                height={24} 
                className="w-6 h-6"
              />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-gray-900 group-hover:text-[#47f793] transition-colors duration-300">FITO</h1>
              <p className="text-xs text-gray-500">Admin</p>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 group ${
                  isActive
                    ? 'bg-[#47f793]/10 text-[#47f793] border border-[#47f793]/30'
                    : 'text-gray-700 hover:text-gray-900 hover:bg-gray-50 border border-transparent'
                }`}
              >
                <Icon className={`w-5 h-5 transition-transform duration-300 ${isActive ? 'scale-110' : 'group-hover:scale-110'}`} />
                <span className="font-medium">{item.label}</span>
              </Link>
            )
          })}
        </nav>

        {/* User Info */}
        <div className="absolute bottom-20 left-0 right-0 px-4">
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Logged in as</p>
            <p className="text-sm font-medium text-gray-900 truncate">{userEmail}</p>
          </div>
        </div>

        {/* Logout Button */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full rounded-lg text-gray-700 hover:text-red-600 hover:bg-red-50 transition-all duration-300 border border-transparent hover:border-red-200 group"
          >
            <LogOut className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ml-64 min-h-screen relative z-10">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  )
}

