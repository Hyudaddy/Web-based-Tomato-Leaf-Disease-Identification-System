'use client'

import { useEffect, useState, useRef } from 'react'
import Image from 'next/image'
import { diseaseDatabase } from '@/data/diseaseInfo'

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

const typeColors = {
  'Healthy': { text: 'text-green-700', badge: 'bg-green-100 text-green-800' },
  'Fungal': { text: 'text-orange-700', badge: 'bg-orange-100 text-orange-800' },
  'Bacterial': { text: 'text-red-700', badge: 'bg-red-100 text-red-800' },
  'Viral': { text: 'text-purple-700', badge: 'bg-purple-100 text-purple-800' },
  'Pest': { text: 'text-yellow-700', badge: 'bg-yellow-100 text-yellow-800' }
}

// Map disease names to their image folders
const diseaseImageMap: { [key: string]: string } = {
  'Healthy Tomato Leaf': 'healthy',
  'Early Blight': 'early blight',
  'Late Blight': 'late blight',
  'Septoria Leaf Spot': 'septoria leaf spot',
  'Bacterial Spot': 'bacterial spot',
  'Leaf Mold': 'leaf mold',
  'Yellow Leaf Curl Virus': 'yellow curl virus',
  'Mosaic Virus': 'mosaic virus',
  'Target Spot': 'target spot',
  'Spider Mites': 'spider mites'
}

