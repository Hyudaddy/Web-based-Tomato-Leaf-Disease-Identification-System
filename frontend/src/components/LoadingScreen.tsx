'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'

interface LoadingScreenProps {
  onComplete: () => void
}

export default function LoadingScreen({ onComplete }: LoadingScreenProps) {
  const [progress, setProgress] = useState(0)
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsComplete(true)
          setTimeout(() => {
            onComplete()
          }, 300)
          return 100
        }
        return prev + 2
      })
    }, 30)

    return () => clearInterval(interval)
  }, [onComplete])

  return (
    <div className={`fixed inset-0 bg-white z-50 transition-opacity duration-300 flex items-center justify-center ${isComplete ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}>
      <div className="flex flex-col items-center justify-center gap-8">
        {/* FITO Logo - Large and Noticeable */}
        <div className="relative">
          <Image 
            src="/fito_loading_logo.png" 
            alt="FITO Loading Logo" 
            width={240} 
            height={240}
            priority
            className="w-60 h-60 animate-pulse"
          />
        </div>
        
        {/* Progress Indicator */}
        <div className="text-center">
          <div className="text-9xl font-bold text-[#47f793] tracking-[-0.02em] font-montserrat" style={{ fontWeight: 700 }}>
            {progress}%
          </div>
        </div>
      </div>
    </div>
  )
}


