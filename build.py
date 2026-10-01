#!/usr/bin/env python3
"""Vanguard Placement Group — static site builder.
Run:  python3 build.py   → writes every .html page in this folder.
NOTE: talent names, credits and shortlist results are PLACEHOLDER data.
"""
import os, re

EMAIL = "vanguardplacementgroup@gmail.com"
UNS = "https://images.unsplash.com/photo-"
Q = "?auto=format&fit=crop&w=900&q=70"

# ----------------------------------------------------------------- talent data
TALENT = [
    dict(slug="liam-k", name="Liam K.", first="Liam", disc="Screen actor", cat="screen",
         city="London", status="Booked", stat_class="booked",
         headline="Lead in new Netflix series",
         photo="1500648767791-00dcc994a43e",
         age="28–35", height="6'0\"", accents="RP, Northern English, General American",
         langs="English, basic French", union="Equity", rep="Signed via Vanguard shortlist, 2026",
         reel="2 min 10 sec", training="Three years rep theatre, screen intensive at a London studio",
         desks="4", callbacks="3", response="19h",
         note="He does almost nothing in the third scene and it is the best thing on the tape. That is the clip we led with, and it is the clip the desk called about.",
         credits=[("2026", "Lead — untitled streaming drama (in production)"),
                  ("2025", "Supporting — independent feature, festival circuit"),
                  ("2025", "Guest lead — returning crime series, episode 4"),
                  ("2024", "National commercial — insurance campaign"),
                  ("2023", "Stage — two-hander, Edinburgh run")],
         gallery=["1507003211169-0a1dd7228f2d", "1485846234645-a62644f84728", "1536440136628-849c177e76a1"]),

    dict(slug="amara-o", name="Amara O.", first="Amara", disc="Screen actor", cat="screen",
         city="Manchester", status="In negotiation", stat_class="",
         headline="Recurring role, BBC drama",
         photo="1531123897727-8f129e1688ce",
         age="24–31", height="5'6\"", accents="Northern English, RP, Nigerian",
         langs="English, Yoruba", union="Equity", rep="In negotiation — two desks",
         reel="1 min 45 sec", training="Drama school graduate, 2023",
         desks="3", callbacks="2", response="31h",
         note="Comedy timing that does not announce itself. We sent her to a drama desk anyway, because the restraint is what sells the jokes.",
         credits=[("2026", "Recurring — returning network drama (terms in negotiation)"),
                  ("2025", "Short film lead — BIFA-qualifying festival"),
                  ("2024", "Supporting — streaming anthology, episode 2"),
                  ("2024", "Brand film — retail campaign, national"),
                  ("2023", "Stage — ensemble, regional theatre")],
         gallery=["1521119989659-a83eee488004", "1485846234645-a62644f84728", "1492691527719-9d1e07e534b4"]),

    dict(slug="diego-s", name="Diego S.", first="Diego", disc="Commercial talent", cat="commercial",
         city="Madrid", status="Signed", stat_class="signed",
         headline="Signed — three-year agency deal",
         photo="1506794778202-cad84cf45f1d",
         age="30–40", height="5'11\"", accents="Castilian Spanish, General American",
         langs="Spanish, English, Portuguese", union="Non-union", rep="Signed — three-year agreement, 2026",
         reel="1 min 30 sec", training="On-camera technique, Madrid; improv background",
         desks="2", callbacks="2", response="14h",
         note="Non-union, no agent, one decent commercial and a phone self-tape. Signed inside three weeks. The material was never the problem — nobody had put it in front of the right desk.",
         credits=[("2026", "Signed — commercial division, three-year term"),
                  ("2025", "National campaign — automotive, Iberia"),
                  ("2025", "Hero spot — telecoms, regional broadcast"),
                  ("2024", "Supporting — Spanish-language streaming series"),
                  ("2024", "Print campaign — menswear")],
         gallery=["1519085360753-af0119f7cbe7", "1485846234645-a62644f84728", "1516035069371-29a1b244cc32"]),

    dict(slug="noor-h", name="Noor H.", first="Noor", disc="Screen actor", cat="screen",
         city="Toronto", status="Booked", stat_class="booked",
         headline="Supporting lead, indie feature",
         photo="1544005313-94ddf0286df2",
         age="22–29", height="5'4\"", accents="Canadian, General American, Levantine Arabic",
         langs="English, Arabic, French", union="ACTRA apprentice", rep="Shortlisted to 3 desks — offer accepted",
         reel="2 min", training="Conservatory programme, Toronto",
         desks="3", callbacks="3", response="22h",
         note="Three desks, three callbacks. That almost never happens, and it happened because the reel opened on the one scene where she was not performing at all.",
         credits=[("2026", "Supporting lead — independent feature (post-production)"),
                  ("2025", "Series regular test — cable drama"),
                  ("2025", "Lead — web series, two seasons"),
                  ("2024", "Commercial — bank, national Canadian broadcast"),
                  ("2023", "Stage — new writing festival")],
         gallery=["1529626455594-4ff0802cfb7e", "1485846234645-a62644f84728", "1522556189639-b150ed9c4330"]),

    dict(slug="jonah-r", name="Jonah R.", first="Jonah", disc="Stage & screen", cat="stage",
         city="New York", status="In negotiation", stat_class="",
         headline="Series regular test, cable drama",
         photo="1492562080023-ab3db95bfbce",
         age="35–45", height="6'2\"", accents="New York, General American, Southern",
         langs="English", union="SAG-AFTRA", rep="Test option — terms in negotiation",
         reel="2 min 20 sec", training="Twelve years stage, Meisner-trained",
         desks="5", callbacks="2", response="27h",
         note="Twelve years of stage work and a reel cut like a theatre programme. We re-ordered it, led with the interrogation scene, and the first desk tested him.",
         credits=[("2026", "Series regular test — cable drama (in negotiation)"),
                  ("2025", "Co-star — network procedural, two episodes"),
                  ("2024", "Lead — off-Broadway revival"),
                  ("2024", "Supporting — independent thriller"),
                  ("2022", "Narration — documentary series")],
         gallery=["1507003211169-0a1dd7228f2d", "1485846234645-a62644f84728", "1489599849927-2ee91cede3ba"]),

    dict(slug="priya-n", name="Priya N.", first="Priya", disc="Voice & presenting", cat="voice",
         city="Dublin", status="Signed", stat_class="signed",
         headline="Signed — commercial division",
         photo="1529626455594-4ff0802cfb7e",
         age="26–34", height="5'7\"", accents="Irish, RP, Neutral Indian English",
         langs="English, Hindi", union="Non-union", rep="Signed — commercial division, 2026",
         reel="60 sec voice sample + 90 sec presenting",
         training="Broadcast journalism background, VO coaching",
         desks="2", callbacks="2", response="11h",
         note="A sixty-second sample with three clean reads beat every ten-minute demo in the pile that month. Range notes written out, no guessing required.",
         credits=[("2026", "Signed — commercial and voice division"),
                  ("2025", "Presenter — branded content series, six episodes"),
                  ("2025", "Voice — national radio campaign"),
                  ("2024", "Narration — corporate documentary"),
                  ("2024", "Host — live event, 900 attendees")],
         gallery=["1524504388940-b1c1722653e1", "1485846234645-a62644f84728", "1478737270239-2f02b77fc618"]),
]

NAVLINKS = [("index.html", "Home"), ("talent.html", "Our Talent"), ("shortlisted.html", "Shortlisted"),
            ("success-stories.html", "Testimonials"), ("about.html", "About")]

DD = [("how-it-works.html", "How It Works", "The 4-step vetting pipeline"),
      ("agencies.html", "For Agencies &amp; Casting", "Request a shortlist"),
      ("faq.html", "FAQ", "Every question, answered straight"),
      ("contact.html", "Contact", "Talk to the review desk")]


