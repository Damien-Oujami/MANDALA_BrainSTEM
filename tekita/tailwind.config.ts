import type { Config } from 'tailwindcss'

export default {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0A0F1C',
        teal: '#00C7B7',
        magenta: '#E62BA5',
        sky: '#1F6FEB',
        honey: '#FFC857',
        text: '#F2F5F9',
      },
      boxShadow: {
        glow: '0 0 24px rgba(230,43,165,0.15), 0 0 36px rgba(0,199,183,0.12)'
      }
    },
  },
  plugins: [],
} satisfies Config
