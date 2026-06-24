'use client'

export default function BackgroundProvider() {
  return (
    <div
      className="fixed inset-0 -z-50"
      style={{
        backgroundImage: 'url(/tomato_bg_all.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
        filter: 'blur(0px)',
      }}
    />
  )
}

export function BackgroundOverlay() {
  return (
    <div
      className="fixed inset-0 -z-40"
      style={{
        background: 'rgba(255, 255, 255, 0.92)',
        pointerEvents: 'none',
      }}
    />
  )
}
