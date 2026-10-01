#!/usr/bin/env python3
"""Pack the entire 17-page Vanguard site into ONE self-contained .html file.
Run:  python3 pack_single.py   →  ../vanguard-placement-group.html
"""
import re, os, collections
import build

# ---- capture every page body instead of writing files -----------------------
PAGES = collections.OrderedDict()

def collect(slug, title, desc, body, active=None):
    PAGES[slug] = dict(title=title, desc=desc, body=body, active=active or slug)
    return slug

build.page = collect
build.build_home(); build.build_talent(); build.build_shortlisted(); build.build_submit()
build.build_how(); build.build_agencies(); build.build_stories(); build.build_about()
build.build_faq(); build.build_contact(); build.build_404()
for t in build.TALENT:
    build.profile_page(t)

route = lambda slug: 'home' if slug == 'index.html' else slug[:-5]

def rewrite(html):
    """point every internal .html link at the in-file router"""
    def sub(m):
        href = m.group(1)
        return f'href="#/{route(href)}"'
    return re.sub(r'href="([a-z0-9\-]+\.html)"', sub, html)

CSS = open('styles.css').read()
JS  = rewrite(open('main.js').read())   # chatbot answers link internally too

NAV = rewrite(build.nav_html('index.html'))
FOOT = rewrite(build.FOOTER)
FOOT = FOOT.replace('<script src="main.js" defer></script>', '').replace('</body>\n</html>', '')

ROUTES = "\n".join(
    f'<div class="route" id="route-{route(slug)}" data-title="{p["title"]}">\n{rewrite(p["body"])}\n</div>'
    for slug, p in PAGES.items())

EXTRA_CSS = """
/* ---- single-file router ---- */
.route{display:none}
.route.on{display:block;animation:routeIn .45s cubic-bezier(.2,.8,.2,1)}
@keyframes routeIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
"""

ROUTER_JS = """
/* ============================================================
   SINGLE-FILE ROUTER — every page lives in this one document
   ============================================================ */
(function router(){
  const routes = [...document.querySelectorAll('.route')];
  const ids = routes.map(r => r.id.replace('route-',''));
  const navLinks = [...document.querySelectorAll('.nav-links a, .mobile-menu a')];

  function counters(scope){
    scope.querySelectorAll('.count').forEach(el => {
      if (el.dataset.done) return;
      el.dataset.done = '1';
      const target = parseFloat(el.dataset.count), dec = +(el.dataset.decimals||0), comma = el.dataset.comma;
      let start = null;
      const step = ts => {
        if (!start) start = ts;
        const k = Math.min((ts - start)/1400, 1), v = target * (1 - Math.pow(1-k,3));
        el.textContent = comma ? Math.round(v).toLocaleString() : v.toFixed(dec);
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }

  function show(name, push){
    if (!ids.includes(name)) name = '404';
    routes.forEach(r => r.classList.toggle('on', r.id === 'route-' + name));
    const cur = document.getElementById('route-' + name);
    document.title = cur.dataset.title || 'Vanguard Placement Group';
    // elements inside a hidden route never trip the scroll observer — reveal them now
    setTimeout(() => { cur.querySelectorAll('.reveal').forEach(el => el.classList.add('in')); counters(cur); }, 60);
    navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#/' + name));
    document.querySelector('.mobile-menu')?.classList.remove('open');
    if (push !== false) scrollTo({top:0, behavior:'instant' in window ? 'instant' : 'auto'});
  }

  addEventListener('hashchange', () => {
    const h = location.hash.replace(/^#\\/?/, '');
    if (!h) return show('home');
    show(h);
  });

  const first = location.hash.replace(/^#\\/?/, '');
  show(first || 'home', false);
})();
"""

html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vanguard Placement Group — Raw Talent In. Big Opportunities Out.</title>
<meta name="description" content="Send your reel or resume. We shortlist it straight to the right desks. Helping independent talent secure agency representation — 48h average response.">
<meta property="og:type" content="website">
<meta property="og:title" content="Vanguard Placement Group — Raw Talent In. Big Opportunities Out.">
<meta property="og:description" content="Send your reel or resume. We shortlist it straight to the right desks.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23003087'/%3E%3Ctext x='32' y='45' font-family='Georgia,serif' font-weight='700' font-size='34' fill='white' text-anchor='middle'%3EV%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,500;0,600;0,700;0,800;1,500;1,600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>if(window.tailwind)tailwind.config={{theme:{{extend:{{colors:{{vanguard:'#003087',vanguardLift:'#2b6cff'}}}}}}}};</script>
<style>
{CSS}
{EXTRA_CSS}
</style>
</head>
<body>
<div class="reel-bg" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
{NAV}
{ROUTES}
{FOOT}
<script>
{JS}
{ROUTER_JS}
</script>
</body>
</html>
'''

out = os.path.join('..', 'vanguard-placement-group.html')
open(out, 'w').write(html)
print(f"wrote {out}  —  {len(html):,} bytes  ·  {len(PAGES)} pages inlined")
for s in PAGES: print("   #/" + route(s))
