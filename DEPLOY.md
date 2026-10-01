# Deploying Vanguard Placement Group to Cloudflare

You have two files. Use **one** of them, depending on how your Cloudflare project was created.

| File | Use it when |
|---|---|
| `vanguard-cloudflare.zip` | You're using **Cloudflare Pages** (drag & drop / "Upload assets") |
| `vanguard-workers.zip` | You're using **Workers** with Wrangler CLI or a Git repo |

---

## ⚠️ The usual reason a deploy fails

**1. The zip had a folder inside it.**
Cloudflare looks for `index.html` at the *top level* of what you upload. If it unpacks to
`vanguard/index.html`, the deploy either fails or gives you a blank page / 404 on every route.

`vanguard-cloudflare.zip` is now **flat** — `index.html` is at the root, no wrapper folder.

**2. The project was created as a "Worker", not a static site.**
A plain Worker expects JavaScript with a `fetch` handler. Uploading HTML to it fails with
something like `Uncaught TypeError: Cannot read properties of undefined` or
`No event handlers were registered`. Static HTML needs **Pages** or **Workers + Static Assets**.

**3. A build command was set.**
Cloudflare tried to auto-detect a framework and ran `npm run build`, which fails because
there is no `package.json` / build step. This site needs **no build at all**.

---

## Option A — Cloudflare Pages (easiest, recommended)

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** tab → **Upload assets**
2. Project name: `vanguard-placement-group`
3. Unzip `vanguard-cloudflare.zip` on your computer, then **drag the 23 loose files**
   (or the unzipped folder's *contents*) into the upload box — not the folder itself
4. Click **Deploy site**

You get `https://vanguard-placement-group.pages.dev`

If the dashboard asks for build settings:

- Framework preset: **None**
- Build command: **leave completely empty**
- Build output directory: **`/`**

---

## Option B — Workers with Static Assets (Wrangler CLI)

```bash
unzip vanguard-workers.zip -d vanguard-deploy
cd vanguard-deploy
npx wrangler login
npx wrangler deploy
```

The included `wrangler.toml` already says:

```toml
name = "vanguard-placement-group"
compatibility_date = "2025-09-01"

[assets]
directory = "./public"
not_found_handling = "404-page"
```

That tells Workers "serve these files, there is no server code" — which is what
a plain Worker project is missing when the deploy fails.

---

## Option C — Fixing the project you already created

If you already made a Worker and it won't accept the files:

1. Dashboard → your project → **Settings** → scroll to the bottom → **Delete project**
   (nothing else is attached to it — but check the name first, deleting is permanent)
2. Re-create it using **Option A** above.

Alternatively keep the project and just run `npx wrangler deploy` from Option B against
the same name — it will convert it into an assets-serving Worker.

---

## After it's live

- Custom domain: project → **Custom domains** → add `vanguardplacementgroup.com`
- `404.html` is picked up automatically by Pages
- `_headers` and `_redirects` are included and only do anything on Pages
- Every page is static HTML — no database, no API keys, nothing to configure

## What I need to debug further

Paste the **exact error text** Cloudflare showed, plus:

- Was the project created under **Pages** or **Workers**?
- Did you upload a **zip**, a **folder**, or connect a **Git repo**?
- Did the failure happen at **upload**, at **build**, or does it deploy but show a blank page / 404?
