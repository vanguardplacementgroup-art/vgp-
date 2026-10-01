/* ============================================================
   VANGUARD PLACEMENT GROUP — shared site script
   Config at the top: flip any of these off in one line.
   ============================================================ */
const VPG = {
  EMAIL: 'vanguardplacementgroup@gmail.com',
  SLOTS_LEFT: 3,              // shortlist slots shown in the urgency bar / badges
  SHOW_TOASTS: true,          // simulated "just shortlisted" activity toasts — set false to remove
  SHOW_URGENCY: true,         // sticky countdown bar at the top
  SHOW_EXIT_POP: true,        // exit-intent checklist popup
  DEADLINE_DAY: 5             // 5 = Friday — countdown targets this weekday, 23:59
};

/* ---------- helpers ---------- */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const mailto = (subject, body) =>
  `mailto:${VPG.EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

/* ---------- slot counters everywhere ---------- */
$$('[data-slots]').forEach(el => el.textContent = VPG.SLOTS_LEFT);

/* ---------- urgency bar + countdown ---------- */
(function urgency() {
  const bar = $('#urgency');
  if (bar && (!VPG.SHOW_URGENCY || sessionStorage.getItem('vpg-urgency') === 'off')) {
    bar.classList.add('hide'); $('#nav')?.classList.add('no-urgency');
  }
  const clocks = [$('#cdClock'), $('#cdClock2')].filter(Boolean);
  if (!clocks.length) return;
  const target = () => {
    const d = new Date();
    let diff = (VPG.DEADLINE_DAY - d.getDay() + 7) % 7;
    const t = new Date(d); t.setDate(d.getDate() + diff); t.setHours(23, 59, 0, 0);
    if (t <= d) t.setDate(t.getDate() + 7);
    return t;
  };
  let end = target();
  setInterval(() => {
    let s = Math.max(0, Math.floor((end - new Date()) / 1000));
    if (s === 0) end = target();
    const dd = Math.floor(s / 86400), hh = Math.floor(s % 86400 / 3600), mm = Math.floor(s % 3600 / 60), ss = s % 60;
    const txt = `${dd}d ${String(hh).padStart(2,'0')}h ${String(mm).padStart(2,'0')}m ${String(ss).padStart(2,'0')}s`;
    clocks.forEach(c => c.textContent = txt);
  }, 1000);
  $('#urgencyClose')?.addEventListener('click', () => {
    bar.classList.add('hide'); $('#nav')?.classList.add('no-urgency');
    sessionStorage.setItem('vpg-urgency', 'off');
  });
})();

/* ---------- nav ---------- */
const nav = $('#nav'), toTop = $('#toTop');
addEventListener('scroll', () => {
  nav?.classList.toggle('scrolled', scrollY > 30);
  toTop?.classList.toggle('show', scrollY > 600);
}, { passive: true });
toTop?.addEventListener('click', () => scrollTo({ top: 0, behavior: 'smooth' }));

const menuBtn = $('#menuBtn'), mobileMenu = $('#mobileMenu');
menuBtn?.addEventListener('click', () => mobileMenu.classList.toggle('open'));
$$('#mobileMenu a').forEach(a => a.addEventListener('click', () => mobileMenu.classList.remove('open')));

$('#themeBtn')?.addEventListener('click', () => {
  const el = document.documentElement;
  el.dataset.theme = el.dataset.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('vpg-theme', el.dataset.theme);
});
if (localStorage.getItem('vpg-theme')) document.documentElement.dataset.theme = localStorage.getItem('vpg-theme');

$$('#year').forEach(e => e.textContent = new Date().getFullYear());

/* ---------- hero typed rotator ---------- */
(function typed() {
  const el = $('#heroRot'); if (!el) return;
  const out = $('#rotTyped'), phrases = el.dataset.phrases.split('|');
  let p = 0, i = 0, del = false;
  (function tick() {
    const t = phrases[p];
    out.textContent = del ? t.slice(0, --i) : t.slice(0, ++i);
    let wait = del ? 26 : 45;
    if (!del && i === t.length) { wait = 1900; del = true; }
    else if (del && i === 0) { del = false; p = (p + 1) % phrases.length; wait = 300; }
    setTimeout(tick, wait);
  })();
})();

/* ---------- reveal + counters ---------- */
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { threshold: .12, rootMargin: '0px 0px -60px' });
$$('.reveal').forEach(el => io.observe(el));

const cio = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return;
  const el = e.target, target = parseFloat(el.dataset.count), dec = +(el.dataset.decimals || 0), comma = el.dataset.comma;
  let start = null;
  const step = ts => {
    if (!start) start = ts;
    const k = Math.min((ts - start) / 1400, 1), v = target * (1 - Math.pow(1 - k, 3));
    el.textContent = comma ? Math.round(v).toLocaleString() : v.toFixed(dec);
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step); cio.unobserve(el);
}), { threshold: .5 });
$$('.count').forEach(el => cio.observe(el));

/* ---------- marquee duplication ---------- */
const mt = $('#marqueeTrack'); if (mt) mt.innerHTML += mt.innerHTML;

/* ---------- FAQ accordion ---------- */
$$('.faq-item').forEach(item => {
  const q = item.querySelector('.faq-q'), a = item.querySelector('.faq-a');
  q.addEventListener('click', () => {
    const open = item.classList.contains('open');
    $$('.faq-item.open').forEach(o => { o.classList.remove('open'); o.querySelector('.faq-a').style.maxHeight = null; });
    if (!open) { item.classList.add('open'); a.style.maxHeight = a.scrollHeight + 'px'; }
  });
});

/* ---------- filters ---------- */
$$('[data-filter-group]').forEach(group => {
  const targets = $$(`[data-filter-item="${group.dataset.filterGroup}"]`);
  group.addEventListener('click', e => {
    const b = e.target.closest('button[data-filter]'); if (!b) return;
    $$('button', group).forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    const f = b.dataset.filter;
    targets.forEach(t => t.classList.toggle('is-hidden', f !== 'all' && !t.dataset.cat.split(' ').includes(f)));
  });
});

/* ---------- show more grids ---------- */
$$('[data-more]').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    const extras = $$('[data-extra]');
    const showing = extras[0]?.classList.contains('show');
    extras.forEach(x => { x.classList.toggle('show', !showing); x.classList.add('in'); });
    btn.textContent = showing ? btn.dataset.more : 'Show fewer ←';
  });
});

/* ---------- locked teaser ---------- */
$$('[data-unlock]').forEach(b => b.addEventListener('click', () => {
  const box = b.closest('.locked');
  box.querySelector('.lock-ui').remove();
  box.querySelector('.blurred').style.filter = 'none';
  box.style.borderStyle = 'solid';
}));

/* ---------- reel lightbox ---------- */
const lb = $('#lightbox');
function openLB(d) {
  if (!lb) return;
  $('#lbImg').src = d.img || '';
  $('#lbTitle').textContent = d.title || 'Showreel';
  $('#lbDesc').textContent = d.desc || '';
  $('#lbChip').textContent = d.chip || 'Reel';
  $('#lbLink').href = mailto(`Reel request — ${d.title || ''}`, `Hi Vanguard,\n\nPlease send me the full reel for ${d.title || ''}.\n\nThanks,`);
  lb.classList.add('on'); document.body.style.overflow = 'hidden';
}
function closeLB() { lb?.classList.remove('on'); document.body.style.overflow = ''; }
$$('[data-reel]').forEach(b => b.addEventListener('click', () => openLB({
  img: b.dataset.img, title: b.dataset.reelTitle, chip: b.dataset.chip, desc: b.dataset.desc
})));
$('#lbClose')?.addEventListener('click', closeLB);
$('#lbBackdrop')?.addEventListener('click', closeLB);
addEventListener('keydown', e => { if (e.key === 'Escape') { closeLB(); $('#exitPop')?.classList.remove('on'); } });

/* ---------- activity toasts ---------- */
(function toasts() {
  if (!VPG.SHOW_TOASTS) return;
  const wrap = $('#toastWrap'); if (!wrap) return;
  const items = [
    ['Reel approved — London', 'Screen actor shortlisted to 2 desks'],
    ['New submission — Dublin', 'Commercial talent, review started'],
    ['Callback logged — Toronto', 'Desk responded in under 24h'],
    ['Shortlist sent — Manchester', 'Material now with a casting desk'],
    ['Signed — Madrid', 'Three-year representation agreed']
  ];
  let n = 0;
  const pop = () => {
    const [a, b] = items[n++ % items.length];
    const el = document.createElement('div');
    el.className = 'toast';
    el.innerHTML = `<span class="tdot"></span><span><b>${a}</b><span>${b}</span></span>`;
    wrap.appendChild(el);
    setTimeout(() => { el.classList.add('out'); setTimeout(() => el.remove(), 400); }, 6000);
  };
  setTimeout(pop, 9000);
  setInterval(pop, 34000);
})();

/* ---------- exit-intent popup ---------- */
(function exitPop() {
  if (!VPG.SHOW_EXIT_POP) return;
  const pop = $('#exitPop'); if (!pop || sessionStorage.getItem('vpg-exit')) return;
  const show = () => {
    if (sessionStorage.getItem('vpg-exit')) return;
    pop.classList.add('on'); sessionStorage.setItem('vpg-exit', '1');
  };
  addEventListener('mouseout', e => { if (!e.relatedTarget && e.clientY < 10) show(); });
  setTimeout(show, 75000);
  $('.ex-close', pop)?.addEventListener('click', () => pop.classList.remove('on'));
  $('.ex-back', pop)?.addEventListener('click', () => pop.classList.remove('on'));
  $('#exitGet')?.addEventListener('click', () => {
    location.href = mailto('Send me the Reel Teardown Checklist',
      'Hi Vanguard,\n\nPlease send me the free Reel Teardown Checklist.\n\nName:\nDiscipline:\nCity:\n\nThanks,');
  });
})();

/* ---------- multi-step submit form ---------- */
(function msf() {
  const form = $('#msForm'); if (!form) return;
  const steps = $$('.msf-step', form), bars = $$('.msf-bar i', form);
  let s = 0;
  const paint = () => {
    steps.forEach((el, i) => el.classList.toggle('on', i === s));
    bars.forEach((b, i) => b.classList.toggle('on', i <= s));
  };
  $$('[data-next]', form).forEach(b => b.addEventListener('click', () => {
    const cur = steps[s], need = $$('[required]', cur).filter(i => !i.value.trim());
    if (need.length) { need[0].focus(); need[0].style.borderColor = '#e8112d'; return; }
    s = Math.min(s + 1, steps.length - 1); paint();
  }));
  $$('[data-prev]', form).forEach(b => b.addEventListener('click', () => { s = Math.max(s - 1, 0); paint(); }));
  form.addEventListener('submit', e => {
    e.preventDefault();
    const g = n => (form[n]?.value || '').trim();
    const body = `Name: ${g('name')}\nEmail: ${g('email')}\nPhone: ${g('phone')}\nDiscipline: ${g('role')}\nCity: ${g('city')}\n` +
      `Union status: ${g('union')}\nRepresentation: ${g('rep')}\nReel / resume: ${g('link')}\n\nNotes:\n${g('msg')}`;
    location.href = mailto(`Reel submission — ${g('name')}`, body);
    $('#msDone').textContent = 'Opening your email app — hit send and the review desk has it.';
  });
  paint();
})();

/* ---------- simple footer form ---------- */
$$('.simple-form').forEach(form => form.addEventListener('submit', e => {
  e.preventDefault();
  const g = n => (form[n]?.value || '').trim();
  if (!g('name') || !g('email') || !g('link')) {
    form.querySelector('.form-note').textContent = 'Name, email and a reel link, please.';
    return;
  }
  location.href = mailto(`Reel submission — ${g('name')}`,
    `Name: ${g('name')}\nEmail: ${g('email')}\nDiscipline: ${g('role')}\nCity: ${g('city')}\nReel / resume: ${g('link')}\n\n${g('msg')}`);
  form.querySelector('.form-note').textContent = 'Opening your email app — hit send and we reply within 48 hours.';
}));

/* ============================================================
   CHATBOT — free text + quick chips + guided submission flow
   ============================================================ */
(function chatbot() {
  const fab = $('#chatFab'), panel = $('#chatPanel'), body = $('#chatBody'),
        form = $('#chatForm'), input = $('#chatText');
  if (!fab || !panel) return;

  const E = VPG.EMAIL, S = VPG.SLOTS_LEFT;
  let started = false, flow = null, data = {};

  const say = (html, who = 'bot') => {
    const d = document.createElement('div');
    d.className = 'msg ' + who; d.innerHTML = html;
    body.appendChild(d); body.scrollTop = body.scrollHeight;
  };
  const typing = () => {
    const d = document.createElement('div');
    d.className = 'msg bot typing'; d.innerHTML = '<i></i><i></i><i></i>';
    body.appendChild(d); body.scrollTop = body.scrollHeight; return d;
  };
  const botSay = (html, delay = 600) => {
    const t = typing();
    setTimeout(() => { t.remove(); say(html); }, delay);
  };

  /* ---- knowledge base: [keywords, answer] ---- */
  const INTENTS = [
    [['hi','hello','hey','good morning','good evening','yo','hiya'],
     `Hi — you're through to the Vanguard review desk. 👋\n\nAsk me anything about getting shortlisted, or type <b>submit</b> and I'll take your details right here.`],

    [['how does it work','how it works','process','what happens','shortlist work','shortlisting'],
     `Four steps, no mystery:\n\n<b>1.</b> You send a reel or resume link.\n<b>2.</b> Someone here watches all of it — not the first ten seconds.\n<b>3.</b> If it's ready, we put it on the desk of an agent or casting director looking for exactly what you do.\n<b>4.</b> You hear back either way, usually inside 48 hours.\n\nWant the long version? <a href="how-it-works.html">See How It Works →</a>`],

    [['cost','price','pricing','how much','fee','charge','expensive','afford','payment','pay'],
     `There's no fixed price list — it depends on how much material you have, how many desks we approach and how fast you need it moving.\n\nTell us what you're after and you'll have a number within 24 hours. The number we quote is the number you pay — no percentage surprises later.`],

    [['how fast','how long','timing','turnaround','response time','when will i hear','wait'],
     `48 hours on average for a review decision. Busy weeks it stretches to three days and we'll say so rather than leave you refreshing your inbox.\n\nApproved shortlists go out to desks the same week.`],

    [['what do i send','what should i send','what to send','requirements','material','need from me','prepare'],
     `A link is all we need — Vimeo, YouTube (unlisted is fine), Drive, Dropbox.\n\nIdeally:\n• A reel, self-tape or scene, 1–3 minutes\n• Your resume or credit list\n• A current headshot\n• One line on what you're aiming for next\n\nNo reel yet? Send a self-tape. We've shortlisted people off a single scene.`],

    [['union','sag','equity','aftra','non-union','nonunion','card'],
     `Both. Plenty of the talent we shortlist is non-union and still gets signed.\n\nIf a role or a desk is union-only, we tell you before we submit — not after.`],

    [['chance','odds','likely','will i get','good enough','am i ready','reject'],
     `Honest answer: it depends on the material and the season. About a third of submissions get shortlisted straight away, some get notes and come back stronger, some aren't ready yet.\n\nWhat we won't do is take you on and send nothing. If we can't place you, you'll hear that in plain words.`],

    [['who reviews','who watches','who are you','team','review department','acquisitions'],
     `The Review Department — the talent acquisitions desk here at Vanguard. Real people who've sat on both sides of casting, not a filter and a form.\n\n<a href="about.html">More about the desk →</a>`],

    [['agency','agent','casting director','desk','representation','sign','signed'],
     `We work with agency and casting desks across the UK, Ireland, North America and Europe. When your material fits what one of them is building, it goes straight to a named person.\n\nIf you're an agency looking for talent, start here: <a href="agencies.html">For Agencies & Casting →</a>`],

    [['talent','roster','who do you represent','actors','your talent','books'],
     `Screen actors, commercial talent, stage and theatre, voice and presenting. Every one of them came to us independent.\n\n<a href="talent.html">See the roster →</a> or <a href="shortlisted.html">see recent shortlists →</a>`],

    [['booked','in negotiation','status','tags','what does booked mean'],
     `On the shortlist pages:\n\n<b>Booked</b> — the role is confirmed.\n<b>In negotiation</b> — the desk came back and terms are being agreed.\n<b>Signed</b> — representation agreement in place.`],

    [['location','where','country','city','uk','us','remote','international','territory'],
     `We're remote-first and work across territories — London, Manchester, Dublin, New York, Toronto, Madrid and more.\n\nTell us where you're based and where you'd work, and we match desks in those markets.`],

    [['nda','confidential','private','safe','data','share my'],
     `Your material goes to desks only — never posted publicly, never sold on, never used as marketing without you saying yes in writing. Ask for an NDA and you'll have one the same day.`],

    [['exclusive','contract','lock','commitment','tie'],
     `No exclusivity trap. Shortlisting through us doesn't stop you submitting yourself or signing elsewhere. If an agency signs you, the relationship is yours.`],

    [['beginner','start','no experience','just starting','student','first reel','young','age'],
     `Beginners are welcome — we've shortlisted people whose only footage was a student film and two self-tapes.\n\nWhat matters is whether the material shows something castable. If it doesn't yet, we'll tell you what to shoot next.`],

    [['headshot','photo','resume','cv','profile'],
     `A current headshot and a one-page credit list is plenty. No professional shoot needed to be reviewed — good natural light and an honest face beats an outdated glamour shot.`],

    [['length','how long should','minutes','reel length','duration'],
     `One to three minutes. Lead with your strongest scene — a desk decides in the first twenty seconds whether to keep watching, so don't bury it behind a montage.`],

    [['self tape','self-tape','tape tips','audition tips','tips','improve'],
     `Quick version: eye-line just off lens, clean background, your face lit from the front, sound recorded close, and no reading the whole script — pick the moment that turns.\n\nAsk me for the <b>checklist</b> and I'll send you our full teardown list.`],

    [['checklist','free','guide','teardown','download','magnet'],
     `The Reel Teardown Checklist — the exact 12 things our desk looks for before shortlisting anyone. Free.\n\n<a href="${mailto('Send me the Reel Teardown Checklist','Hi Vanguard,\n\nPlease send me the free Reel Teardown Checklist.\n\nName:\nDiscipline:\nCity:\n\nThanks,')}">Email it to me →</a>`],

    [['feedback','notes','why rejected','critique','review my'],
     `Every submission gets a reason, not a silence. If we pass, you get the notes — what's missing, what to shoot, whether it's a timing issue rather than a talent one.`],

    [['call','zoom','meeting','speak','phone','talk to someone'],
     `Happy to. Email <b>${E}</b> with two or three times that suit you and the desk will confirm one.`],

    [['contact','email','reach','get in touch','address'],
     `Email: <b>${E}</b>\nResponse time: 48 hours average.\n\n<a href="contact.html">Contact page →</a>`],

    [['slot','slots','spaces','availability','full','closed','deadline'],
     `There are <b>${S} shortlist slots</b> left in this review cycle — it closes Friday at midnight, then the desk moves to the next intake.\n\nType <b>submit</b> and I'll take your details now.`],

    [['testimonial','review','success','worked','results','proof'],
     `Alex M. got a lead off a quiet scene nobody else flagged. Zara P. was on three desks in a week. Tyler H. signed after his own agent passed.\n\n<a href="success-stories.html">Read the full stories →</a>`],

    [['thanks','thank you','cheers','appreciate','great','nice'],
     `Any time. If you want the desk to actually see your material, type <b>submit</b> — takes about 40 seconds.`],

    [['bye','goodbye','later','see you'],
     `Good luck out there. We're at <b>${E}</b> whenever your reel is ready. 🎬`]
  ];

  const FLOW = [
    { key: 'name',  q: `Let's do it. First — <b>what's your name?</b>` },
    { key: 'role',  q: `Nice to meet you, {name}. <b>What do you do?</b> (screen actor, commercial, stage, voice…)` },
    { key: 'city',  q: `<b>Which city are you based in?</b>` },
    { key: 'link',  q: `Last big one — <b>paste the link to your reel, self-tape or resume.</b> Vimeo, YouTube, Drive, anything.` },
    { key: 'email', q: `And <b>your email</b>, so the desk can come back to you.` }
  ];

  function answer(raw) {
    const q = raw.toLowerCase().trim();

    if (flow !== null) { return handleFlow(raw); }
    if (/^(submit|send my reel|send reel|apply|sign me|get shortlisted|start)/.test(q)) return startFlow();

    let best = null, score = 0;
    INTENTS.forEach(([keys, ans]) => {
      let s = 0;
      keys.forEach(k => { if (q.includes(k)) s = Math.max(s, k.length); });
      if (s > score) { score = s; best = ans; }
    });
    if (best) return botSay(best, 650);

    botSay(`Good question — and I'd rather give you a real answer than a guess.\n\nEmail the desk at <b>${E}</b> and you'll have one within 48 hours. Or type <b>submit</b> and I'll take your details now so the review starts either way.`, 700);
  }

  function startFlow() {
    flow = 0; data = {};
    botSay(FLOW[0].q, 500);
  }

  function handleFlow(val) {
    data[FLOW[flow].key] = val.trim();
    flow++;
    if (flow < FLOW.length) {
      return botSay(FLOW[flow].q.replace('{name}', (data.name || '').split(' ')[0]), 550);
    }
    const subject = `Reel submission — ${data.name}`;
    const bodyTxt = `Name: ${data.name}\nDiscipline: ${data.role}\nCity: ${data.city}\nReel / resume: ${data.link}\nEmail: ${data.email}\n\nSent from the Vanguard site assistant.`;
    flow = null;
    botSay(`Got it, ${(data.name || '').split(' ')[0]} — here's what I have:\n\n<b>Name:</b> ${data.name}\n<b>Discipline:</b> ${data.role}\n<b>City:</b> ${data.city}\n<b>Link:</b> ${data.link}\n<b>Email:</b> ${data.email}\n\nOne tap to send it to the review desk:\n\n<a href="${mailto(subject, bodyTxt)}"><b>📨 Send this to the desk →</b></a>\n\nYou'll hear back within 48 hours — including if the answer is no.`, 800);
  }

  function userAsked(text) {
    say(text.replace(/</g, '&lt;'), 'user');
    answer(text);
  }

  function open() {
    panel.classList.add('on');
    $('#chatBadge')?.remove();
    if (!started) {
      started = true;
      botSay(`Hi — Vanguard review desk. 👋\n\n<b>${S} shortlist slots</b> left this cycle. Ask me anything, or type <b>submit</b> and I'll take your details straight to the desk.`, 450);
    }
    setTimeout(() => input?.focus(), 300);
  }

  fab.addEventListener('click', () => panel.classList.contains('on') ? panel.classList.remove('on') : open());
  $('#chatClose')?.addEventListener('click', () => panel.classList.remove('on'));
  $$('[data-chat-quick]').forEach(b => b.addEventListener('click', () => {
    if (!panel.classList.contains('on')) open();
    userAsked(b.dataset.chatQuick);
  }));
  $$('[data-chat-open]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); open(); }));

  form?.addEventListener('submit', e => {
    e.preventDefault();
    const v = input.value.trim(); if (!v) return;
    input.value = ''; userAsked(v);
  });

  // nudge: open the badge after 25s if untouched
  setTimeout(() => { if (!started) $('#chatBadge')?.classList.add('flash'); }, 25000);
})();
