const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: ["./assets/templates/index.html", "./assets/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        sans: ["Encode Sans", ...defaultTheme.fontFamily.sans],
        "sans-expanded": [
          "Encode Sans Expanded",
          ...defaultTheme.fontFamily.sans,
        ],
      },
      keyframes: {
        wiggle: {
          '0%, 100%': { transform: 'rotate(-2deg)' },
          '50%': { transform: 'rotate(2deg)' },
        },
        'button-pop': {
          '0%': { transform: 'scale(var(--btn-focus-scale, 0.95))' },
          '40%': { transform: 'scale(1.02)' },
          '100%': { transform: 'scale(1)' },
        },
      },
      animation: {
        wiggle: 'wiggle 200ms ease-in-out',
        'button-pop': 'button-pop var(--animation-btn, 0.25s) ease-out',
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