// Store image filenames for each disease
const diseaseImages: { [key: string]: string[] } = {
  'healthy': ['1af0bfe1-4bcf-4b8b-be66-5d0953eb647e___GH_HL Leaf 482.2.JPG', '1bfeed83-f119-46cd-b806-0e17e1dae136___RS_HL 0017_180deg.JPG', '1ca23194-53c1-44a9-973a-39aa073f4a33___RS_HL 0058_180deg.JPG', '1ca3c77d-13d8-43cc-929f-9c3a79e5dd1b___RS_HL 0250.JPG', '1d024f2a-0ceb-4560-81fc-1114e6341f02___RS_HL 0431_flipTB.JPG'],
  'early blight': ['0bd357fe-1e54-4c65-979c-e894e0b8a3aa___RS_Erly.B 8328.JPG', '0db67be3-f733-4d15-b7d9-5d075b2cafc7___RS_Erly.B 6401.JPG', '0e2abcfb-e62b-4c61-a24a-0800cad904a8___RS_Erly.B 7382.JPG', '0f03a09c-aa48-4d51-95e1-752c466c3742___RS_Erly.B 6413.JPG', '0f7a2408-9c26-4ff9-bee5-2bfcd91a11f7___RS_Erly.B 9440.JPG'],
  'late blight': ['00ce4c63-9913-4b16-898c-29f99acf0dc3___RS_Late.B 4982_flipLR.JPG', '0a39aa48-3f94-4696-9e43-ff4a93529dc3___RS_Late.B 5103_flipLR.JPG', '0a4b3cde-c83a-4c83-b037-010369738152___RS_Late.B 6985_flipLR.JPG', '0d98a9eb-18e7-47e7-9010-196189bae113___RS_Late.B 5047_flipLR.JPG', '0da53824-7b3b-43a9-9b34-146a7f71ef7e___RS_Late.B 6958_flipLR.JPG'],
  'septoria leaf spot': ['0a25f893-1b5f-4845-baa1-f68ac03d96ac___Matt.S_CG 7863.JPG', '0a70601b-8511-4a56-9562-c95c46372874___Matt.S_CG 1032.JPG', '0aa486df-97b6-4764-89a9-d193e16aabbb___Keller.St_CG 1931.JPG', '0af9f990-ad92-4411-8623-4498ca4805ce___Keller.St_CG 1942.JPG', '0ea8a7c0-74f4-404b-81f4-233e501dab60___Matt.S_CG 6731_180deg.JPG'],
  'bacterial spot': ['0ab54691-ba9f-4c1f-a69b-ec0501df4401___GCREC_Bact.Sp 3170.JPG', '0ad88d7a-c14a-4ac9-8520-c11a0ade3a8f___UF.GRC_BS_Lab Leaf 0996.JPG', '0afe3bbd-b18b-4c70-8fbd-072844e742a2___GCREC_Bact.Sp 3434.JPG', '0c5eb8e4-e0fb-424a-8873-e43f9a6121ef___GCREC_Bact.Sp 6281.JPG', '0c9b7dd9-a0c7-4b6e-bb4d-b2e3cab833d0___GCREC_Bact.Sp 6081.JPG'],
  'leaf mold': ['0de02a32-f166-4d67-bbb8-689e96d04c44___Crnl_L.Mold 8811.JPG', '0eda4dc5-7f7b-4e27-9e53-1e0326eef88e___Crnl_L.Mold 8850.JPG', '0fd01669-64ab-4042-9715-bf1bcb2ccfbf___Crnl_L.Mold 6996.JPG', '1a1acd8f-bd8d-47be-945d-ce308dffd678___Crnl_L.Mold 6675.JPG', '1c03ffcb-9476-453c-96be-5bd1f629b2d1___Crnl_L.Mold 8853.JPG'],
  'yellow curl virus': ['10293c1b-da1e-4b3a-821e-4f71c54c2733___YLCV_NREC 2751.JPG', '36543f6a-1f3a-4371-8b0b-f60995a966a4___UF.GRC_YLCV_Lab 01266.JPG', '40928b95-6a82-4757-85e1-98d3930f1512___UF.GRC_YLCV_Lab 02076.JPG', '41278dff-4a95-43e8-8c9e-f8a6ec63b486___YLCV_NREC 2648.JPG', '46743c5e-9665-4ab9-aa10-20044684b87e___YLCV_GCREC 5224.JPG'],
  'mosaic virus': ['000ec6ea-9063-4c33-8abe-d58ca8a88878___PSU_CG 2169_270deg.JPG', '00c07a77-15e6-4815-92d4-8d1e1afb7f3c___PSU_CG 2052_180deg.JPG', '0c779116-043c-4715-b080-16be2e8d2552___PSU_CG 2285_90deg.JPG', '1b9dc07a-40ab-45bc-a873-1ad4212e35a3___PSU_CG 2289.JPG', '1ccfd473-6b3d-47a9-897b-0653d7683d75___PSU_CG 2163_180deg.JPG'],
  'target spot': ['0b126ce6-af82-477f-8f4e-1de79d84a6dd___Com.G_TgS_FL 8294_flipTB.JPG', '0df45326-8aa9-49bf-a2fd-e7f454c2dfbf___Com.G_TgS_FL 9718_180deg.JPG', '0eaa45be-4346-4e3c-ab6f-4ce9f9aec1db___Com.G_TgS_FL 7902_180deg.JPG', '0ed61d9f-3301-4088-a020-ccc9ebed8b21___Com.G_TgS_FL 8399_180deg.JPG', '0f9aa748-57f0-4b14-98c0-b9c1966badc9___Com.G_TgS_FL 9854_flipTB.JPG'],
  'spider mites': ['0cee18fc-bbbd-40dd-8d73-93df072c09ea___Com.G_SpM_FL 8904.JPG', '0f6a5f32-3d95-4ef1-bc01-ba36f2efb2b4___Com.G_SpM_FL 1661_180deg.JPG', '0f94b000-c54f-45c1-b976-22cb57dda0c4___Com.G_SpM_FL 9640.JPG', '1b51a575-adbd-406b-8371-754b6009e7fb___Com.G_SpM_FL 1769.JPG', '1ba7b39c-c687-42da-b283-edf7a03b17b7___Com.G_SpM_FL 9484_flipTB.JPG']
}

const getDiseaseFolderImages = (folderName: string): string[] => {
  return diseaseImages[folderName] || []
}

