import type { Config } from "tailwindcss";

const config: Config = {
    darkMode: "class",
    content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
  	extend: {
  		colors: {
  			background: 'hsl(var(--background), <alpha-value>)',
  			foreground: 'hsla(var(--foreground))',
  			card: {
  				DEFAULT: 'hsl(var(--card), <alpha-value>)',
  				foreground: 'hsla(var(--card-foreground))'
  			},
  			popover: {
  				DEFAULT: 'hsl(var(--popover), <alpha-value>)',
  				foreground: 'hsla(var(--popover-foreground))'
  			},
  			primary: {
  				DEFAULT: 'hsl(var(--primary), <alpha-value>)',
  				foreground: 'hsla(var(--primary-foreground))'
  			},
  			secondary: {
  				DEFAULT: 'hsl(var(--secondary), <alpha-value>)',
  				foreground: 'hsla(var(--secondary-foreground))'
  			},
  			muted: {
  				DEFAULT: 'hsl(var(--muted), <alpha-value>)',
  				foreground: 'hsla(var(--muted-foreground))'
  			},
  			accent: {
  				DEFAULT: 'hsl(var(--accent), <alpha-value>)',
  				foreground: 'hsla(var(--accent-foreground))'
  			},
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive), <alpha-value>)',
  				foreground: 'hsla(var(--destructive-foreground))'
  			},
  			border: 'hsla(var(--border))',
  			input: 'hsla(var(--input))',
  			ring: 'hsla(var(--ring))',
  			chart: {
  				'1': 'hsla(var(--chart-1))',
  				'2': 'hsla(var(--chart-2))',
  				'3': 'hsla(var(--chart-3))',
  				'4': 'hsla(var(--chart-4))',
  				'5': 'hsla(var(--chart-5))'
  			}
  		},
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		}
  	}
  }
};
export default config;
