'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import { getDiseaseInfo } from '@/data/diseaseInfo'

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

interface PredictionResult {
  success: boolean
  prediction: string
  confidence: number
  confidence_level: string
  reliability: string
  all_predictions: Array<{
    class: string
    confidence: number
  }>
  safety_recommendations: {
    disclaimer: string
    confidence_threshold: string
    next_steps: string[]
    disease_info?: {
      treatment: string
      prevention: string
    }
  }
  filename: string
}

export default function FitoPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResult(null)
      setError(null)
    }
  }

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResult(null)
      setError(null)
    }
  }

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
  }

  const handlePredict = async () => {
    if (!selectedFile) return

    setIsLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      // Use the same host as the frontend but port 8000 for backend
      const backendUrl = `${window.location.protocol}//${window.location.hostname}:8000/predict`
      const response = await fetch(backendUrl, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const resetUpload = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    setResult(null)
    setError(null)
  }

  // Calculate model metrics (mock data for now)
  const modelMetrics = {
    accuracy: 0.8504,
    precision: 0.8234,
    recall: 0.7891,
    f1Score: 0.8060
  }

  const currentDiseaseInfo = result ? getDiseaseInfo(result.prediction) : null

  return (
    <div className="min-h-screen bg-white">
      {/* Four Grid Layout - 2x2 explicit grid */}
      <main className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-8">
        <AnimatedSection>
        <div className="grid grid-cols-1 lg:grid-cols-[400px_1fr] gap-x-8 gap-y-8">
          {/* TOP LEFT - Upload Section */}
          <div className="flex flex-col gap-8">
            {/* Upload Area - Fixed Height */}
            <div className="h-[400px]">
            {!selectedFile ? (
              <div
                  className="h-full border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-[#47f793] transition-all duration-300 ease-out cursor-pointer hover:bg-gray-50 flex items-center justify-center"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => document.getElementById('file-input')?.click()}
              >
                <div className="space-y-4">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto transition-all duration-300 ease-out hover:bg-[#47f793] group">
                      <svg className="w-8 h-8 text-gray-600 group-hover:text-gray-900 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </div>
                  <div>
                      <h4 className="text-lg font-medium text-gray-900 mb-2">
                      Upload Tomato Leaf
                    </h4>
                      <p className="text-sm text-gray-600">
                        Drag and drop or click to browse
                    </p>
                    </div>
                </div>
              </div>
            ) : (
                <div className="relative h-full">
                    <Image
                      src={previewUrl!}
                      alt="Uploaded tomato leaf"
                    width={400}
                    height={400}
                    className="w-full h-full rounded-lg object-cover"
                    />
                    <button
                      onClick={resetUpload}
                    className="absolute top-4 right-4 bg-white text-gray-900 rounded-full w-8 h-8 flex items-center justify-center hover:bg-gray-100 transition-all duration-300 ease-out shadow-lg hover:scale-110 active:scale-95"
                    >
                      ×
                    </button>
                  </div>
              )}
                </div>

              {/* Analyze Button - Always Visible */}
              <button
                onClick={handlePredict}
                disabled={isLoading || !selectedFile}
                className="w-full bg-gray-900 hover:bg-[#0F0F0F] disabled:bg-gray-400 text-white font-medium py-4 px-6 rounded-lg transition-all duration-300 ease-out hover:scale-[1.02] active:scale-95 disabled:hover:scale-100"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Analyzing...</span>
                  </div>
                ) : (
                  'Analyze Disease'
                )}
              </button>

            <input
              id="file-input"
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>

          {/* TOP RIGHT - Analysis Result + Evaluation System */}
          <div className="flex flex-col gap-8">
              {/* Main Analysis Score - Always Visible */}
              <div className="space-y-4">
                <h2 className="text-[40px] font-bold text-gray-900 tracking-tight" style={{ fontFamily: 'var(--font-montserrat), sans-serif' }}>
                  ANALYSIS / RESULT
                </h2>
                <div>
                  <div className="text-[64px] font-bold text-gray-900 leading-none" style={{ fontFamily: 'var(--font-montserrat), sans-serif' }}>
                    {result ? result.prediction : 'None'}
                  </div>
                  <div className="text-2xl text-gray-600 mt-2">
                    {result ? `${(result.confidence * 100).toFixed(2)}%` : '0%'}
                  </div>
                </div>
              </div>

              {/* Evaluation System - Always Visible with Green Theme */}
              <div className="border-t border-gray-200 pt-8">
                <h3 className="text-sm text-gray-600 mb-6">Evaluation System</h3>
                <div className="grid grid-cols-4 gap-6">
                  <div>
                    <div className="text-xs text-gray-600 mb-2">Accuracy</div>
                    <div className="text-xs text-[#47f793] font-semibold mb-3">
                      {result ? `${Math.round(modelMetrics.accuracy * 100)}%` : '0%'}
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-[#47f793] transition-all duration-500"
                        style={{ width: result ? `${modelMetrics.accuracy * 100}%` : '0%' }}
                      ></div>
                    </div>
                    <div className="text-sm font-medium text-gray-900 mt-3">
                      {result ? `${(modelMetrics.accuracy * 10).toFixed(2)} / 10` : '0.00 / 10'}
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-gray-600 mb-2">Precision</div>
                    <div className="text-xs text-gray-600 font-semibold mb-3">
                      {result ? `${Math.round(modelMetrics.precision * 100)}%` : '0%'}
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-[#47f793] transition-all duration-500"
                        style={{ width: result ? `${modelMetrics.precision * 100}%` : '0%' }}
                      ></div>
                    </div>
                    <div className="text-sm font-medium text-gray-900 mt-3">
                      {result ? `${(modelMetrics.precision * 10).toFixed(2)} / 10` : '0.00 / 10'}
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-gray-600 mb-2">Recall</div>
                    <div className="text-xs text-[#47f793] font-semibold mb-3">
                      {result ? `${Math.round(modelMetrics.recall * 100)}%` : '0%'}
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-[#47f793] transition-all duration-500"
                        style={{ width: result ? `${modelMetrics.recall * 100}%` : '0%' }}
                      ></div>
                    </div>
                    <div className="text-sm font-medium text-gray-900 mt-3">
                      {result ? `${(modelMetrics.recall * 10).toFixed(2)} / 10` : '0.00 / 10'}
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-gray-600 mb-2">F1-Score</div>
                    <div className="text-xs text-[#47f793] font-semibold mb-3">
                      {result ? `${Math.round(modelMetrics.f1Score * 100)}%` : '0%'}
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-[#47f793] transition-all duration-500"
                        style={{ width: result ? `${modelMetrics.f1Score * 100}%` : '0%' }}
                      ></div>
                    </div>
                    <div className="text-sm font-medium text-gray-900 mt-3">
                      {result ? `${(modelMetrics.f1Score * 10).toFixed(2)} / 10` : '0.00 / 10'}
                    </div>
                  </div>
                </div>
              </div>
          </div>

          {/* BOTTOM LEFT - All Predictions */}
          <div className="border-t border-gray-200 pt-8 space-y-6">
            <h3 className="text-sm text-gray-600 mb-4">All Predictions</h3>
            
            {result && result.all_predictions ? (
              <div className="space-y-4">
                {result.all_predictions.slice(0, 10).map((pred, index) => (
                  <div 
                    key={index} 
                    className="flex items-center justify-between py-4 border-b border-dotted border-gray-200 last:border-0"
                  >
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900">{pred.class}</div>
                    </div>
                    <div className="flex items-center space-x-8 text-sm">
                      <div className="w-24">
                        <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gray-900 transition-all duration-500"
                            style={{ width: `${pred.confidence * 100}%` }}
                          ></div>
                        </div>
                      </div>
                      <div className="font-bold text-gray-900 w-12 text-right">
                        {(pred.confidence * 10).toFixed(2)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-600">
                <p className="text-sm">No predictions available</p>
              </div>
            )}
          </div>

          {/* BOTTOM RIGHT - Disease Information */}
          <div className="border-t border-gray-200 pt-8 space-y-6">
              <h3 className="text-sm text-gray-600 mb-4">Disease Information</h3>
              
              {currentDiseaseInfo ? (
                <>
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-2">{currentDiseaseInfo.name}</h2>
                    <p className="text-sm text-gray-600 italic mb-3">{currentDiseaseInfo.scientificName}</p>
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                      currentDiseaseInfo.type === 'Healthy' ? 'bg-green-100 text-green-800' :
                      currentDiseaseInfo.type === 'Fungal' ? 'bg-orange-100 text-orange-800' :
                      currentDiseaseInfo.type === 'Bacterial' ? 'bg-red-100 text-red-800' :
                      currentDiseaseInfo.type === 'Viral' ? 'bg-purple-100 text-purple-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {currentDiseaseInfo.type}
                    </span>
                  </div>

                  {/* Symptoms */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-3">Symptoms</h5>
                    <ul className="text-sm text-gray-600 space-y-2">
                      {currentDiseaseInfo.symptoms.map((symptom, index) => (
                        <li key={index} className="flex items-start">
                          <span className="mr-2 text-gray-600">•</span>
                          <span>{symptom}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Visual Cues */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-3">Visual Cues</h5>
                    <ul className="text-sm text-gray-600 space-y-2">
                      {currentDiseaseInfo.visualCues.map((cue, index) => (
                        <li key={index} className="flex items-start">
                          <span className="mr-2 text-gray-600">•</span>
                          <span>{cue}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Treatment */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-3">Treatment</h5>
                    <ul className="text-sm text-gray-600 space-y-2">
                      {currentDiseaseInfo.treatment.map((treatment, index) => (
                        <li key={index} className="flex items-start">
                          <span className="mr-2 text-gray-600">•</span>
                          <span>{treatment}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Prevention */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-3">Prevention</h5>
                    <ul className="text-sm text-gray-600 space-y-2">
                      {currentDiseaseInfo.prevention.map((prevention, index) => (
                        <li key={index} className="flex items-start">
                          <span className="mr-2 text-gray-600">•</span>
                          <span>{prevention}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Impact */}
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">Impact</h5>
                    <p className="text-sm text-gray-600 leading-relaxed">{currentDiseaseInfo.impact}</p>
                  </div>
                </>
              ) : (
                <div className="text-center py-12 text-gray-600">
                  <p className="text-sm">No disease information available</p>
                </div>
              )}
          </div>
        </div>
        </AnimatedSection>
      </main>

      {/* Error Message */}
      {error && (
        <div className="fixed top-4 right-4 bg-red-50 border border-red-200 rounded-lg p-4 max-w-sm z-50">
          <div className="flex items-center">
            <div className="text-red-500 mr-3">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h4 className="text-red-800 font-medium">Error</h4>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}