def logo_svg(bgvar="--bg"):
    return f'''<svg viewBox="0 0 120 120" aria-hidden="true">
        <circle cx="60" cy="60" r="57" fill="none" stroke="var(--logo-ink)" stroke-width="2.6" opacity=".9"/>
        <text x="34" y="74" font-family="Playfair Display, Georgia, serif" font-size="56" font-weight="800" fill="var(--logo-blue)" text-anchor="middle">V</text>
        <g transform="translate(78,48)">
          <circle r="16" fill="var(--logo-blue)"/><circle r="4.4" fill="var({bgvar})"/>
          <circle cx="0" cy="-9.5" r="3.3" fill="var({bgvar})"/><circle cx="0" cy="9.5" r="3.3" fill="var({bgvar})"/>
          <circle cx="-9.5" cy="0" r="3.3" fill="var({bgvar})"/><circle cx="9.5" cy="0" r="3.3" fill="var({bgvar})"/>
        </g>
        <text x="60" y="95" font-family="Inter, sans-serif" font-size="10.5" font-weight="900" letter-spacing="1.4" fill="var(--logo-ink)" text-anchor="middle">VANGUARD</text>
        <text x="60" y="106" font-family="Inter, sans-serif" font-size="7.6" font-weight="700" letter-spacing="1.1" fill="var(--logo-ink)" opacity=".75" text-anchor="middle">PLACEMENT GROUP</text>
      </svg>'''


def nav_html(active):
    links = "".join(
        f'<a href="{h}" class="{"active" if h == active else ""}">{t}</a>' for h, t in NAVLINKS)
    dd = "".join(f'<a href="{h}"><b>{t}</b><span>{s}</span></a>' for h, t, s in DD)
    mob = "".join(f'<a href="{h}">{t}</a>' for h, t in NAVLINKS + [(d[0], d[1]) for d in DD])
    return f'''
<div class="urgency" id="urgency">
  <span>⚠️ <b><span data-slots>3</span> shortlist slots left</b> this review cycle — intake closes in</span>
  <span class="cd" id="cdClock">—</span>
  <a href="submit.html">Send your reel →</a>
  <button class="ux" id="urgencyClose" aria-label="Dismiss">×</button>
</div>

<nav class="nav" id="nav">
  <div class="container nav-inner">
    <a href="index.html" class="logo" aria-label="Vanguard Placement Group — home">
      {logo_svg()}
      <span class="logo-txt"><b>Vanguard Placement Group</b><small>Talent Acquisitions</small></span>
    </a>
    <div class="nav-links">
      {links}
      <div class="dd"><button type="button">More ▾</button><div class="dd-menu">{dd}</div></div>
    </div>
    <div class="nav-right">
      <button class="theme-btn" id="themeBtn" aria-label="Switch colour mode" title="Light / dark">◐</button>
      <a href="submit.html" class="btn btn-primary btn-sm">Send Your Reel</a>
      <button class="menu-btn" id="menuBtn" aria-label="Menu"><span></span></button>
    </div>
  </div>
</nav>
<div class="mobile-menu" id="mobileMenu">{mob}
  <a href="submit.html" class="btn btn-primary" style="margin-top:16px;font-family:Inter,sans-serif;font-size:15px">Send Your Reel</a>
</div>'''


FOOTER = f'''
<footer class="footer" id="send">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="logo">{logo_svg("--bg-2")}
          <span class="logo-txt"><b>Vanguard Placement Group</b><small>Talent Acquisitions</small></span></a>
        <p>Helping independent talent secure agency representation. Reels and resumes reviewed by a real acquisitions desk, then shortlisted to the people who cast and sign.</p>
        <div class="f-contact">
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <span>Review Department · Talent Acquisitions</span>
          <span>Response time: 48 hours average</span>
          <span style="display:flex;gap:14px;margin-top:6px">
            <a href="talent.html">Our Talent</a><a href="shortlisted.html">Shortlisted</a>
            <a href="how-it-works.html">How It Works</a><a href="faq.html">FAQ</a>
          </span>
        </div>
      </div>

      <div class="form-card">
        <h4>Send your reel</h4>
        <p>One minute, five fields. A link is all we need.</p>
        <form class="simple-form" novalidate>
          <div class="f-row">
            <label class="field"><span>Your name</span><input type="text" name="name" placeholder="Alex Moore" required></label>
            <label class="field"><span>Email</span><input type="email" name="email" placeholder="you@email.com" required></label>
          </div>
          <div class="f-row">
            <label class="field"><span>Discipline</span><select name="role">
              <option>Screen actor</option><option>Commercial talent</option>
              <option>Stage &amp; theatre</option><option>Voice &amp; presenting</option><option>Other</option></select></label>
            <label class="field"><span>City</span><input type="text" name="city" placeholder="London"></label>
          </div>
          <label class="field"><span>Reel or resume link</span><input type="url" name="link" placeholder="https://vimeo.com/your-reel" required></label>
          <label class="field"><span>Anything we should know</span><textarea name="msg" placeholder="Recent credits, union status, what you're aiming for next…"></textarea></label>
          <button type="submit" class="btn btn-primary" style="width:100%">Send Your Reel</button>
          <p class="form-note">Opens your email app addressed to {EMAIL}.</p>
        </form>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Vanguard Placement Group. All rights reserved.</span>
      <span>Helping independent talent secure agency representation.</span>
    </div>
  </div>
</footer>

<!-- floating UI -->
<div class="sticky-cta">
  <a href="submit.html" class="btn btn-primary">Send Your Reel</a>
  <button class="btn btn-ghost" data-chat-open>Ask the desk</button>
</div>
<div class="toast-wrap" id="toastWrap"></div>
<a class="mail-fab" href="mailto:{EMAIL}" aria-label="Email Vanguard Placement Group">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 6 9 7 9-7"/></svg></a>
<button class="to-top" id="toTop" aria-label="Back to top">↑</button>

<button class="chat-fab" id="chatFab" aria-label="Open the review desk assistant">
  <span class="pulse-ring"></span><span class="chat-badge" id="chatBadge">1</span>
  <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M20 2H4a2 2 0 00-2 2v18l4-4h14a2 2 0 002-2V4a2 2 0 00-2-2z"/></svg>
</button>
<div class="chat-panel" id="chatPanel">
  <div class="chat-head">
    <span class="avatar">VPG</span>
    <div><b>Vanguard Review Desk</b><span>Instant answers · real people behind them</span></div>
    <button class="chat-close" id="chatClose" aria-label="Close chat">×</button>
  </div>
  <div class="chat-body" id="chatBody"></div>
  <div class="chat-quick">
    <button type="button" data-chat-quick="how does the shortlisting work">🎬 How it works</button>
    <button type="button" data-chat-quick="how much does it cost">💷 Cost?</button>
    <button type="button" data-chat-quick="how fast do you respond">⚡ How fast?</button>
    <button type="button" data-chat-quick="what should i send">📎 What to send</button>
    <button type="button" data-chat-quick="submit">🚀 Submit my reel</button>
  </div>
  <form class="chat-input" id="chatForm" autocomplete="off">
    <input type="text" id="chatText" placeholder="Ask the desk anything…" aria-label="Type your question">
    <button type="submit" aria-label="Send"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21 23 12 2.01 3 2 10l15 2-15 2z"/></svg></button>
  </form>
</div>

<div class="exit-pop" id="exitPop">
  <div class="ex-back"></div>
  <div class="ex-card">
    <button class="ex-close" aria-label="Close">×</button>
    <div class="gift">🎬</div>
    <h3>Before you go — the <em>Reel Teardown Checklist</em></h3>
    <p>The 12 things our desk checks before shortlisting anyone. The same list we use on every submission. Free, no strings.</p>
    <button class="btn btn-primary" id="exitGet" style="width:100%">Send me the checklist</button>
    <p class="ex-alt">Or email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</div>

<div class="lightbox" id="lightbox">
  <div class="lb-backdrop" id="lbBackdrop"></div>
  <div class="lb-card">
    <button class="lb-close" id="lbClose" aria-label="Close">×</button>
    <div class="lb-media"><img id="lbImg" src="" alt="">
      <div class="lb-badge"><div><b>Reel available on request</b><span>Full reels are released to verified desks and by email — one click below.</span></div></div>
    </div>
    <div class="lb-body">
      <span class="sec-label" id="lbChip">Reel</span>
      <h3 id="lbTitle">Showreel</h3>
      <p id="lbDesc"></p>
      <a class="btn btn-primary" id="lbLink" href="mailto:{EMAIL}">📨 Request the full reel</a>
    </div>
  </div>
</div>
<script src="main.js" defer></script>
</body>
</html>'''


