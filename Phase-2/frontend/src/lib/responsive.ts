/**
 * Responsive Design Utilities
 *
 * Breakpoints:
 * - sm: 640px (mobile)
 * - md: 768px (tablet)
 * - lg: 1024px (desktop)
 * - xl: 1280px (large desktop)
 */

export const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
} as const

export type Breakpoint = keyof typeof breakpoints

export const containerClasses = {
  // Max width containers for different breakpoints
  full: 'w-full',
  sm: 'w-full sm:max-w-sm',
  md: 'w-full md:max-w-md',
  lg: 'w-full lg:max-w-lg',
  xl: 'w-full xl:max-w-xl',
  '2xl': 'w-full xl:max-w-2xl',
  '4xl': 'w-full xl:max-w-4xl',
  '6xl': 'w-full xl:max-w-6xl',
} as const

export const gridClasses = {
  // Single column on mobile, responsive on larger screens
  auto: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
  '2col': 'grid-cols-1 md:grid-cols-2',
  '3col': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
  '4col': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
} as const

export const textSizeClasses = {
  h1: 'text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold',
  h2: 'text-xl sm:text-2xl md:text-3xl font-bold',
  h3: 'text-lg sm:text-xl font-semibold',
  body: 'text-sm sm:text-base md:text-lg',
  small: 'text-xs sm:text-sm',
} as const

export const spacingClasses = {
  // Responsive padding
  p: 'p-3 sm:p-4 md:p-6 lg:p-8',
  py: 'py-3 sm:py-4 md:py-6 lg:py-8',
  px: 'px-3 sm:px-4 md:px-6 lg:px-8',
  // Responsive gap
  gap: 'gap-3 sm:gap-4 md:gap-6 lg:gap-8',
} as const

export const navClasses = {
  // Responsive navigation styles
  container: 'flex flex-col sm:flex-row justify-between items-center gap-2 sm:gap-4',
  links: 'flex flex-col sm:flex-row gap-2 sm:gap-4 w-full sm:w-auto',
} as const

/**
 * Media query hooks for responsive components
 */
export function useMediaQuery(minWidth: number): boolean {
  if (typeof window === 'undefined') return false
  return window.innerWidth >= minWidth
}

export function useIsMobile(): boolean {
  return useMediaQuery(640) === false
}

export function useIsTablet(): boolean {
  const isMobile = useIsMobile()
  const isDesktop = useMediaQuery(1024)
  return !isMobile && !isDesktop
}

export function useIsDesktop(): boolean {
  return useMediaQuery(1024)
}
