# Learn app — setup (one-time, ~10 min)

An offline, installable iPhone app for your academic-set **lessons + quizzes**, that **auto-updates over the air**. How it works: your Mac regenerates a `content.json` from your sets → pushes it to free HTTPS hosting (GitHub Pages) → the home-screen app fetches it and caches it for offline.

## What's in this folder
| File | Role |
|---|---|
| `index.html` | the app (lessons + spaced-repetition quizzes, offline) |
| `manifest.webmanifest` | makes it installable to the home screen |
| `sw.js` | service worker — offline + OTA content fetch |
| `icon-192.png` / `icon-512.png` / `icon-180.png` | app icons |
| `content.json` | your real content (3 subjects, 16 lessons, 30 cards) — regenerated automatically |
| `generate_content.py` | reads your sets → `content.json` (auto-includes new sets) |
| `sync_content.sh` | regenerate + push (the auto-update step) |

---

## Step 1 — Host it on GitHub Pages (free, HTTPS)
1. Create a free **GitHub** account if you don't have one. Install **GitHub Desktop** (handles login/auth without command-line fuss).
2. Make a new repository, e.g. **`learn-app`** (public is fine — this is non-sensitive learning content; never put anything sensitive in your sets).
3. Copy **all the files in this folder** into the repo, commit, and push (GitHub Desktop: drag files in → "Commit" → "Push").
4. On github.com: repo → **Settings → Pages** → Source = `main` branch, root folder → Save. After a minute it gives you a URL like `https://<you>.github.io/learn-app/`.

> Quick alternative for an instant look (no account): drag this folder onto **app.netlify.com/drop** for a temporary HTTPS URL. (For the *automatic* OTA updates, use the GitHub path above.)

## Step 2 — Put it on your iPhone
1. Open the Pages URL in **Safari** on your iPhone.
2. Tap **Share → Add to Home Screen**. It installs like an app (your graduation-cap icon), runs full-screen, and works offline on the train.
3. First open online caches everything; after that it works with no signal. Your progress (lessons done, quiz spacing) is saved on the phone.

## Step 3 — Make it auto-update (OTA)
So new lessons/quizzes (and new sets) flow to your phone without you doing anything:
1. Clone your `learn-app` repo locally (GitHub Desktop does this) — note its folder path.
2. Edit `sync_content.sh`: set `REPO=` to that local clone path.
3. Test it once: `bash sync_content.sh` → it regenerates `content.json` and pushes.
4. **Schedule it.** Ask Claude (in a chat with your folders mounted): *"create the learn-content-sync scheduled task"* and give it your repo path — Claude will set a weekly (or daily) task that runs `sync_content.sh`. From then on, the app updates OTA: open it on wifi and it pulls the latest.

That's it. Add a new academic set on the desktop → next sync → it appears on your phone.

---

## Notes
- **Offline:** works fully offline after first load; reconnect to pick up updates.
- **Lessons** are currently outline-level for most subjects (the quizzes are complete) — they fill in as you run `LEARN: <subject>` on the desktop, and sync across automatically.
- **Privacy:** content is your clean-side learning material (home automation etc.) — no PHI, safe to host publicly. Keep it that way.
- **Want a different host** (private, or no GitHub)? Ask Claude — Netlify/Cloudflare Pages work the same way.