def page(slug, title, desc, body, active=None):
    active = active or slug
    html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23003087'/%3E%3Ctext x='32' y='45' font-family='Georgia,serif' font-weight='700' font-size='34' fill='white' text-anchor='middle'%3EV%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,500;0,600;0,700;0,800;1,500;1,600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>if(window.tailwind)tailwind.config={{theme:{{extend:{{colors:{{vanguard:'#003087',vanguardLift:'#2b6cff'}}}}}}}};</script>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="reel-bg" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
{nav_html(active)}
{body}
{FOOTER}'''
    open(slug, "w").write(html)
    return slug


# ----------------------------------------------------------------- components
def talent_card(t, link=True, extra=False):
    tag = f'<span class="tc-tag {t["stat_class"]}">{t["status"]}</span>'
    href = f'talent-{t["slug"]}.html'
    cls = "talent-card reveal" + (" hidden-card" if extra else "")
    attr = ' data-extra' if extra else ''
    return f'''<article class="{cls}" data-filter-item="roster" data-cat="{t['cat']} {t['status'].lower().replace(' ','-')}"{attr}>
  {tag}
  <a href="{href}" class="tc-media" style="display:block">
    <img src="{UNS}{t['photo']}{Q}" alt="{t['name']} headshot" loading="lazy" onerror="this.src='https://picsum.photos/seed/vpg-{t['slug']}/700/875'">
  </a>
  <div class="tc-body">
    <h3><a href="{href}">{t['name']}</a></h3>
    <p class="tc-role">{t['disc']} · {t['city']}</p>
    <p style="margin-top:8px">{t['headline']}</p>
    <div class="tc-actions">
      <button class="tc-watch" data-reel data-img="{UNS}{t['photo']}{Q}" data-reel-title="{t['name']} — showreel" data-chip="{t['disc']}" data-desc="{t['reel']} · {t['city']}. {t['headline']}.">▶ Watch Reel</button>
      <a class="tc-watch" href="{href}" style="border-color:transparent;color:var(--blue-soft)">Full profile →</a>
    </div>
  </div>
</article>'''


def profile_page(t):
    credits = "".join(f"<li><b>{y}</b><span>{c}</span></li>" for y, c in t["credits"])
    gal = "".join(
        f'<img src="{UNS}{g}{Q}" alt="{t["name"]} still" loading="lazy" onerror="this.src=\'https://picsum.photos/seed/vpg-{t["slug"]}-{i}/400/400\'">'
        for i, g in enumerate(t["gallery"]))
    more = "".join(
        f'<a class="pill" href="talent-{o["slug"]}.html">{o["name"]} · {o["city"]}</a>'
        for o in TALENT if o["slug"] != t["slug"])
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → <a href="talent.html">Our Talent</a> → {t['name']}</p>
  </div>
</header>

<section style="padding:60px 0 90px">
  <div class="container pf-grid">
    <div class="reveal">
      <div class="pf-media">
        <img src="{UNS}{t['photo']}{Q}" alt="{t['name']} headshot" onerror="this.src='https://picsum.photos/seed/vpg-{t['slug']}/800/1000'">
        <button class="pf-play" data-reel data-img="{UNS}{t['photo']}{Q}" data-reel-title="{t['name']} — showreel" data-chip="{t['disc']}" data-desc="{t['reel']} · {t['city']}. {t['headline']}.">▶ Watch the reel</button>
      </div>
      <div class="pf-gallery">{gal}</div>
      <div class="pf-stats">
        <div><b>{t['desks']}</b><span>Desks submitted</span></div>
        <div><b>{t['callbacks']}</b><span>Callbacks</span></div>
        <div><b>{t['response']}</b><span>First reply</span></div>
      </div>
    </div>

    <div class="reveal" style="--d:.1s">
      <div class="pf-head">
        <span class="tc-tag {t['stat_class']}" style="position:static;display:inline-block;margin-bottom:16px">{t['status']}</span>
        <h1>{t['name']}</h1>
        <p class="pf-sub">{t['disc']} · {t['city']}</p>
      </div>
      <p style="font-size:1.15rem;font-weight:500;color:var(--muted);margin-bottom:26px">{t['headline']}. Shortlisted by the Vanguard review desk and currently working with partner agencies in {t['city']} and beyond.</p>

      <div class="desk-note">“{t['note']}”<span>— Vanguard Review Department</span></div>

      <h2 class="sec-title" style="font-size:1.6rem;margin-bottom:12px">Profile</h2>
      <table class="pf-table">
        <tr><td>Playing age</td><td>{t['age']}</td></tr>
        <tr><td>Height</td><td>{t['height']}</td></tr>
        <tr><td>Accents</td><td>{t['accents']}</td></tr>
        <tr><td>Languages</td><td>{t['langs']}</td></tr>
        <tr><td>Union status</td><td>{t['union']}</td></tr>
        <tr><td>Representation</td><td>{t['rep']}</td></tr>
        <tr><td>Reel length</td><td>{t['reel']}</td></tr>
        <tr><td>Training</td><td>{t['training']}</td></tr>
      </table>

      <h2 class="sec-title" style="font-size:1.6rem;margin-bottom:14px">Selected credits</h2>
      <ul class="pf-credits">{credits}</ul>

      <div class="cta-row">
        <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Talent%20enquiry%20%E2%80%94%20{t['name'].replace(' ', '%20')}">Request {t['first']} for a role</a>
        <a class="btn btn-ghost" href="submit.html">I want a profile like this</a>
      </div>
      <p style="font-size:13px;color:var(--muted-2);margin-top:14px">Representation enquiries go straight to the Review Department. Average reply: 48 hours.</p>
    </div>
  </div>
</section>

<section class="soft">
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">More talent</p><h2 class="sec-title">Others on the <em>books</em></h2></div>
    <div class="pill-row">{more}</div>
    <div style="text-align:center;margin-top:34px" class="reveal"><a href="talent.html" class="btn btn-ghost">See the full roster →</a></div>
  </div>
</section>

<section style="padding:0 0 100px">
  <div class="container"><div class="cta-card reveal">
    <h2>Your profile could be the <em>next one</em> on this list.</h2>
    <p>Only <b><span data-slots>3</span> shortlist slots</b> left this cycle. Send your reel and the desk starts reviewing within 48 hours.</p>
    <div class="cta-row-w"><a href="submit.html" class="btn btn-white">Send Your Reel</a>
      <button class="btn" style="border:2px solid rgba(255,255,255,.45);color:#fff" data-chat-open>Ask the desk a question</button></div>
    <p class="cta-mail">Or email <b>{EMAIL}</b></p>
  </div></div>
</section>'''
    return page(f'talent-{t["slug"]}.html', f'{t["name"]} — {t["disc"]}, {t["city"]} | Vanguard Placement Group',
                f'{t["name"]}, {t["disc"]} based in {t["city"]}. {t["headline"]}. Profile, credits and reel — shortlisted by Vanguard Placement Group.',
                body, active="talent.html")


