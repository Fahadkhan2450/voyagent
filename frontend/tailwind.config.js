/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        dusk: {
          DEFAULT: "#0F2A3D",
          deep: "#0A1F2E",
          card: "#16374B",
          line: "#25506A",
        },
        amber: {
          DEFAULT: "#E8A33D",
          soft: "#F2C177",
        },
        lagoon: {
          DEFAULT: "#4FB3A9",
        },
        parchment: {
          DEFAULT: "#F5F1E8",
          muted: "#AFC2CD",
        },
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["Inter", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
