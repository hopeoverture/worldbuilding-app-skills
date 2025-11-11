'use client'

import * as React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Menu } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Separator } from '@/components/ui/separator'
import { ModeToggle } from '@/components/mode-toggle'
import { cn } from '@/lib/utils'

interface NavItem {
  title: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
}

interface AppShellProps {
  children: React.ReactNode
  navigation?: NavItem[]
  siteTitle?: string
}

export function AppShell({
  children,
  navigation = [],
  siteTitle = 'App',
}: AppShellProps) {
  const pathname = usePathname()
  const [open, setOpen] = React.useState(false)

  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-4">
            {/* Mobile menu trigger */}
            {navigation.length > 0 && (
              <Sheet open={open} onOpenChange={setOpen}>
                <SheetTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="md:hidden"
                    aria-label="Open menu"
                  >
                    <Menu className="h-5 w-5" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="w-64 pr-0">
                  <MobileNav
                    items={navigation}
                    pathname={pathname}
                    onItemClick={() => setOpen(false)}
                  />
                </SheetContent>
              </Sheet>
            )}

            {/* Site title */}
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-xl font-bold">{siteTitle}</span>
            </Link>
          </div>

          {/* Right side actions */}
          <div className="flex items-center gap-2">
            <ModeToggle />
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Desktop sidebar */}
        {navigation.length > 0 && (
          <aside className="hidden w-64 border-r bg-background md:block">
            <nav className="sticky top-16 flex h-[calc(100vh-4rem)] flex-col gap-2 p-4">
              <DesktopNav items={navigation} pathname={pathname} />
            </nav>
          </aside>
        )}

        {/* Main content */}
        <main id="main-content" className="flex-1">
          {children}
        </main>
      </div>
    </div>
  )
}

function MobileNav({
  items,
  pathname,
  onItemClick,
}: {
  items: NavItem[]
  pathname: string
  onItemClick: () => void
}) {
  return (
    <nav className="flex flex-col gap-2 py-4">
      {items.map((item) => {
        const Icon = item.icon
        const isActive = pathname === item.href

        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onItemClick}
            className={cn(
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
            )}
          >
            {Icon && <Icon className="h-4 w-4" />}
            {item.title}
          </Link>
        )
      })}
    </nav>
  )
}

function DesktopNav({
  items,
  pathname,
}: {
  items: NavItem[]
  pathname: string
}) {
  return (
    <>
      {items.map((item) => {
        const Icon = item.icon
        const isActive = pathname === item.href

        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
            )}
          >
            {Icon && <Icon className="h-4 w-4" />}
            {item.title}
          </Link>
        )
      })}
    </>
  )
}
