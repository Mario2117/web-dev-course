/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['polls/templates/**/*.html'],
  theme: {
    extend: {},
  },
  plugins: [  require('@tailwindcss/typography'),
	      require('@tailwindcss/aspect-ratio'),
	      require('@tailwindcss/forms'),
  ],
}

