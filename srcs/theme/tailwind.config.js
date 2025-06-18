/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Wagtail templates
    '../weblog/templates/**/*.html',
    // Wagtail admin templates
    '../config/templates/**/*.html',
    // Wagtail admin static files
    '../config/static/wagtailadmin/**/*.js',
    // Wagtail admin static files
    '../config/static/wagtailadmin/**/*.css',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
} 