export default function InformationPage() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  // Model evaluation metrics
  const evaluationMetrics = {
    accuracy: {
      value: 0.8504,
      percentage: 85.04,
      description: 'The proportion of correct predictions out of all predictions made. It measures overall correctness of the model.',
      formula: '(TP + TN) / (TP + TN + FP + FN)'
    },
    precision: {
      value: 0.8234,
      percentage: 82.34,
      description: 'Of all predictions marked as positive (disease), how many were actually correct. Focuses on minimizing false positives.',
      formula: 'TP / (TP + FP)'
    },
    recall: {
      value: 0.7891,
      percentage: 78.91,
      description: 'Of all actual positive cases, how many were correctly identified. Important for catching all disease cases.',
      formula: 'TP / (TP + FN)'
    },
    f1Score: {
      value: 0.8060,
      percentage: 80.60,
      description: 'The harmonic mean of precision and recall. Provides a balanced score between the two metrics.',
      formula: '2 × (Precision × Recall) / (Precision + Recall)'
    }
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Title Section with Typewriter */}
      <section className="relative min-h-[60vh] pt-32 pb-20 flex items-center justify-center">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div 
            className={`transition-all duration-1500 ease-out ${
              mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-normal text-gray-900 leading-tight tracking-tight">
              <Typewriter text="Disease Library & Information" />
            </h1>
          </div>
        </div>
      </section>

      {/* Divider */}
      <div className="border-t border-gray-200"></div>

      {/* Disease Library Section */}
      <section className="py-20 md:py-32">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          {diseaseDatabase.map((disease, index) => (
            <AnimatedSection key={disease.id} delay={index * 100}>
              <div className="mb-20 md:mb-32 pb-20 md:pb-32 border-b border-gray-200 last:border-0">
                {/* Disease Name and Type */}
                <div className="mb-6">
                  <div className="flex items-center gap-4 mb-3">
                    <h2 className={`text-4xl md:text-5xl font-normal text-gray-900 tracking-tight`}>
                      {disease.name}
                    </h2>
                    <span className={`inline-block px-4 py-1 rounded-full text-sm font-semibold ${
                      typeColors[disease.type as keyof typeof typeColors].badge
                    }`}>
                      {disease.type}
                    </span>
                  </div>
                  <p className="text-lg md:text-xl text-gray-600 italic">{disease.scientificName}</p>
                </div>

                {/* Images in One Line */}
                <div className="mb-12">
                  <p className="text-sm text-gray-500 mb-4 font-medium">Sample Images</p>
                  <div className="flex gap-3 overflow-x-auto pb-4">
                    {[1, 2, 3, 4, 5].map((i) => {
                      const folderName = diseaseImageMap[disease.name] || 'healthy'
                      const images = getDiseaseFolderImages(folderName)
                      const imageName = images[i - 1] || null
                      
                      return (
                        <div
                          key={i}
                          className="flex-shrink-0 w-40 h-40 md:w-48 md:h-48 rounded-lg overflow-hidden bg-gray-100 border border-gray-200 hover:shadow-lg transition-shadow duration-300"
                        >
                          {imageName ? (
                            <Image
                              src={`/diseases/${folderName}/${imageName}`}
                              alt={`${disease.name} - Sample ${i}`}
                              width={200}
                              height={200}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-sm text-gray-400">
                              <span>No Image</span>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>

                {/* Severity Indicator */}
                <div className="mb-8 flex items-center gap-4">
                  <div className="w-32">
                    <div className="text-xs text-gray-600 mb-2 font-medium">Severity</div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${
                          disease.severity === 'Low' ? 'bg-green-500' :
                          disease.severity === 'Medium' ? 'bg-yellow-500' :
                          disease.severity === 'High' ? 'bg-orange-500' :
                          'bg-red-500'
                        }`}
                        style={{
                          width: `${
                            disease.severity === 'Low' ? '25%' :
                            disease.severity === 'Medium' ? '50%' :
                            disease.severity === 'High' ? '75%' :
                            '100%'
                          }`
                        }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-sm font-medium text-gray-700">{disease.severity}</span>
                </div>

                {/* Disease Information Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                  {/* Left Column */}
                  <div className="space-y-8">
                    {/* Symptoms */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-4">Symptoms</h5>
                      <ul className="text-sm text-gray-700 space-y-2">
                        {disease.symptoms.map((symptom, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="mr-3 text-gray-400 mt-0.5">→</span>
                            <span>{symptom}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Visual Cues */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-4">Visual Cues</h5>
                      <ul className="text-sm text-gray-700 space-y-2">
                        {disease.visualCues.map((cue, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="mr-3 text-gray-400 mt-0.5">→</span>
                            <span>{cue}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Right Column */}
                  <div className="space-y-8">
                    {/* Treatment */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-4">Treatment</h5>
                      <ul className="text-sm text-gray-700 space-y-2">
                        {disease.treatment.map((treatment, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="mr-3 text-gray-400 mt-0.5">→</span>
                            <span>{treatment}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Prevention */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-4">Prevention</h5>
                      <ul className="text-sm text-gray-700 space-y-2">
                        {disease.prevention.map((prevention, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="mr-3 text-gray-400 mt-0.5">→</span>
                            <span>{prevention}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Impact */}
                <div className="mt-12 pt-8 border-t border-gray-200">
                  <h5 className="text-sm font-semibold text-gray-900 mb-3">Impact</h5>
                  <p className="text-base text-gray-700 leading-relaxed">{disease.impact}</p>
                </div>
              </div>
            </AnimatedSection>
          ))}
        </div>
      </section>

      {/* Divider */}
      <div className="border-t border-gray-200"></div>

      {/* Model Evaluation Metrics Section */}
      <section className="py-20 md:py-32">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection>
            <h2 className="text-4xl md:text-5xl font-normal text-gray-900 mb-12 md:mb-20">
              Model Evaluation Metrics
            </h2>
          </AnimatedSection>

          <AnimatedSection delay={100}>
            <p className="text-lg text-gray-700 mb-16 leading-relaxed max-w-3xl">
              Our FITO disease identification model is evaluated using multiple metrics to ensure reliable and accurate predictions. Here's what each metric means and how they contribute to understanding model performance.
            </p>
          </AnimatedSection>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-16 mb-16">
            {/* Accuracy */}
            <AnimatedSection delay={150}>
              <div>
                <div className="mb-8">
                  <h3 className="text-2xl md:text-3xl font-normal text-gray-900 mb-3">Accuracy</h3>
                  <div className="text-5xl font-normal text-[#47f793] mb-4">
                    {evaluationMetrics.accuracy.percentage.toFixed(2)}%
                  </div>
                </div>
                <div className="space-y-6">
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">What it means:</h5>
                    <p className="text-sm md:text-base text-gray-700 leading-relaxed">
                      {evaluationMetrics.accuracy.description}
                    </p>
                  </div>
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">Formula:</h5>
                    <div className="bg-gray-50 p-4 rounded-lg text-sm font-mono text-gray-900 border border-gray-200">
                      {evaluationMetrics.accuracy.formula}
                    </div>
                  </div>
                </div>
              </div>
            </AnimatedSection>

            {/* Precision */}
            <AnimatedSection delay={200}>
              <div>
                <div className="mb-8">
                  <h3 className="text-2xl md:text-3xl font-normal text-gray-900 mb-3">Precision</h3>
                  <div className="text-5xl font-normal text-[#47f793] mb-4">
                    {evaluationMetrics.precision.percentage.toFixed(2)}%
                  </div>
                </div>
                <div className="space-y-6">
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">What it means:</h5>
                    <p className="text-sm md:text-base text-gray-700 leading-relaxed">
                      {evaluationMetrics.precision.description}
                    </p>
                  </div>
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">Formula:</h5>
                    <div className="bg-gray-50 p-4 rounded-lg text-sm font-mono text-gray-900 border border-gray-200">
                      {evaluationMetrics.precision.formula}
                    </div>
                  </div>
                </div>
              </div>
            </AnimatedSection>

            {/* Recall */}
            <AnimatedSection delay={250}>
              <div>
                <div className="mb-8">
                  <h3 className="text-2xl md:text-3xl font-normal text-gray-900 mb-3">Recall</h3>
                  <div className="text-5xl font-normal text-[#47f793] mb-4">
                    {evaluationMetrics.recall.percentage.toFixed(2)}%
                  </div>
                </div>
                <div className="space-y-6">
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">What it means:</h5>
                    <p className="text-sm md:text-base text-gray-700 leading-relaxed">
                      {evaluationMetrics.recall.description}
                    </p>
                  </div>
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">Formula:</h5>
                    <div className="bg-gray-50 p-4 rounded-lg text-sm font-mono text-gray-900 border border-gray-200">
                      {evaluationMetrics.recall.formula}
                    </div>
                  </div>
                </div>
              </div>
            </AnimatedSection>

            {/* F1 Score */}
            <AnimatedSection delay={300}>
              <div>
                <div className="mb-8">
                  <h3 className="text-2xl md:text-3xl font-normal text-gray-900 mb-3">F1 Score</h3>
                  <div className="text-5xl font-normal text-[#47f793] mb-4">
                    {evaluationMetrics.f1Score.percentage.toFixed(2)}%
                  </div>
                </div>
                <div className="space-y-6">
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">What it means:</h5>
                    <p className="text-sm md:text-base text-gray-700 leading-relaxed">
                      {evaluationMetrics.f1Score.description}
                    </p>
                  </div>
                  <div>
                    <h5 className="text-sm font-semibold text-gray-900 mb-2">Formula:</h5>
                    <div className="bg-gray-50 p-4 rounded-lg text-sm font-mono text-gray-900 border border-gray-200">
                      {evaluationMetrics.f1Score.formula}
                    </div>
                  </div>
                </div>
              </div>
            </AnimatedSection>
          </div>

          {/* Understanding Metrics Section */}
          <AnimatedSection delay={350}>
            <div className="border-t border-gray-200 pt-16 md:pt-20">
              <h3 className="text-2xl md:text-3xl font-normal text-gray-900 mb-12">Understanding the Metrics</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div>
                  <h5 className="font-semibold text-gray-900 mb-3">Why Multiple Metrics?</h5>
                  <p className="text-base text-gray-700 leading-relaxed">
                    A single accuracy score isn't enough. Different metrics capture different aspects of model performance. For disease identification, we care about catching all diseases (recall) while minimizing false alarms (precision).
                  </p>
                </div>
                <div>
                  <h5 className="font-semibold text-gray-900 mb-3">What's the Ideal Score?</h5>
                  <p className="text-base text-gray-700 leading-relaxed">
                    Scores range from 0-100%. Higher is better. Our model scores in the 78-85% range, indicating good but not perfect performance. Real-world conditions and image quality variations affect predictions.
                  </p>
                </div>
                <div>
                  <h5 className="font-semibold text-gray-900 mb-3">Legend (TP, TN, FP, FN):</h5>
                  <ul className="space-y-2 text-base text-gray-700">
                    <li><strong>TP:</strong> True Positives - Correctly identified diseases</li>
                    <li><strong>TN:</strong> True Negatives - Correctly identified healthy leaves</li>
                    <li><strong>FP:</strong> False Positives - Healthy leaves marked as diseased</li>
                    <li><strong>FN:</strong> False Negatives - Diseases missed</li>
                  </ul>
                </div>
                <div>
                  <h5 className="font-semibold text-gray-900 mb-3">Best Practices for Using FITO</h5>
                  <ul className="space-y-2 text-base text-gray-700">
                    <li>• Use clear, well-lit images</li>
                    <li>• Photograph multiple leaves if possible</li>
                    <li>• Compare results with our disease library</li>
                    <li>• When uncertain, consult with agronomists</li>
                  </ul>
                </div>
              </div>
            </div>
          </AnimatedSection>
        </div>
      </section>
    </div>
  )
}
