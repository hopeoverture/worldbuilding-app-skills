import { AppShell } from '@/components/app-shell'
import { FileText, Palette, SquareStack } from 'lucide-react'

const navigation = [
  {
    title: 'Forms',
    href: '/examples/forms',
    icon: FileText,
  },
  {
    title: 'Dialogs',
    href: '/examples/dialogs',
    icon: SquareStack,
  },
  {
    title: 'Theme',
    href: '/examples/theme',
    icon: Palette,
  },
]

export default function ExamplesLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <AppShell navigation={navigation} siteTitle="Examples">
      {children}
    </AppShell>
  )
}
