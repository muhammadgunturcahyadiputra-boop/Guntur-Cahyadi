import re

with open('C:/Users/ASUS/portfolio-guntur/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add cache busting query to images
html = html.replace('assets/images/guntur_thumb.jpg', 'assets/images/guntur_thumb.jpg?v=2')
html = html.replace('assets/images/guntur_avatar.jpg', 'assets/images/guntur_avatar.jpg?v=2')

# 2. Add search bar + filter controls
old_filter_block = '''          <!-- Filter Tabs -->
          <div class="flex gap-2 mt-4 md:mt-0 overflow-x-auto no-scrollbar pb-1 max-w-full" id="projectFilter">
            <button data-filter="all" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition-all">Semua</button>
            <button data-filter="web" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border text-slate-600 dark:text-slate-300 hover:text-emerald-600 transition-all">Web App</button>
            <button data-filter="system" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border text-slate-600 dark:text-slate-300 hover:text-emerald-600 transition-all">Sistem & DevOps</button>
            <button data-filter="algorithm" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border text-slate-600 dark:text-slate-300 hover:text-emerald-600 transition-all">Algoritma C++</button>
          </div>'''

new_filter_block = '''          <!-- Search Input & Filter Tabs -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mt-4 md:mt-0 w-full md:w-auto">
            <!-- Search Bar -->
            <div class="relative w-full sm:w-56">
              <input type="text" id="projectSearch" placeholder="Cari proyek..." class="w-full pl-9 pr-3.5 py-1.5 text-xs rounded-lg bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all" />
              <i data-lucide="search" class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"></i>
            </div>
            <!-- Filter Pills -->
            <div class="flex gap-1.5 overflow-x-auto no-scrollbar pb-1 max-w-full shrink-0" id="projectFilter">
              <button data-filter="all" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition-all">Semua</button>
              <button data-filter="web" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border text-slate-600 dark:text-slate-300 hover:text-emerald-600 transition-all">Web</button>
              <button data-filter="system" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border text-slate-600 dark:text-slate-300 hover:text-emerald-600 transition-all">Sistem</button>
              <button data-filter="algorithm" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border text-slate-600 dark:text-slate-300 hover:text-emerald-600 transition-all">C++</button>
            </div>
          </div>'''

if old_filter_block in html:
    html = html.replace(old_filter_block, new_filter_block)
    print("Filter block updated with Search Bar")
else:
    print("Warning: old_filter_block not found")

# 3. Update JavaScript logic for combined filter + search
old_js_filter = '''    // Project Filtering
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => {
          b.classList.remove('bg-emerald-600', 'text-white');
          b.classList.add('bg-white', 'dark:bg-dark-card', 'text-slate-600', 'dark:text-slate-300');
        });
        btn.classList.add('bg-emerald-600', 'text-white');
        btn.classList.remove('bg-white', 'dark:bg-dark-card', 'text-slate-600', 'dark:text-slate-300');

        const filter = btn.getAttribute('data-filter');

        projectCards.forEach(card => {
          const category = card.getAttribute('data-category') || '';
          if (filter === 'all' || category.includes(filter)) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });'''

new_js_filter = '''    // Unified Project Filtering & Search
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    const projectSearchInput = document.getElementById('projectSearch');
    let currentFilter = 'all';

    function applyProjectFilter() {
      const searchTerm = (projectSearchInput ? projectSearchInput.value : '').toLowerCase().trim();

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category') || '';
        const cardText = card.innerText.toLowerCase();
        
        const matchesCategory = (currentFilter === 'all' || category.includes(currentFilter));
        const matchesSearch = !searchTerm || cardText.includes(searchTerm);

        if (matchesCategory && matchesSearch) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => {
          b.classList.remove('bg-emerald-600', 'text-white');
          b.classList.add('bg-white', 'dark:bg-dark-card', 'text-slate-600', 'dark:text-slate-300');
        });
        btn.classList.add('bg-emerald-600', 'text-white');
        btn.classList.remove('bg-white', 'dark:bg-dark-card', 'text-slate-600', 'dark:text-slate-300');

        currentFilter = btn.getAttribute('data-filter') || 'all';
        applyProjectFilter();
      });
    });

    if (projectSearchInput) {
      projectSearchInput.addEventListener('input', applyProjectFilter);
    }'''

if old_js_filter in html:
    html = html.replace(old_js_filter, new_js_filter)
    print("Filter JS updated successfully")
else:
    print("Warning: old_js_filter not found")

with open('C:/Users/ASUS/portfolio-guntur/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