# ----------------------------------------------------------------- pages
def build_home():
    cards = "".join(talent_card(t) for t in TALENT[:3])
    body = f'''
<header class="hero" id="top">
  <div class="hero-bg" aria-hidden="true">
    <img src="{UNS}1485846234645-a62644f84728?auto=format&fit=crop&w=1900&q=70" alt="" onerror="this.style.display='none'">
  </div>
  <div class="hero-overlay" aria-hidden="true"></div>
  <div class="hero-edge" aria-hidden="true">Vet · Shortlist · Submit · Sign</div>
  <div class="container hero-inner">
    <div class="eyebrow rise" style="--d:.1s"><span class="dot"></span> <span data-slots>3</span> shortlist slots left — intake closes Friday</div>
    <h1 class="hero-title" aria-label="Raw Talent In. Big Opportunities Out.">
      <span class="line"><span class="w" style="--wd:.2s">Raw</span>&nbsp;<span class="w" style="--wd:.3s">Talent</span>&nbsp;<span class="w" style="--wd:.4s">In.</span></span>
      <span class="line"><em class="w" style="--wd:.55s">Big&nbsp;Opportunities</em>&nbsp;<span class="w" style="--wd:.7s">Out.</span></span>
    </h1>
    <p class="hero-rot rise" style="--d:.85s" id="heroRot"
       data-phrases="Reels read by people who actually cast.|A straight line to the right desk.|No gatekeepers. No waiting list.|Independent talent, agency-ready.">
      <span id="rotTyped"></span><span class="cursor" aria-hidden="true"></span></p>
    <p class="sub rise" style="--d:.95s">Send your reel or resume. We shortlist it straight to the right desks.</p>
    <div class="cta-row rise" style="--d:1.05s">
      <a href="submit.html" class="btn btn-primary">Send Your Reel</a>
      <a href="shortlisted.html" class="btn btn-ghost">See who got shortlisted →</a>
    </div>
    <p class="hero-tag rise" style="--d:1.15s">Helping independents secure agency representation.</p>
  </div>
  <div class="hero-stats-bar">
    <div class="container hs-inner">
      <div class="stat"><b><span class="count" data-count="3200" data-comma="1">0</span><i>+</i></b><span>Talents vetted</span></div>
      <div class="stat"><b><span class="count" data-count="4.9" data-decimals="1">0</span><i>★</i></b><span>Shortlist success rate</span></div>
      <div class="stat"><b><span class="count" data-count="48">0</span><i>h</i></b><span>Average response</span></div>
      <div class="stat"><b><span class="count" data-count="2">0</span></b><span>Agency offers per shortlist</span></div>
    </div>
  </div>
</header>
<div class="perf" aria-hidden="true"></div>

<section class="logos-strip" style="padding:48px 0 30px">
  <div class="container"><p class="logos-title">Desks our shortlists land on</p></div>
  <div class="marquee"><div class="marquee-track" id="marqueeTrack">
    <span class="client-logo lg-serif">Harlow &amp; Vance</span><span class="client-logo lg-bold">NORTHGATE TALENT</span>
    <span class="client-logo lg-wide">MERIDIAN&nbsp;CASTING</span><span class="client-logo lg-serif">Rowe Artists</span>
    <span class="client-logo lg-mono">stage_nine</span><span class="client-logo lg-bold">KESTREL&nbsp;MGMT</span>
    <span class="client-logo lg-wide">ATLAS&nbsp;REP</span><span class="client-logo lg-serif">Linden Group</span>
  </div></div>
</section>

<!-- 10-second test hook -->
<section>
  <div class="container">
    <div class="magnet reveal">
      <div>
        <p class="sec-label">The 10-second test</p>
        <h3>Would your reel survive the first <em>ten seconds?</em></h3>
        <p>That's how long a casting desk gives it before the next tab. We watch the whole thing — then tell you exactly where most people lose them, and whether your opening scene is the right one.</p>
        <div class="cta-row">
          <a href="submit.html" class="btn btn-primary">Put my reel through the test</a>
          <button class="btn btn-ghost" data-chat-open>Ask the desk first</button>
        </div>
      </div>
      <div class="mg-side"><div class="mg-num">10s</div><p style="margin:0;font-weight:700">is all you get.<br>Make it the right 10.</p></div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">Our Talent</p>
      <h2 class="sec-title">The people on our <em>books</em></h2>
      <p class="sec-sub">Every one of them came to us independent — no agent, no manager, just footage and a reason to be seen. Click any profile to see the full file.</p></div>
    <div class="talent-grid">{cards}</div>
    <div style="text-align:center;margin-top:44px" class="reveal"><a href="talent.html" class="btn btn-ghost">See the full roster →</a></div>
  </div>
</section>

<section>
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">Why Vanguard</p><h2 class="sec-title">Why talent <em>comes back</em> to us</h2></div>
    <div class="why-grid">
      <div class="feature reveal"><div class="f-check">✓</div><h3>We spot the moment that books the role</h3><p>One scene usually does the work. We find it, flag it, and make sure it is the first thing a casting desk sees.</p></div>
      <div class="feature reveal" style="--d:.08s"><div class="f-check">✓</div><h3>We filter fast — no wasted time</h3><p>A straight yes or no, usually inside 48 hours. If your material is not ready, we tell you what is missing.</p></div>
      <div class="feature reveal" style="--d:.16s"><div class="f-check">✓</div><h3>You speak directly to the right desk</h3><p>No submission portal, no form that disappears. Your material goes to a named person who is casting or signing right now.</p></div>
      <div class="feature reveal" style="--d:.24s"><div class="f-check">✓</div><h3>Market-ready talent, not just reels</h3><p>Footage is half of it. We look at how you present, what you are right for today, and which room you belong in this season.</p></div>
    </div>
  </div>
</section>

<!-- locked teaser -->
<section class="soft">
  <div class="container" style="max-width:860px">
    <div class="sec-head center reveal"><p class="sec-label">This month</p><h2 class="sec-title">Who got <em>signed</em> this month</h2>
      <p class="sec-sub">Three names came off the shortlist with offers in the last 30 days.</p></div>
    <div class="locked reveal">
      <div class="blurred">
        <p style="font-size:1.3rem;font-weight:700;margin-bottom:10px">Diego S. — signed, three-year commercial agreement, Madrid desk</p>
        <p style="font-size:1.3rem;font-weight:700;margin-bottom:10px">Priya N. — signed, commercial and voice division, Dublin</p>
        <p style="font-size:1.3rem;font-weight:700">Liam K. — lead role confirmed, streaming drama, London</p>
      </div>
      <div class="lock-ui">
        <div><h3>🔒 Shortlist results are desk-only</h3>
          <p>Tap to reveal this month's signings — and see what their material had in common.</p>
          <button class="btn btn-primary" data-unlock>Reveal this month's signings</button></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">Testimonials</p><h2 class="sec-title">What clients <em>actually say</em></h2></div>
    <div class="t-grid">
      <div class="t-card reveal"><div class="t-stars">★★★★★</div><blockquote>“Vanguard spotted a quiet scene in my reel that got me the lead. Never had an agency do that before.”</blockquote><div class="t-who"><span class="t-avatar">AM</span><span><b>Alex M.</b><span>Actor · Toronto</span></span></div></div>
      <div class="t-card reveal" style="--d:.08s"><div class="t-stars">★★★★★</div><blockquote>“They shortlisted me to three desks in one week. The first one called me back same day.”</blockquote><div class="t-who"><span class="t-avatar">ZP</span><span><b>Zara P.</b><span>Actress · London</span></span></div></div>
      <div class="t-card reveal" style="--d:.16s"><div class="t-stars">★★★★★</div><blockquote>“This is the only vetting team that actually understands indie talent. My agent didn’t even get a look until Vanguard did.”</blockquote><div class="t-who"><span class="t-avatar">TH</span><span><b>Tyler H.</b><span>Actor · NYC</span></span></div></div>
      <div class="t-card reveal" style="--d:.24s"><div class="t-stars">★★★★★</div><blockquote>“Clean, fast, and they only put talent in front of the right people. Best bridge I’ve ever used.”</blockquote><div class="t-who"><span class="t-avatar">RS</span><span><b>Riley S.</b><span>Actor · Vancouver</span></span></div></div>
    </div>
    <div style="text-align:center;margin-top:44px" class="reveal"><a href="shortlisted.html" class="btn btn-primary">See the full shortlist</a></div>
  </div>
</section>

<section class="soft">
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">FAQ</p><h2 class="sec-title">Straight <em>answers</em></h2></div>
    <div class="faq-list">
      {faq_items(FAQ_HOME)}
    </div>
    <div style="text-align:center;margin-top:36px" class="reveal"><a href="faq.html" class="btn btn-ghost">All 12 questions →</a></div>
  </div>
</section>

<section style="padding:0 0 100px">
  <div class="container"><div class="cta-card reveal">
    <h2>Your reel is already sitting on a <em>hard drive.</em></h2>
    <p>Send it over. We watch all of it, tell you honestly what it's ready for, and put it in front of the desk most likely to say yes. <b><span data-slots>3</span> slots</b> left this cycle.</p>
    <div class="cta-row-w"><a href="submit.html" class="btn btn-white">Send Your Reel</a>
      <a href="how-it-works.html" class="btn" style="border:2px solid rgba(255,255,255,.45);color:#fff">See how it works</a></div>
    <p class="cta-mail">Questions first? <b>{EMAIL}</b></p>
  </div></div>
</section>'''
    return page("index.html", "Vanguard Placement Group — Raw Talent In. Big Opportunities Out.",
                "Send your reel or resume. We shortlist it straight to the right desks. Helping independent talent secure agency representation — 48h average response.",
                body)


