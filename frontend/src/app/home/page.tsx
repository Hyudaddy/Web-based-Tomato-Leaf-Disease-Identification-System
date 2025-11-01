'use client'

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import LoadingScreen from '@/components/LoadingScreen'
import Image from 'next/image'

const useScrollAnimation = () => {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return scrollY
}

const AnimatedSection = ({ children, delay = 0 }: { children: React.ReactNode, delay?: number }) => {
  const ref = useRef<HTMLDivElement>(null)
  const [isVisible, setIsVisible] = useState(false)
  const scrollY = useScrollAnimation()

  useEffect(() => {
    if (!ref.current) return

    const rect = ref.current.getBoundingClientRect()
    const isInView = rect.top < window.innerHeight * 0.75

    if (isInView) {
      setIsVisible(true)
    }
  }, [scrollY])

  return (
    <div
      ref={ref}
      className={`transition-all duration-1000 ease-out ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-20'
      }`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  )
}

const Typewriter = ({ text, start = true }: { text: string, start?: boolean }) => {
  const [displayedText, setDisplayedText] = useState('')
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    if (!start) {
      setDisplayedText('')
      setIsComplete(false)
      return
    }
  }, [start])

  useEffect(() => {
    if (!start) return
    if (displayedText.length < text.length) {
      const timer = setTimeout(() => {
        setDisplayedText(text.slice(0, displayedText.length + 1))
      }, 50)
      return () => clearTimeout(timer)
    } else {
      setIsComplete(true)
    }
  }, [displayedText, text, start])

  return (
    <span>
      {displayedText}
      {start && <span className="font-bold" style={{ animation: 'blink 1.25s ease-out infinite' }}>|</span>}
    </span>
  )
}

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(true)
  const [currentDescription, setCurrentDescription] = useState(0)
  const [isFading, setIsFading] = useState(false)
  const [mounted, setMounted] = useState(false)
  const scrollY = useScrollAnimation()

  const handleLoadingComplete = () => {
    setIsLoading(false)
    setTimeout(() => {
      setMounted(true)
    }, 100)
  }

  const greeting = "Welcome to, Tomato Leaf Disease Identification System"
  const descriptions = [
    'AI-powered tomato leaf disease detection',
    'Instant diagnosis in seconds',
    '95% accuracy detection rate',
    'For farmers worldwide',
    'Fito or Phyto a greek word for plant'
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setIsFading(true)
      setTimeout(() => {
        setCurrentDescription((prev) => (prev + 1) % descriptions.length)
        setIsFading(false)
      }, 500)
    }, 3000)

    return () => clearInterval(interval)
  }, [descriptions.length])

  const parallax = (value: number) => value * 0.5

  return (
    <>
      {isLoading && <LoadingScreen onComplete={handleLoadingComplete} />}
      <div className={`min-h-screen ${isLoading ? 'hidden' : ''}`}>
        <section 
          className="relative overflow-hidden min-h-screen flex items-center justify-center bg-cover bg-center pt-16"
          style={{
            backgroundImage: 'url(/tomato_bg_all.jpg)',
            backgroundAttachment: 'fixed'
          }}
        >
          {/* Dark overlay for text readability */}
          <div className="absolute inset-0 bg-black/55"></div>
          
          <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10">
            <div 
              className={`transition-all duration-1500 ease-out ${
                mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
              }`}
            >
              <div className="text-center">
              
              {/* Main Heading with Typewriter Effect - Reduced Weight and Size for Better Fit */}
              <h1 className="text-[36px] sm:text-[56px] lg:text-[76px] font-semibold text-white mb-8 leading-[1.25] tracking-tight font-montserrat" style={{ fontWeight: 600 }}>
                <Typewriter text={greeting} start={mounted} />
              </h1>
              
              {/* Rotating Description */}
              <div className="text-[18px] sm:text-[24px] lg:text-[30px] font-normal text-gray-200 mb-12 h-[26px] sm:h-[32px] lg:h-[40px] flex items-center justify-center px-4">
                <span className={`inline-block transition-opacity duration-500 ${isFading ? 'opacity-0' : 'opacity-100'}`}>
                  {descriptions[currentDescription]}
                </span>
              </div>
              
              {/* Learn More Button */}
              <Link
                href="/about"
                className="group inline-flex items-center justify-center px-10 py-4 bg-[#47f793] text-white font-[600] rounded-md hover:bg-[#3ee673] transition-all duration-300 ease-out text-lg shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95"
              >
                Learn More
                <svg className="ml-3 w-5 h-5 transition-transform duration-300 ease-out group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
              </div>
            </div>
          </div>
        </section>
      </div>
    </>
  )
}
