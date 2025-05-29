// ui/tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./app.jsx",
    "./index.jsx"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif']
      }
    },
  },
  plugins: [],
};