FAQ_HOME = [
    ("How does the shortlisting work?",
     "You send a reel or a resume. Someone here watches all of it, works out what you are right for this season, and puts your material on the desk of an agent or casting director looking for exactly that. You hear back either way — including when the answer is no."),
    ("How fast do you vet?",
     "48 hours on average. Busy weeks it stretches to three days, and we will say so rather than leave you refreshing your inbox. Shortlists go out the same week we approve them."),
    ("What makes Vanguard different?",
     "Most submissions get ten seconds and a delete. We watch the whole thing, and we only send you somewhere when the desk is genuinely looking for what you do. Fewer submissions, better ones."),
    ("How do I get started?",
     "Use the submit page, or email your link straight to " + EMAIL + ". A link is fine — Vimeo, YouTube, Drive, whatever you already have."),
]

FAQ_FULL = FAQ_HOME + [
    ("How much does it cost?",
     "There is no fixed list. It depends on how much material you have, how many desks we are approaching and how quickly you need it moving. Tell us what you are after and you will have a number within 24 hours — and the number we quote is the number you pay."),
    ("Do you take union and non-union?",
     "Both. Plenty of the talent we shortlist is non-union and still gets signed. If a role or a desk is union-only we will tell you before we submit, not after."),
    ("What do I actually need to send?",
     "A link to a reel, self-tape or scene, a credit list or resume, and a current headshot. One line on what you are aiming for next helps us match the right desk. No reel yet? Send a self-tape — we have shortlisted people off a single scene."),
    ("Am I good enough to be shortlisted?",
     "About a third of submissions get shortlisted straight away. Some get notes and come back stronger. Some are not ready yet — and you will be told that in plain words rather than left waiting."),
    ("Do you lock me into anything?",
     "No exclusivity. Shortlisting through us does not stop you submitting yourself or signing elsewhere. If an agency signs you, the relationship is yours."),
    ("What happens to my material?",
     "It goes to desks only. Never posted publicly, never sold on, never used as marketing without written permission. Ask for an NDA and you will have one the same day."),
    ("How long should my reel be?",
     "One to three minutes, strongest scene first. A desk decides in the first twenty seconds whether to keep watching, so do not bury the moment that proves you can act."),
    ("I am just starting out — is it worth submitting?",
     "Yes. We have shortlisted people whose only footage was a student film and two self-tapes. What matters is whether the material shows something castable — and if it does not yet, we tell you what to shoot next."),
]


def faq_items(items):
    out = []
    for i, (q, a) in enumerate(items):
        out.append(f'''<div class="faq-item reveal" style="--d:.{i}s"><button class="faq-q">{q}<span class="faq-icon">+</span></button>
<div class="faq-a"><p>{a}</p></div></div>''')
    return "\n".join(out)


def build_talent():
    cards = "".join(talent_card(t) for t in TALENT)
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → Our Talent</p>
    <h1>Our <em>Talent</em></h1>
    <p class="lead">Screen, commercial, stage and voice. Every profile below was an independent submission first — click any face for the full file, credits and reel.</p>
    <div class="cta-row" style="margin-top:28px"><a href="submit.html" class="btn btn-primary">Add me to the roster</a>
      <a href="agencies.html" class="btn btn-ghost">I'm casting — request a shortlist</a></div>
  </div>
</header>

<section>
  <div class="container">
    <div class="filters" data-filter-group="roster">
      <button data-filter="all" class="active">All talent</button>
      <button data-filter="screen">Screen</button>
      <button data-filter="commercial">Commercial</button>
      <button data-filter="stage">Stage</button>
      <button data-filter="voice">Voice &amp; presenting</button>
    </div>
    <div class="talent-grid">{cards}</div>
    <div class="pill-row" style="margin-top:40px">
      <span class="pill">🎬 Profiles updated weekly</span>
      <span class="pill hot">🔥 <span data-slots>3</span> roster slots open</span>
      <span class="pill">⏱ 48h review</span>
    </div>
  </div>
</section>

<section class="soft">
  <div class="container"><div class="magnet reveal">
    <div><p class="sec-label">Roster intake</p><h3>Want your profile on this <em>page?</em></h3>
      <p>Roster profiles are built from material we have already reviewed. Send your reel, pass the review, and your file goes live with a direct request button on it.</p>
      <a href="submit.html" class="btn btn-primary">Start my profile</a></div>
    <div class="mg-side"><div class="mg-num">48h</div><p style="margin:0;font-weight:700">from submission<br>to a real answer.</p></div>
  </div></div>
</section>'''
    return page("talent.html", "Our Talent — Vanguard Placement Group",
                "Screen actors, commercial talent, stage and voice artists represented and shortlisted by Vanguard Placement Group. Full profiles, credits and reels.",
                body)


def build_shortlisted():
    cards = "".join(talent_card(t, extra=(i >= 4)) for i, t in enumerate(TALENT))
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → Shortlisted</p>
    <h1>Recent <em>shortlists</em></h1>
    <p class="lead">Where talent went after we put their material in front of the right desk. Names shortened at their request — click through for the full file.</p>
    <div class="pill-row" style="justify-content:flex-start;margin-top:26px">
      <span class="pill">📨 41 shortlists sent this quarter</span><span class="pill">✅ 2 average offers each</span><span class="pill hot">🔥 intake closes Friday</span>
    </div>
  </div>
</header>

<section>
  <div class="container">
    <div class="filters" data-filter-group="roster">
      <button data-filter="all" class="active">Everything</button>
      <button data-filter="booked">Booked</button>
      <button data-filter="in-negotiation">In negotiation</button>
      <button data-filter="signed">Signed</button>
    </div>
    <div class="talent-grid">{cards}</div>
    <div style="text-align:center;margin-top:44px" class="reveal">
      <a href="#" class="btn btn-ghost" data-more="See full shortlist →">See full shortlist →</a>
    </div>
  </div>
</section>

<section class="soft">
  <div class="container" style="max-width:860px">
    <div class="sec-head center reveal"><p class="sec-label">Pattern</p><h2 class="sec-title">What the booked ones <em>had in common</em></h2></div>
    <div class="steps">
      <div class="step reveal"><b>1</b><div><h3>A strong scene in the first 15 seconds</h3><p>Not a montage. Not titles. A moment where something actually changes on their face.</p></div></div>
      <div class="step reveal" style="--d:.08s"><b>2</b><div><h3>Under three minutes, every time</h3><p>Every reel that got a callback was shorter than the ones that did not.</p></div></div>
      <div class="step reveal" style="--d:.16s"><b>3</b><div><h3>A clear line on what they want next</h3><p>“Returning drama, supporting” beats “open to anything” on every single desk.</p></div></div>
    </div>
    <div style="text-align:center;margin-top:36px" class="reveal"><a href="submit.html" class="btn btn-primary">Put my reel in the next shortlist</a></div>
  </div>
</section>'''
    return page("shortlisted.html", "Shortlisted — Recent Placements | Vanguard Placement Group",
                "Recent Vanguard shortlists: booked, in negotiation and signed. See where independent talent went after the review desk put their material on the right desk.",
                body)


