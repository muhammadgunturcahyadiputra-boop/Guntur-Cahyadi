import re

with open('C:/Users/ASUS/portfolio-guntur/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update viewport for notch support
html = html.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />'
)

# 2. Add touch & input styles (prevent iOS zoom on input focus, smooth scrolling, safe areas)
custom_styles = """
    /* Mobile-first enhancements & iOS fixes */
    * {
      -webkit-tap-highlight-color: transparent;
    }
    html {
      scroll-padding-top: 5rem;
    }
    input, textarea, select {
      font-size: 16px !important; /* Prevents auto-zoom on iOS Safari */
    }
    .safe-bottom {
      padding-bottom: max(0.5rem, env(safe-area-inset-bottom));
    }
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
"""
if '/* Mobile-first enhancements' not in html:
    html = html.replace('.badge-glow {', custom_styles + '\n    .badge-glow {')

# 3. Add mobile bottom navigation bar before toast
bottom_nav = """
  <!-- MOBILE BOTTOM NAVIGATION (HP FRIENDLY) -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 dark:bg-dark-bg/95 backdrop-blur-lg border-t border-slate-200/80 dark:border-dark-border px-3 py-2 flex items-center justify-around safe-bottom transition-colors shadow-[0_-4px_20px_rgba(0,0,0,0.05)] dark:shadow-[0_-4px_20px_rgba(0,0,0,0.3)]">
    <a href="#home" class="flex flex-col items-center gap-1 py-1 px-2.5 text-slate-500 dark:text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
      <i data-lucide="home" class="w-4 h-4"></i>
      <span class="text-[10px] font-medium leading-none">Beranda</span>
    </a>
    <a href="#about" class="flex flex-col items-center gap-1 py-1 px-2.5 text-slate-500 dark:text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
      <i data-lucide="user" class="w-4 h-4"></i>
      <span class="text-[10px] font-medium leading-none">Tentang</span>
    </a>
    <a href="#skills" class="flex flex-col items-center gap-1 py-1 px-2.5 text-slate-500 dark:text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
      <i data-lucide="code-2" class="w-4 h-4"></i>
      <span class="text-[10px] font-medium leading-none">Keahlian</span>
    </a>
    <a href="#projects" class="flex flex-col items-center gap-1 py-1 px-2.5 text-slate-500 dark:text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
      <i data-lucide="folder-git-2" class="w-4 h-4"></i>
      <span class="text-[10px] font-medium leading-none">Proyek</span>
    </a>
    <a href="#contact" class="flex flex-col items-center gap-1 py-1 px-2.5 text-slate-500 dark:text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
      <i data-lucide="mail" class="w-4 h-4"></i>
      <span class="text-[10px] font-medium leading-none">Kontak</span>
    </a>
  </nav>
"""
if 'MOBILE BOTTOM NAVIGATION' not in html:
    html = html.replace('<!-- Notification Toast -->', bottom_nav + '\n  <!-- Notification Toast -->')

# 4. Adjust main/footer padding on mobile so content is not cut off by bottom nav
html = html.replace(
    '<main class="flex-grow pt-24 relative z-10">',
    '<main class="flex-grow pt-20 pb-16 md:pb-0 relative z-10">'
)
html = html.replace(
    '<footer class="py-8 border-t border-slate-200 dark:border-dark-border',
    '<footer class="py-8 mb-16 md:mb-0 border-t border-slate-200 dark:border-dark-border'
)

# 5. Toast position offset for mobile
html = html.replace(
    'id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none"',
    'id="toast" class="fixed bottom-20 md:bottom-6 right-4 md:right-6 left-4 md:left-auto z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none"'
)

# 6. Filter tabs: smooth horizontal scrolling on mobile
html = html.replace(
    'class="flex flex-wrap gap-2 mt-4 md:mt-0" id="projectFilter"',
    'class="flex gap-2 mt-4 md:mt-0 overflow-x-auto no-scrollbar pb-1 max-w-full" id="projectFilter"'
)

# 7. Close mobile menu when clicking outside
mobile_script_enhancement = """
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target) && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
      }
    });
"""
if 'Close mobile menu when clicking outside' not in html:
    html = html.replace("mobileMenuBtn.addEventListener('click', () => {", mobile_script_enhancement + "\n    mobileMenuBtn.addEventListener('click', () => {")

with open('C:/Users/ASUS/portfolio-guntur/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html mobile-friendly upgrade complete!")
