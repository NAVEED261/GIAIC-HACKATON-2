import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Hackathon-2 Task Manager',
  description: 'A full-stack task management system',
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-light text-dark">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