def build_submit():
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → Send Your Reel</p>
    <h1>Send your <em>reel</em></h1>
    <p class="lead">Four quick steps. A link is all we need. The review desk comes back within 48 hours — including if the answer is no.</p>
    <div class="pill-row" style="justify-content:flex-start;margin-top:24px">
      <span class="pill hot">🔥 <span data-slots>3</span> slots left this cycle</span>
      <span class="pill">⏱ Closes in <b id="cdClock2">—</b></span>
      <span class="pill">📨 No account, no upload</span>
    </div>
  </div>
</header>

<section>
  <div class="container grid-2" style="align-items:start">
    <div class="form-card reveal">
      <h4>Submission — review desk</h4>
      <p>Takes about 40 seconds.</p>
      <form id="msForm" novalidate>
        <div class="msf-bar"><i class="on"></i><i></i><i></i><i></i></div>

        <div class="msf-step on">
          <label class="field"><span>Your name</span><input type="text" name="name" placeholder="Alex Moore" required></label>
          <label class="field"><span>Email</span><input type="email" name="email" placeholder="you@email.com" required></label>
          <label class="field"><span>Phone (optional)</span><input type="tel" name="phone" placeholder="+44 …"></label>
          <div class="msf-nav"><button type="button" class="btn btn-primary" data-next style="width:100%">Next →</button></div>
        </div>

        <div class="msf-step">
          <label class="field"><span>Discipline</span><select name="role">
            <option>Screen actor</option><option>Commercial talent</option><option>Stage &amp; theatre</option>
            <option>Voice &amp; presenting</option><option>Other</option></select></label>
          <label class="field"><span>City</span><input type="text" name="city" placeholder="London" required></label>
          <label class="field"><span>Union status</span><select name="union">
            <option>Non-union</option><option>Equity</option><option>SAG-AFTRA</option><option>ACTRA</option><option>Other / applying</option></select></label>
          <div class="msf-nav"><button type="button" class="btn btn-ghost" data-prev>← Back</button><button type="button" class="btn btn-primary" data-next style="flex:1">Next →</button></div>
        </div>

        <div class="msf-step">
          <label class="field"><span>Reel or resume link</span><input type="url" name="link" placeholder="https://vimeo.com/your-reel" required></label>
          <label class="field"><span>Current representation</span><select name="rep">
            <option>None — independent</option><option>Agent, looking to move</option><option>Manager only</option><option>Prefer not to say</option></select></label>
          <div class="msf-nav"><button type="button" class="btn btn-ghost" data-prev>← Back</button><button type="button" class="btn btn-primary" data-next style="flex:1">Next →</button></div>
        </div>

        <div class="msf-step">
          <label class="field"><span>What are you aiming for next?</span><textarea name="msg" placeholder="Returning drama, supporting roles. Recent credits: …"></textarea></label>
          <div class="msf-nav"><button type="button" class="btn btn-ghost" data-prev>← Back</button><button type="submit" class="btn btn-primary" style="flex:1">📨 Send to the review desk</button></div>
          <p class="form-note" id="msDone">Opens your email app addressed to {EMAIL}.</p>
        </div>
      </form>
    </div>

    <div class="reveal" style="--d:.1s">
      <div class="sec-head"><p class="sec-label">What happens next</p><h2 class="sec-title" style="font-size:2.2rem">No black hole. <em>Ever.</em></h2></div>
      <div class="steps">
        <div class="step"><b>1</b><div><h3>Confirmation, same day</h3><p>You get an email saying the desk has it, with a rough review date.</p></div></div>
        <div class="step"><b>2</b><div><h3>Full review, 48 hours</h3><p>Someone watches all of it and writes notes. Not a filter, not a form.</p></div></div>
        <div class="step"><b>3</b><div><h3>Yes, or an honest no</h3><p>Shortlisted — we name the desks. Not yet — you get the reasons and what to shoot.</p></div></div>
      </div>
      <div class="desk-note" style="margin-top:24px">“We would rather send one reel to the right desk than twenty to the wrong ones. That is the whole business.”<span>— Vanguard Review Department</span></div>
      <button class="btn btn-ghost" data-chat-open style="width:100%">💬 Not sure what to send? Ask the desk</button>
    </div>
  </div>
</section>'''
    return page("submit.html", "Send Your Reel — Vanguard Placement Group",
                "Submit your reel or resume to the Vanguard review desk. Four steps, 48-hour response, honest notes either way.",
                body)


def build_how():
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → How It Works</p>
    <h1>How it <em>works</em></h1>
    <p class="lead">Four steps between a file on your laptop and a named person at an agency watching it. No portal, no algorithm, no silence.</p>
  </div>
</header>

<section>
  <div class="container" style="max-width:900px">
    <div class="steps">
      <div class="step reveal"><b>1</b><div><h3>You send material</h3><p>A reel, a self-tape, a scene, a resume — a link is enough. Messy is fine. We have shortlisted people off a single phone-shot scene with decent sound.</p></div></div>
      <div class="step reveal" style="--d:.08s"><b>2</b><div><h3>The desk watches everything</h3><p>All of it, not the first ten seconds. We note what you are castable for right now, which scene proves it, and what is missing if anything is.</p></div></div>
      <div class="step reveal" style="--d:.16s"><b>3</b><div><h3>We match you to live briefs</h3><p>Agency and casting desks tell us what they are building this season. Your material goes to the ones genuinely looking for what you do — by name, not by mass email.</p></div></div>
      <div class="step reveal" style="--d:.24s"><b>4</b><div><h3>You hear back either way</h3><p>Shortlisted: we tell you which desks and when. Not yet: you get the notes, free, and an open door to come back once you have shot what is missing.</p></div></div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">What a desk sees</p><h2 class="sec-title">The file we <em>send</em></h2>
      <p class="sec-sub">Every shortlist goes out in the same format. Clean, short, impossible to ignore.</p></div>
    <div class="grid-2">
      <div class="feature reveal"><div class="f-check">01</div><h3>One page, no padding</h3><p>Name, playing age, location, union status, the single line that says what you are right for.</p></div>
      <div class="feature reveal" style="--d:.08s"><div class="f-check">02</div><h3>Timecoded scene</h3><p>We tell the desk exactly where to start watching. Nobody scrubs for the good bit.</p></div>
      <div class="feature reveal" style="--d:.16s"><div class="f-check">03</div><h3>Why we are sending you</h3><p>Two sentences on why you fit the brief they gave us. Specific, not flattering.</p></div>
      <div class="feature reveal" style="--d:.24s"><div class="f-check">04</div><h3>A way to say yes fast</h3><p>Availability, contact, and a reply-to that reaches a person in minutes.</p></div>
    </div>
    <div style="text-align:center;margin-top:40px" class="reveal"><a href="submit.html" class="btn btn-primary">Start with step one →</a></div>
  </div>
</section>

<section>
  <div class="container" style="max-width:860px">
    <div class="sec-head center reveal"><p class="sec-label">FAQ</p><h2 class="sec-title">While you're <em>here</em></h2></div>
    <div class="faq-list">{faq_items(FAQ_HOME[:3])}</div>
  </div>
</section>'''
    return page("how-it-works.html", "How It Works — Vanguard Placement Group",
                "The Vanguard vetting pipeline: send material, full review in 48 hours, matched to live agency briefs, honest answer either way.",
                body)


def build_agencies():
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → For Agencies &amp; Casting</p>
    <h1>For agencies &amp; <em>casting</em></h1>
    <p class="lead">Tell us the brief. We come back with a pre-vetted shortlist — availability confirmed, material timecoded, no filler.</p>
    <div class="cta-row" style="margin-top:28px">
      <a href="mailto:{EMAIL}?subject=Shortlist%20request" class="btn btn-primary">Request a shortlist</a>
      <button class="btn btn-ghost" data-chat-open>Ask about coverage</button></div>
  </div>
