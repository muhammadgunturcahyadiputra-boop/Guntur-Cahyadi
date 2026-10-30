import re

with open('C:/Users/ASUS/portfolio-guntur/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Navbar logo replacement with Guntur photo
old_nav_logo = '''        <div class="w-9 h-9 rounded-lg bg-emerald-600 text-white flex items-center justify-center font-bold text-base shadow-sm group-hover:bg-emerald-700 transition-colors">
          G
        </div>'''
new_nav_logo = '''        <div class="relative w-9 h-9 shrink-0">
          <img src="assets/images/guntur_thumb.jpg" alt="Muhammad Guntur Cahyadi Putra" class="w-9 h-9 rounded-lg object-cover border border-emerald-500/40 shadow-sm group-hover:border-emerald-500 transition-all" />
        </div>'''
if old_nav_logo in html:
    html = html.replace(old_nav_logo, new_nav_logo)
    print("Replaced navbar logo with photo")
else:
    print("Warning: old_nav_logo not found directly, checking regex")

# 2. About personal card icon replacement with Guntur photo
old_about_icon = '''              <div class="w-20 h-20 rounded-2xl bg-emerald-600/10 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-6">
                <i data-lucide="user-check" class="w-10 h-10"></i>
              </div>'''
new_about_photo = '''              <div class="relative w-24 h-24 mb-6">
                <img src="assets/images/guntur_avatar.jpg" alt="Muhammad Guntur Cahyadi Putra" class="w-24 h-24 rounded-2xl object-cover border-2 border-emerald-500/40 shadow-md ring-4 ring-emerald-500/10" />
                <span class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-emerald-500 border-2 border-white dark:border-dark-card flex items-center justify-center text-white shadow-sm" title="Mahasiswa Aktif UNESA">
                  <i data-lucide="check" class="w-3.5 h-3.5 stroke-[3]"></i>
                </span>
              </div>'''
if old_about_icon in html:
    html = html.replace(old_about_icon, new_about_photo)
    print("Replaced about card icon with Guntur photo")
else:
    print("Warning: old_about_icon not found directly")

# 3. GitHub Contact item - add official GitHub SVG logo
github_svg = '''<svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'''

old_contact_github = '''              <div class="flex items-center gap-3.5 p-3.5 rounded-xl bg-slate-50 dark:bg-dark-card border border-slate-200 dark:border-dark-border">
                <div class="w-9 h-9 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                  <i data-lucide="github" class="w-4 h-4"></i>
                </div>
                <div>
                  <span class="text-[11px] font-mono text-slate-400 block">GitHub</span>
                  <a href="https://github.com/muhammadgunturcahyadiputra-boop" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-slate-800 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400">
                    muhammadgunturcahyadiputra-boop
                  </a>
                </div>
              </div>'''

new_contact_github = f'''              <div class="flex items-center gap-3.5 p-3.5 rounded-xl bg-slate-50 dark:bg-dark-card border border-slate-200 dark:border-dark-border hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                <div class="w-9 h-9 rounded-lg bg-slate-900 dark:bg-dark-surface text-white dark:text-slate-100 flex items-center justify-center shadow-sm">
                  {github_svg}
                </div>
                <div class="min-w-0 flex-1">
                  <span class="text-[11px] font-mono text-slate-400 block">GitHub</span>
                  <a href="https://github.com/muhammadgunturcahyadiputra-boop" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-slate-800 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 truncate block">
                    muhammadgunturcahyadiputra-boop
                  </a>
                </div>
              </div>'''

if old_contact_github in html:
    html = html.replace(old_contact_github, new_contact_github)
    print("Replaced GitHub contact card with official GitHub logo")
else:
    print("Warning: old_contact_github not found directly")

# 4. Also replace GitHub icon in Hero button & Projects with official SVG for 100% reliability
html = html.replace(
    '<i data-lucide="github" class="w-4 h-4"></i>\n            <span>GitHub Profil</span>',
    f'{github_svg}\n            <span>GitHub Profil</span>'
)
html = html.replace(
    '<span>Lihat Repository</span>\n                <i data-lucide="github" class="w-3.5 h-3.5"></i>',
    f'<span>Lihat Repository</span>\n                {github_svg}'
)

with open('C:/Users/ASUS/portfolio-guntur/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully with Guntur's photo and GitHub logo!")
