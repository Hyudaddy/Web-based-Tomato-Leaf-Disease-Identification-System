import type { Metadata } from 'next'
import { Inter, Montserrat } from 'next/font/google'
import './globals.css'
import Navigation from '@/components/Navigation'
import BackgroundProvider, { BackgroundOverlay } from '@/components/BackgroundProvider'

const inter = Inter({ subsets: ['latin'] })
const montserrat = Montserrat({ 
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-montserrat'
})

export const metadata: Metadata = {
  title: 'Fito - AI-Powered Tomato Disease Detection',
  description: 'Detect tomato leaf diseases with 85% accuracy using advanced AI technology. Get instant diagnosis, treatment recommendations, and prevention strategies.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} ${montserrat.variable}`}>
        <BackgroundProvider />
        <BackgroundOverlay />
        <Navigation />
        {children}
      </body>
    </html>
  )
}
