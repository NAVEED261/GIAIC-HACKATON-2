import Link from 'next/link'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a1a2e] via-[#16213e] to-[#0f3460] flex flex-col">
      {/* Navigation */}
      <nav className="bg-[#1a1a2e]/80 backdrop-blur-md border-b border-[#e94560]/20">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-[#e94560]">
            Task Manager
          </Link>
          <Link href="/" className="text-white hover:text-[#e94560] font-medium transition-colors">
            Back to Home
          </Link>
        </div>
      </nav>

      {/* Auth Content */}
      <div className="flex-1 flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md">
          {children}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-[#1a1a2e]/80 border-t border-[#e94560]/20 text-white py-8">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p className="text-gray-400">&copy; 2025 Hackathon-2 Task Manager • Built with ❤ & AI</p>
          <p className="text-xs text-gray-500 mt-1">DEVELOPED BY: HAFIZ NAVEED UDDIN</p>
        </div>
      </footer>
    </div>
  )
}
