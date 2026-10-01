VANGUARD PLACEMENT GROUP — complete website package
====================================================
Raw Talent In. Big Opportunities Out.
Contact: vanguardplacementgroup@gmail.com


WHAT'S IN HERE
--------------

ROOT FOLDER  → the full multi-page website, deploy-ready.
   index.html            Home
   talent.html           Our Talent (filterable roster)
   shortlisted.html      Recent shortlists (Booked / In negotiation / Signed)
   submit.html           Send Your Reel — 4-step form
   how-it-works.html     The vetting pipeline
   agencies.html         For Agencies & Casting
   success-stories.html  Testimonials / long-form wins
   about.html            The Review Department
   faq.html              12 questions
   contact.html          Contact the desk
   404.html              Not-found page
   talent-liam-k.html    \
   talent-amara-o.html    |
   talent-diego-s.html    |  6 full talent profile pages
   talent-noor-h.html     |  (opened by clicking any headshot)
   talent-jonah-r.html    |
   talent-priya-n.html   /
   styles.css            All styling
   main.js               Chatbot, router-free nav, countdown, toasts, forms
   sitemap.xml, robots.txt, _headers, _redirects

single-file/  → THE SAME SITE AS ONE FILE.
   index.html  (identical copy, named for hosting)
   vanguard-placement-group.html
   All 17 pages inlined with hash routing (#/talent, #/submit …).
   No CSS or JS files needed. Double-click to open — it just works.

source/  → how it was built, for future edits.
   build.py         regenerates all 17 pages      (python3 build.py)
   pack_single.py   re-packs them into one file   (python3 pack_single.py)
   wrangler.toml    Cloudflare Workers config

DEPLOY.md  → step-by-step Cloudflare instructions + why a deploy fails.


DEPLOY IN 60 SECONDS (Cloudflare Pages)
---------------------------------------
EASIEST:  upload single-file/index.html on its own. One file, whole site.

FULL SITE: Cloudflare dashboard → Workers & Pages → Create → Pages →
   Upload assets → drag the LOOSE FILES from this folder's root
   (not the folder itself — Cloudflare needs index.html at the top level).
   Framework preset: None.  Build command: EMPTY.  Output directory: /

You can delete the single-file/ and source/ folders before uploading.


EDITING
-------
Change text in source/build.py, then:
   python3 build.py          → rebuilds all 17 pages
   python3 pack_single.py    → rebuilds the single-file version


SETTINGS YOU CAN CHANGE IN ONE LINE
-----------------------------------
Top of main.js (and inside the single-file version):

   EMAIL: 'vanguardplacementgroup@gmail.com'
   SLOTS_LEFT: 3          number shown in the urgency bar and badges
   SHOW_TOASTS: true      the "just shortlisted" pop-ups — SIMULATED, set false to remove
   SHOW_URGENCY: true     sticky countdown bar at the top
   SHOW_EXIT_POP: true    exit-intent checklist popup
   DEADLINE_DAY: 5        countdown target (5 = Friday, 23:59)


PLACEHOLDER DATA — REPLACE BEFORE LAUNCH
----------------------------------------
These are invented and should be swapped for real information:
 - All 6 talent names, photos, credits and results
   (Liam K., Amara O., Diego S., Noor H., Jonah R., Priya N.)
 - The testimonials (Alex M., Zara P., Tyler H., Riley S. and the three extras)
 - Statistics: 3,200+ vetted, 4.9 rating, 48h response, 41 shortlists, 9 territories
 - Agency/desk names in the scrolling strip (Harlow & Vance, Northgate Talent …)
 - The "3 slots left" counter and the Friday countdown
 - The activity toasts in the bottom-left corner are simulated

Photos come from Unsplash and Picsum at runtime; fonts from Google Fonts.
An internet connection is needed for images and fonts to appear.
