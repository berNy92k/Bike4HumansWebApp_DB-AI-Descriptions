import type { ReactNode, SVGProps } from 'react'

// Small inline SVG icon set (stroke="currentColor", so they inherit text color and work in
// both themes/active states automatically) — used instead of emoji, which don't render
// consistently across every OS/browser font setup.
type IconProps = SVGProps<SVGSVGElement>

function Icon({ children, ...props }: IconProps & { children: ReactNode }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.8}
      strokeLinecap="round"
      strokeLinejoin="round"
      width="1em"
      height="1em"
      {...props}
    >
      {children}
    </svg>
  )
}

export function IconHome(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M3 11.5 12 4l9 7.5" />
      <path d="M5.5 10v9a1 1 0 0 0 1 1H9a1 1 0 0 0 1-1v-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v4a1 1 0 0 0 1 1h2.5a1 1 0 0 0 1-1v-9" />
    </Icon>
  )
}

export function IconBike(props: IconProps) {
  return (
    <Icon {...props}>
      <circle cx="5.5" cy="17.5" r="3.5" />
      <circle cx="18.5" cy="17.5" r="3.5" />
      <path d="M5.5 17.5 10 8h4l2.5 4.5M10 8 8.5 6h-2M10 8l3 5.5h5.5M13 13.5 15.5 8" />
    </Icon>
  )
}

export function IconFactory(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M3 20V11l6 4v-4l6 4v-4l6 4v5z" />
      <path d="M3 20h18" />
      <path d="M8 20v-3M13 20v-3M18 20v-3" />
    </Icon>
  )
}

export function IconUser(props: IconProps) {
  return (
    <Icon {...props}>
      <circle cx="12" cy="8" r="3.5" />
      <path d="M4.5 20c1-4 4-6 7.5-6s6.5 2 7.5 6" />
    </Icon>
  )
}

export function IconShield(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M12 3.5 19 6v5.5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z" />
    </Icon>
  )
}

export function IconPackage(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M3.5 8 12 4l8.5 4-8.5 4-8.5-4Z" />
      <path d="M3.5 8v9L12 21l8.5-4V8" />
      <path d="M12 12v9" />
    </Icon>
  )
}

export function IconCreditCard(props: IconProps) {
  return (
    <Icon {...props}>
      <rect x="3" y="6" width="18" height="13" rx="1.5" />
      <path d="M3 10.5h18M7 14.5h4" />
    </Icon>
  )
}

export function IconCart(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M3.5 4h2l2.4 11.5a1.5 1.5 0 0 0 1.5 1.2h8.3a1.5 1.5 0 0 0 1.47-1.18L20.5 8H6" />
      <circle cx="10" cy="20" r="1.4" />
      <circle cx="17" cy="20" r="1.4" />
    </Icon>
  )
}

export function IconMoon(props: IconProps) {
  return (
    <Icon {...props}>
      <path d="M20 14.2A8.5 8.5 0 1 1 9.8 4a7 7 0 0 0 10.2 10.2Z" />
    </Icon>
  )
}

export function IconSun(props: IconProps) {
  return (
    <Icon {...props}>
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2.5v2M12 19.5v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.5 12h2M19.5 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
    </Icon>
  )
}
