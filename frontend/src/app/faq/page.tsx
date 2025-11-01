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

export default function FAQPage() {
  const [mounted, setMounted] = useState(false)
  const [openIndex, setOpenIndex] = useState<number | null>(0)
  const scrollY = useScrollAnimation()

  useEffect(() => {
    setMounted(true)
  }, [])

  const parallax = (value: number) => value * 0.5

  const faqs = [
    {
      question: 'What is Fito?',
      answer: 'Fito is an AI-powered platform that uses advanced machine learning to detect tomato leaf diseases instantly from photos. Simply upload an image of a tomato leaf, and our system provides accurate diagnosis with treatment recommendations.'
    },
    {
      question: 'How accurate is Fito?',
      answer: 'Fito achieves 85% accuracy across 10 different tomato disease types. Our model has been trained on thousands of high-quality images and validated by agricultural experts to ensure reliable results you can trust.'
    },
    {
      question: 'How long does analysis take?',
      answer: 'Disease analysis takes less than 5 seconds from upload to diagnosis. Our system processes thousands of data points instantly to provide you with immediate, actionable results.'
    },
    {
      question: 'What tomato diseases can Fito detect?',
      answer: 'Fito can detect 10 major tomato leaf diseases including Early Blight, Late Blight, Septoria Leaf Spot, Two-spotted Spider Mite damage, Target Spot, Mosaic Virus, and more. Healthy leaves are also identified.'
    },
    {
      question: 'Do I need special equipment?',
      answer: 'No special equipment needed! Any smartphone or camera works. Simply take a clear photo of the affected tomato leaf and upload it through the Fito platform.'
    },
    {
      question: 'Is my data secure?',
      answer: 'Yes, we take data security seriously. Your images and personal information are encrypted and protected. We never share your data with third parties without explicit consent.'
    },
    {
      question: 'Can Fito work offline?',
      answer: 'Yes! Fito can work offline since the AI model runs locally on your device. The trained model file is included with the application, so disease detection happens entirely on your machine without needing internet connectivity.'
    },
    {
      question: 'What should I do after getting a diagnosis?',
      answer: 'After diagnosis, Fito provides treatment recommendations specific to the detected disease. We recommend consulting with local agricultural experts for additional guidance tailored to your region.'
    }
  ]

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
              <Typewriter text="Questions answered. Clarity provided." />
            </h1>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 md:py-32 border-t border-gray-200">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl">
            {faqs.map((faq, index) => (
              <AnimatedSection key={index} delay={index * 50}>
                <div className="pb-8 border-b border-gray-200 last:border-b-0">
                  <button
                    onClick={() => setOpenIndex(openIndex === index ? null : index)}
                    className="w-full text-left transition-all duration-300 ease-out hover:text-[#47f793] group"
                  >
                    <div className="flex items-start justify-between gap-6 py-4">
                      <h3 className="text-lg sm:text-xl font-normal text-gray-900 group-hover:text-[#47f793] transition-colors duration-300">
                        {faq.question}
                      </h3>
                      <div className={`flex-shrink-0 w-6 h-6 flex items-center justify-center transition-transform duration-300 ${openIndex === index ? 'rotate-180' : ''}`}>
                        <svg className="w-5 h-5 text-[#47f793]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                      </div>
                    </div>
                  </button>
                  
                  {openIndex === index && (
                    <div className="animate-in fade-in duration-300 pl-0">
                      <p className="text-base sm:text-lg font-light text-gray-700 leading-relaxed pb-4">
                        {faq.answer}
                      </p>
                    </div>
                  )}
                </div>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Still have questions? */}
      <section className="py-20 md:py-32 bg-gray-50 border-t border-gray-200">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection>
            <div className="text-center pt-12">
              <h2 className="text-4xl sm:text-5xl font-normal text-gray-900 mb-6">
                Didn't find what you're looking for?
              </h2>
              <p className="text-lg sm:text-xl font-light text-gray-700 mb-8 max-w-2xl mx-auto">
                Reach out to our team for personalized support and expert advice on using Fito or managing tomato crop health.
              </p>
              <Link
                href="/contact"
                className="inline-flex items-center justify-center px-8 py-4 bg-gray-900 text-white font-medium rounded-md hover:bg-[#47f793] hover:text-gray-900 transition-all duration-300 ease-out text-lg hover:shadow-lg hover:scale-105 active:scale-95"
              >
                Get in Touch
              </Link>
            </div>
          </AnimatedSection>
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
                {['Home', 'Fito', 'About', 'FAQ', 'Contact'].map((item) => (
                  <Link
                    key={item}
                    href={item === 'Home' ? '/home' : item === 'Fito' ? '/fito' : item === 'About' ? '/about' : item === 'FAQ' ? '/faq' : '/contact'}
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