</header>

<section>
  <div class="container">
    <div class="why-grid">
      <div class="feature reveal"><div class="f-check">✓</div><h3>Pre-vetted, not pre-filtered</h3><p>Every name on the list has been watched end to end by a person who can tell you why they are on it.</p></div>
      <div class="feature reveal" style="--d:.08s"><div class="f-check">✓</div><h3>Timecoded material</h3><p>You get the exact scene that answers your brief. No scrubbing through four minutes of montage.</p></div>
      <div class="feature reveal" style="--d:.16s"><div class="f-check">✓</div><h3>Availability confirmed first</h3><p>We check before we send. Nobody on your shortlist is already on location in another country.</p></div>
      <div class="feature reveal" style="--d:.24s"><div class="f-check">✓</div><h3>Fresh faces, properly sourced</h3><p>Independent talent you will not have seen on the same three directories as everyone else.</p></div>
      <div class="feature reveal" style="--d:.32s"><div class="f-check">✓</div><h3>Turnaround in days</h3><p>Standard briefs come back inside 72 hours. Urgent ones, same week — say so and we prioritise.</p></div>
      <div class="feature reveal" style="--d:.4s"><div class="f-check">✓</div><h3>Discreet by default</h3><p>Project details stay with the desk. NDA on request, signed the same day.</p></div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="container" style="max-width:820px">
    <div class="sec-head center reveal"><p class="sec-label">Brief us</p><h2 class="sec-title">What we need from <em>you</em></h2></div>
    <div class="steps">
      <div class="step reveal"><b>1</b><div><h3>The role and the tone</h3><p>Playing age, register, how much screen time, what the character has to carry.</p></div></div>
      <div class="step reveal" style="--d:.08s"><b>2</b><div><h3>Territory and union requirement</h3><p>Where it shoots, who can legally work on it, whether local-hire matters.</p></div></div>
      <div class="step reveal" style="--d:.16s"><b>3</b><div><h3>Your deadline</h3><p>Real one, not the padded one. We will tell you straight if it is not possible.</p></div></div>
    </div>
    <div style="text-align:center;margin-top:36px" class="reveal">
      <a href="mailto:{EMAIL}?subject=Shortlist%20request%20%E2%80%94%20brief" class="btn btn-primary">Send us a brief</a></div>
  </div>
</section>'''
    return page("agencies.html", "For Agencies & Casting — Vanguard Placement Group",
                "Request a pre-vetted shortlist from Vanguard Placement Group. Timecoded material, confirmed availability, turnaround in days.",
                body)


def build_stories():
    rows = [
        (TALENT[0], "AM", "“Vanguard spotted a quiet scene in my reel that got me the lead. Never had an agency do that before.”",
         "Three years of self-tapes, no agent, and a reel that opened on a fight scene. The desk moved a two-line hospital scene to the front — the one where he says almost nothing — and the first agency that watched it asked to meet him that week."),
        (TALENT[1], "ZP", "“They shortlisted me to three desks in one week. The first one called me back same day.”",
         "She had been submitting to open calls for eighteen months. We cut the reel to ninety seconds, wrote one line about what she wanted next, and sent it to three desks building returning dramas. Two replied inside 24 hours."),
        (TALENT[4], "TH", "“This is the only vetting team that actually understands indie talent. My agent didn’t even get a look until Vanguard did.”",
         "Twelve years of stage work, a reel ordered like a theatre programme. We led with the interrogation scene instead of the Shakespeare, and a cable drama tested him for a series regular inside a month."),
        (TALENT[5], "RS", "“Clean, fast, and they only put talent in front of the right people. Best bridge I’ve ever used.”",
         "A sixty-second voice sample with three clean reads and written range notes. It beat every ten-minute demo in the pile that month and the commercial division signed her."),
    ]
    cards = ""
    for t, ini, quote, story in rows:
        cards += f'''<article class="story reveal">
  <img src="{UNS}{t['photo']}{Q}" alt="{t['name']}" loading="lazy" onerror="this.src='https://picsum.photos/seed/vpg-s-{t['slug']}/700/520'">
  <div><div class="t-stars">★★★★★</div>
    <h3>{t['headline']}</h3>
    <blockquote style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:600;margin-bottom:14px">{quote}</blockquote>
    <p>{story}</p>
    <div class="cta-row"><a href="talent-{t['slug']}.html" class="btn btn-ghost btn-sm">See the full profile →</a></div>
  </div></article>'''
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → Testimonials</p>
    <h1>What clients <em>actually say</em></h1>
    <p class="lead">Four shortlists, four outcomes — and what actually changed between the version that got ignored and the version that got a callback.</p>
  </div>
</header>

<section><div class="container">{cards}</div></section>

<section class="soft">
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">In their words</p><h2 class="sec-title">More from the <em>roster</em></h2></div>
    <div class="t-grid">
      <div class="t-card reveal"><div class="t-stars">★★★★★</div><blockquote>“They told me my reel was not ready and exactly what to shoot. Six weeks later they shortlisted me. That honesty is rare.”</blockquote><div class="t-who"><span class="t-avatar">MK</span><span><b>Marcus K.</b><span>Actor · Birmingham</span></span></div></div>
      <div class="t-card reveal" style="--d:.08s"><div class="t-stars">★★★★★</div><blockquote>“I had been emailing agencies for two years with nothing back. One shortlist and I had two meetings.”</blockquote><div class="t-who"><span class="t-avatar">EL</span><span><b>Elena L.</b><span>Actress · Dublin</span></span></div></div>
      <div class="t-card reveal" style="--d:.16s"><div class="t-stars">★★★★★</div><blockquote>“Fast, specific, no flattery. They treat your career like it is a real thing, not a hobby.”</blockquote><div class="t-who"><span class="t-avatar">DO</span><span><b>Daniel O.</b><span>Voice artist · Manchester</span></span></div></div>
    </div>
    <div style="text-align:center;margin-top:44px" class="reveal"><a href="submit.html" class="btn btn-primary">Send Your Reel</a></div>
  </div>
</section>'''
    return page("success-stories.html", "Success Stories & Testimonials — Vanguard Placement Group",
                "Real outcomes from Vanguard shortlists: leads booked, agencies signed, callbacks inside 24 hours. What changed between the ignored reel and the one that worked.",
                body, active="success-stories.html")


def build_about():
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → About</p>
    <h1>The <em>Review Department</em></h1>
    <p class="lead">Vanguard Placement Group exists for one reason: independent talent with good material keeps getting lost in piles nobody finishes watching.</p>
  </div>
</header>

