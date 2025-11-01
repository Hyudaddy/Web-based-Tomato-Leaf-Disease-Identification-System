'use client'

import { useEffect, useState, useRef } from 'react'
import Link from 'next/link'

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

const Typewriter = ({ text }: { text: string }) => {
  const [displayedText, setDisplayedText] = useState('')
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    if (displayedText.length < text.length) {
      const timer = setTimeout(() => {
        setDisplayedText(text.slice(0, displayedText.length + 1))
      }, 50)
      return () => clearTimeout(timer)
    } else {
      setIsComplete(true)
    }
  }, [displayedText, text])

  return (
    <span>
      {displayedText}
      {!isComplete && <span className="animate-pulse">|</span>}
    </span>
  )
}

export default function AboutPage() {
  const [mounted, setMounted] = useState(false)
  const scrollY = useScrollAnimation()

  useEffect(() => {
    setMounted(true)
  }, [])

  const parallax = (value: number) => value * 0.5

  return (
    <div className="min-h-screen bg-white overflow-hidden">
      {/* Tagline Section with Typewriter */}
      <section className="relative min-h-screen pt-32 pb-20 md:pt-40 md:pb-32 flex items-center justify-center">

        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10">
          <div 
            className={`transition-all duration-1500 ease-out ${
              mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-normal text-gray-900 leading-tight tracking-tight">
              <Typewriter text="Committed to empowering farmers with intelligence." />
            </h1>
          </div>
        </div>
      </section>

      {/* Vision Section */}
      <section className="py-20 md:py-32 border-t border-gray-200">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-start pt-12">
            <AnimatedSection delay={0}>
              <h2 className="text-2xl sm:text-3xl font-normal text-gray-700 sticky top-32">
                The Vision
              </h2>
            </AnimatedSection>

            <AnimatedSection delay={200}>
              <div className="space-y-8">
                <p className="text-lg sm:text-xl font-light text-gray-900 leading-relaxed">
                  Fito envisions a future where every farmer, regardless of location or resources, 
                  has instant access to laboratory-grade disease detection. Through our AI-driven solutions, 
                  we aim to revolutionize agricultural diagnostics, enhancing crop yields and fostering 
                  sustainable farming practices globally.
                </p>
                <p className="text-lg sm:text-xl font-light text-gray-900 leading-relaxed">
                  We strive for an agricultural ecosystem where quality crop protection is elevated 
                  for all farmers worldwide.
                </p>
              </div>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 md:py-32 bg-gray-50 border-t border-gray-200">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-start pt-12">
            <AnimatedSection delay={0}>
              <h2 className="text-2xl sm:text-3xl font-normal text-gray-700 sticky top-32">
                The Mission
              </h2>
            </AnimatedSection>

            <AnimatedSection delay={200}>
              <div className="space-y-8">
                <p className="text-lg sm:text-xl font-light text-gray-900 leading-relaxed">
                  Our mission is to democratize advanced agricultural technology and make it accessible 
                  to farmers everywhere. We're building tools that detect diseases instantly, provide 
                  actionable insights, and empower farmers to make informed decisions.
                </p>
                <p className="text-lg sm:text-xl font-light text-gray-900 leading-relaxed">
                  By combining cutting-edge machine learning with intuitive design, we're eliminating 
                  barriers to crop health monitoring. Every farmer deserves access to the technology 
                  that protects their livelihood.
                </p>
              </div>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* Roadmap / ML System Section */}
      <section className="py-20 md:py-32 border-t border-gray-200">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-start pt-12">
            <AnimatedSection delay={0}>
              <h2 className="text-2xl sm:text-3xl font-normal text-gray-700 sticky top-32">
                Our ML System
              </h2>
            </AnimatedSection>

            <AnimatedSection delay={200}>
              <div className="space-y-12">
                {[
                  {
                    step: '01',
                    title: 'Gathering Dataset',
                    description: 'Collecting thousands of high-quality tomato leaf images representing diverse disease states and healthy leaves from various growing conditions worldwide.'
                  },
                  {
                    step: '02',
                    title: 'Training the Model',
                    description: 'Using advanced deep learning techniques to train our neural networks on the comprehensive dataset, achieving 85% accuracy across 10 disease types.'
                  },
                  {
                    step: '03',
                    title: 'Developing the System',
                    description: 'Integrating the trained model into an intuitive platform that provides instant, actionable diagnoses to farmers with treatment recommendations.'
                  }
                ].map((item, index) => (
                  <div key={index} className="pb-8 border-b border-gray-200 last:border-b-0">
                    <div className="text-sm font-light text-gray-500 mb-2">{item.step}</div>
                    <h3 className="text-xl sm:text-2xl font-normal text-gray-900 mb-4">
                      {item.title}
                    </h3>
                    <p className="text-base sm:text-lg font-light text-gray-700 leading-relaxed">
                      {item.description}
                    </p>
                  </div>
                ))}
              </div>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* Our Approach Section */}
      <section className="py-20 md:py-32 bg-gray-50 border-t border-gray-200">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection>
            <div className="text-center mb-20 pt-12">
              <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6 font-montserrat">
                Our Approach
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Simple to use, sophisticated under the hood
              </p>
            </div>
          </AnimatedSection>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                number: '01',
                title: 'Upload a Photo',
                description: 'Snap a photo of your tomato leaf using any smartphone or camera'
              },
              {
                number: '02',
                title: 'AI Analysis',
                description: 'Our model analyzes thousands of features in milliseconds'
              },
              {
                number: '03',
                title: 'Instant Diagnosis',
                description: 'Get results with treatment recommendations immediately'
              }
            ].map((step, index) => (
              <AnimatedSection key={index} delay={index * 150}>
                <div className="relative group">
                  <div className="absolute inset-0 bg-gradient-to-br from-[#47f793] to-green-500 rounded-3xl opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
                  <div className="relative bg-white border border-gray-200 rounded-3xl p-8 group-hover:border-[#47f793] transition-all duration-300">
                    <div className="text-6xl font-bold text-gray-200 group-hover:text-[#47f793]/20 transition-colors duration-300 mb-4">
                      {step.number}
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-[#47f793] transition-colors duration-300">
                      {step.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                </div>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black text-white pt-20 pb-8">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          {/* Back to top button */}
          <button 
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="mb-12 hover:text-[#47f793] transition-colors duration-300"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
            </svg>
          </button>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-16 py-12 border-t border-gray-800">
            {/* Navigation */}
            <div>
              <h3 className="text-sm font-light tracking-widest text-gray-400 mb-8 uppercase">Navigation</h3>
              <nav className="space-y-4">
                {['Home', 'Fito', 'About', 'Contact'].map((item) => (
                  <Link
                    key={item}
                    href={item === 'Home' ? '/home' : item === 'Fito' ? '/fito' : item === 'About' ? '/about' : '#'}
                    className="text-2xl sm:text-3xl font-light text-white hover:text-[#47f793] transition-colors duration-300 block"
                  >
                    {item}
                  </Link>
                ))}
              </nav>
            </div>

            {/* Services/Features */}
            <div>
              <h3 className="text-sm font-light tracking-widest text-gray-400 mb-8 uppercase">Features</h3>
              <nav className="space-y-3">
                {[
                  'Disease Detection',
                  'Analysis Results',
                  'Treatment Guide',
                  'Crop Monitoring',
                  'Data Insights',
                  'Farmer Support'
                ].map((item) => (
                  <a
                    key={item}
                    href="#"
                    className="text-base font-light text-gray-300 hover:text-[#47f793] transition-colors duration-300"
                  >
                    {item}
                  </a>
                ))}
              </nav>
            </div>

            {/* Contact */}
            <div>
              <h3 className="text-sm font-light tracking-widest text-gray-400 mb-8 uppercase">Contact</h3>
              <div className="space-y-4">
                <p className="text-lg font-light text-white">
                  +1 (555) 123-4567
                </p>
                <p className="text-base font-light text-gray-300">
                  hello@fito.ai
                </p>
              </div>
            </div>
          </div>

          {/* Logo and Copyright */}
          <div className="border-t border-gray-800 pt-12 mt-12">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-8">
              <Link href="/home" className="flex items-center space-x-2 group">
                <span className="text-xl font-semibold text-white group-hover:text-[#47f793] transition-colors duration-300">FITO</span>
              </Link>
              <div className="flex items-center space-x-6">
                {/* Social Links */}
                {[
                  { icon: 'linkedin', label: 'LinkedIn' },
                  { icon: 'facebook', label: 'Facebook' },
                  { icon: 'instagram', label: 'Instagram' },
                  { icon: 'twitter', label: 'Twitter' }
                ].map((social) => (
                  <a
                    key={social.icon}
                    href="#"
                    className="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-[#47f793] transition-colors duration-300"
                    aria-label={social.label}
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      {social.icon === 'linkedin' && (
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                      )}
                      {social.icon === 'facebook' && (
                        <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                      )}
                      {social.icon === 'instagram' && (
                        <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0m0 22.065C6.92 22.065 2.935 18.08 2.935 12.935 2.935 7.79 6.92 3.805 12 3.805s9.065 3.985 9.065 9.13-3.985 9.13-9.065 9.13m4.5-15.5a1.125 1.125 0 110-2.25 1.125 1.125 0 010 2.25m-4.5 2.625a4.5 4.5 0 110 9 4.5 4.5 0 010-9"/>
                      )}
                      {social.icon === 'twitter' && (
                        <path d="M23.953 4.57a10 10 0 002.856-3.51 9.98 9.98 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                      )}
                    </svg>
                  </a>
                ))}
              </div>
            </div>

            <div className="mt-8 pt-8 border-t border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-sm font-light text-gray-400">
              <div className="space-x-6">
                <a href="#" className="hover:text-[#47f793] transition-colors duration-300">Privacy Policy</a>
                <a href="#" className="hover:text-[#47f793] transition-colors duration-300">Terms & Conditions</a>
              </div>
              <p>Copyright © 2024 Fito. All Rights Reserved.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
