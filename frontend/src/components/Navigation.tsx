'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import Image from 'next/image'
import { useState } from 'react'

export default function Navigation() {
  const pathname = usePathname()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const navItems = [
    { name: 'Home', href: '/home' },
    { name: 'Identify', href: '/fito' },
    { name: 'Information', href: '/information' },
    { name: 'About', href: '/about' },
    { name: 'FAQ', href: '/faq' },
    { name: 'Contact', href: '/contact' }
  ]

  const closeMenu = () => setIsMenuOpen(false)

  // Don't render navigation on admin pages
  if (pathname?.startsWith('/admin')) {
    return null
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 pointer-events-none">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <div className="flex justify-between items-start">
          {/* Logo - Left - Standalone */}
          <Link href="/home" className="flex items-center space-x-2 pointer-events-auto group" onClick={closeMenu}>
            <div className="relative w-6 h-6 transition-transform duration-300 ease-out group-hover:scale-110">
              <Image 
                src="/logo_001.png" 
                alt="Fito Logo" 
                width={24} 
                height={24} 
                className="w-6 h-6"
              />
            </div>
            <span className="text-xl font-semibold text-white transition-colors duration-300 ease-out group-hover:text-[#47f793]">FITO</span>
          </Link>

          {/* Navigation Bar - Right - Separate Floating Element (Desktop) */}
          <div className="hidden md:flex pointer-events-auto">
            <div className="bg-black/40 backdrop-blur-md rounded-md px-6 py-3 flex items-center space-x-6 border border-white/25 shadow-sm transition-all duration-300 ease-out hover:shadow-md hover:bg-black/50">
              {/* Navigation Links */}
              <div className="flex items-center space-x-6">
                {navItems.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`text-sm font-medium transition-all duration-300 ease-out relative group/link ${
                      pathname === item.href
                        ? 'text-white font-semibold'
                        : 'text-white/85 hover:text-white'
                    }`}
                  >
                    <span className="relative z-10">{item.name}</span>
                    <span className={`absolute inset-x-0 -bottom-1 h-0.5 bg-[#47f793] transform origin-left transition-transform duration-300 ease-out ${
                      pathname === item.href ? 'scale-x-100' : 'scale-x-0 group-hover/link:scale-x-100'
                    }`}></span>
                  </Link>
                ))}
              </div>

              {/* Log-in Button */}
              <Link
                href="/login"
                className="px-5 py-2 bg-[#47f793] text-gray-900 text-sm font-semibold rounded-md hover:bg-white transition-all duration-300 ease-out hover:scale-[1.02] active:scale-95"
              >
                Log-in
              </Link>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden pointer-events-auto">
            <button
              type="button"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="bg-black/40 backdrop-blur-md rounded-md p-3 border border-white/25 shadow-sm text-white/85 hover:text-white transition-all duration-300 ease-out hover:shadow-md"
              aria-label="Toggle menu"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <>
            {/* Backdrop */}
            <div 
              className="fixed inset-0 bg-black/30 md:hidden pointer-events-auto"
              onClick={closeMenu}
              style={{ top: '70px' }}
            />
            
            {/* Mobile Menu Content */}
            <div className="absolute top-20 right-4 md:hidden pointer-events-auto w-72">
              <div className="bg-black/40 backdrop-blur-md rounded-lg p-4 border border-white/25 shadow-lg">
                {/* Navigation Links */}
                <div className="flex flex-col space-y-2">
                  {navItems.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      onClick={closeMenu}
                      className={`px-4 py-3 rounded-md text-sm font-medium transition-all duration-300 ease-out ${
                        pathname === item.href
                          ? 'bg-[#47f793]/20 text-white font-semibold border-l-2 border-[#47f793]'
                          : 'text-white/85 hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      {item.name}
                    </Link>
                  ))}
                </div>

                {/* Divider */}
                <div className="my-3 border-t border-white/20" />

                {/* Log-in Button */}
                <Link
                  href="/login"
                  onClick={closeMenu}
                  className="block w-full px-4 py-3 bg-[#47f793] text-gray-900 text-sm font-semibold rounded-md hover:bg-white transition-all duration-300 ease-out text-center"
                >
                  Log-in
                </Link>
              </div>
            </div>
          </>
        )}
      </div>
    </nav>
  )
}