<section>
  <div class="container grid-2" style="align-items:center;gap:50px">
    <div class="reveal">
      <img src="{UNS}1521119989659-a83eee488004{Q}" alt="The review desk" style="border-radius:22px;border:2px solid var(--line)" onerror="this.src='https://picsum.photos/seed/vpg-about/900/700'">
    </div>
    <div class="reveal" style="--d:.1s">
      <p class="sec-label">Who we are</p>
      <h2 class="sec-title" style="font-size:2.4rem">A desk, not a <em>directory</em></h2>
      <p style="color:var(--muted);font-weight:450;margin-bottom:16px">We are a small talent acquisitions team. People bring us reels and resumes, we watch everything properly, and the material that is ready goes to agents and casting directors we actually speak to.</p>
      <p style="color:var(--muted);font-weight:450;margin-bottom:16px">There is no directory to pay into and no profile that sits there collecting dust. A shortlist is a real email, to a real person, with your scene timecoded in it.</p>
      <p style="color:var(--muted);font-weight:450">When someone is not ready, we say that too — with the reasons. It is the part of the job people thank us for most.</p>
      <div class="cta-row" style="margin-top:24px"><a href="submit.html" class="btn btn-primary">Send your reel</a><a href="how-it-works.html" class="btn btn-ghost">How it works</a></div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="container">
    <div class="sec-head center reveal"><p class="sec-label">Standards</p><h2 class="sec-title">What we <em>will not</em> do</h2></div>
    <div class="why-grid">
      <div class="feature reveal"><div class="f-check">✕</div><h3>Mass-submit you</h3><p>Blasting fifty desks burns your name. We send to the ones that briefed us for what you do.</p></div>
      <div class="feature reveal" style="--d:.08s"><div class="f-check">✕</div><h3>Promise representation</h3><p>Nobody can. We promise the review, the honesty and the submission — the signature is the agency's call.</p></div>
      <div class="feature reveal" style="--d:.16s"><div class="f-check">✕</div><h3>Sit on your material</h3><p>48 hours, then you know. No limbo, no chasing, no polite silence.</p></div>
      <div class="feature reveal" style="--d:.24s"><div class="f-check">✕</div><h3>Share anything publicly</h3><p>Your reel goes to desks only. NDA on request, same day.</p></div>
    </div>
    <div class="hs-inner" style="margin-top:50px;border:2px solid var(--line);border-radius:20px;overflow:hidden">
      <div class="stat"><b><span class="count" data-count="3200" data-comma="1">0</span><i>+</i></b><span>Talents vetted</span></div>
      <div class="stat"><b><span class="count" data-count="41">0</span></b><span>Shortlists this quarter</span></div>
      <div class="stat"><b><span class="count" data-count="48">0</span><i>h</i></b><span>Average response</span></div>
      <div class="stat"><b><span class="count" data-count="9">0</span></b><span>Territories covered</span></div>
    </div>
  </div>
</section>

<section style="padding:0 0 100px">
  <div class="container"><div class="cta-card reveal">
    <h2>Send it. <em>Worst case</em>, you get honest notes.</h2>
    <p>Best case, your material is on an agency desk by Friday. <b><span data-slots>3</span> slots</b> left in this review cycle.</p>
    <div class="cta-row-w"><a href="submit.html" class="btn btn-white">Send Your Reel</a>
      <a href="contact.html" class="btn" style="border:2px solid rgba(255,255,255,.45);color:#fff">Talk to the desk</a></div>
    <p class="cta-mail">Or email <b>{EMAIL}</b></p>
  </div></div>
</section>'''
    return page("about.html", "About the Review Department — Vanguard Placement Group",
                "Vanguard Placement Group is a talent acquisitions desk helping independent talent secure agency representation. Who reviews, what we will not do, and our standards.",
                body)


def build_faq():
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → FAQ</p>
    <h1>Straight <em>answers</em></h1>
    <p class="lead">Twelve questions we get before anyone sends anything over. If yours is not here, the chat assistant answers in seconds.</p>
    <div class="cta-row" style="margin-top:26px"><button class="btn btn-primary" data-chat-open>💬 Ask the desk</button>
      <a href="submit.html" class="btn btn-ghost">Skip ahead — send my reel</a></div>
  </div>
</header>

<section><div class="container"><div class="faq-list">{faq_items(FAQ_FULL)}</div></div></section>

<section class="soft">
  <div class="container"><div class="magnet reveal">
    <div><p class="sec-label">Free</p><h3>The <em>Reel Teardown Checklist</em></h3>
      <p>The 12 things our desk checks before shortlisting anyone — the same list, in the same order. Run your reel through it before you send.</p>
      <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Send%20me%20the%20Reel%20Teardown%20Checklist">Email me the checklist</a></div>
    <div class="mg-side"><div class="mg-num">12</div><p style="margin:0;font-weight:700">checks.<br>Two minutes.</p></div>
  </div></div>
</section>'''
    return page("faq.html", "FAQ — Vanguard Placement Group",
                "How shortlisting works, how fast we vet, what to send, union status, cost and confidentiality — answered straight by the Vanguard review desk.",
                body)


def build_contact():
    body = f'''
<header class="page-hero">
  <div class="container">
    <p class="crumb"><a href="index.html">Home</a> → Contact</p>
    <h1>Talk to the <em>desk</em></h1>
    <p class="lead">One inbox, real people, 48-hour average reply. Talent, agencies and press all land in the same place.</p>
  </div>
</header>

<section>
  <div class="container grid-2" style="align-items:start">
    <div class="reveal">
      <div class="steps">
        <div class="step"><b>✉</b><div><h3>Email</h3><p><a href="mailto:{EMAIL}" style="color:var(--blue-soft);font-weight:700">{EMAIL}</a><br>Talent submissions, agency briefs, everything else.</p></div></div>
        <div class="step"><b>⏱</b><div><h3>Response time</h3><p>48 hours average. Three days in a heavy intake week — and we will say so.</p></div></div>
        <div class="step"><b>💬</b><div><h3>Instant answers</h3><p>The chat assistant handles the common questions right now, day or night. <button class="tc-watch" data-chat-open style="margin-top:8px">Open the chat</button></p></div></div>
        <div class="step"><b>🔒</b><div><h3>Confidentiality</h3><p>Material goes to desks only. NDA on request, signed the same day.</p></div></div>
      </div>
    </div>
    <div class="form-card reveal" style="--d:.1s">
      <h4>Send a message</h4>
      <p>Submitting a reel? The <a href="submit.html" style="color:var(--blue-soft);font-weight:700">submission form</a> is faster.</p>
      <form class="simple-form" novalidate>
        <div class="f-row">
          <label class="field"><span>Your name</span><input type="text" name="name" placeholder="Alex Moore" required></label>
          <label class="field"><span>Email</span><input type="email" name="email" placeholder="you@email.com" required></label>
        </div>
        <div class="f-row">
          <label class="field"><span>You are</span><select name="role">
            <option>Talent — submitting</option><option>Agency / casting desk</option><option>Press</option><option>Other</option></select></label>
          <label class="field"><span>City</span><input type="text" name="city" placeholder="London"></label>
        </div>
        <label class="field"><span>Link (reel, site, brief)</span><input type="url" name="link" placeholder="https://" required></label>
        <label class="field"><span>Message</span><textarea name="msg" placeholder="What do you need?"></textarea></label>
        <button type="submit" class="btn btn-primary" style="width:100%">Send message</button>
        <p class="form-note">Opens your email app addressed to {EMAIL}.</p>
      </form>
    </div>
  </div>
</section>'''
    return page("contact.html", "Contact — Vanguard Placement Group",
                f"Contact the Vanguard Placement Group review desk: {EMAIL}. Talent submissions, agency briefs and press, 48-hour average reply.",
                body)


def build_404():
    body = '''
<header class="page-hero" style="padding:220px 0 120px;text-align:center">
  <div class="container">
    <p class="sec-label" style="justify-content:center">404</p>
    <h1>That page is off the <em>shortlist</em>.</h1>
    <p class="lead" style="margin:0 auto">The link is broken or the page moved. The talent is still here though.</p>
    <div class="cta-row" style="justify-content:center;margin-top:30px">
      <a href="index.html" class="btn btn-primary">Back to home</a>
      <a href="talent.html" class="btn btn-ghost">See the roster</a></div>
  </div>
</header>'''
    return page("404.html", "Page not found — Vanguard Placement Group", "That page could not be found.", body)


# ----------------------------------------------------------------- run
if __name__ == "__main__":
    built = [build_home(), build_talent(), build_shortlisted(), build_submit(), build_how(),
             build_agencies(), build_stories(), build_about(), build_faq(), build_contact(), build_404()]
    built += [profile_page(t) for t in TALENT]

    pages = [p for p in built if p != "404.html"]
    urls = "".join(f"  <url><loc>https://vanguardplacementgroup.com/{p}</loc></url>\n" for p in pages)
    open("sitemap.xml", "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open("robots.txt", "w").write("User-agent: *\nAllow: /\nSitemap: https://vanguardplacementgroup.com/sitemap.xml\n")

    print(f"built {len(built)} pages:")
    for p in built:
        print("  ", p, os.path.getsize(p), "bytes")
