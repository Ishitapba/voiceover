# Blog to Voiceover

A free, unlimited alternative to sites like aiktp.com. Paste blog text, pick
a natural-sounding voice (including Australian English), generate a
ready-to-download MP3. Hosted on **Render.com**'s free tier, so your team
member just opens a link — nothing to install.

Built on **edge-tts**, a free open-source library using the same natural
neural voices behind Microsoft Edge's "Read Aloud" feature.

(Note: Hugging Face Spaces now requires a paid plan for Gradio apps —
only their "Static" browser-only template is free, which can't run this.
Render's free web service tier still supports real Python apps with no
credit card required.)

## Deploy it — using Mac Terminal

1. **Create an empty GitHub repo** (one-time): go to github.com → sign in
   (or create a free account) → click **+** (top right) → **New repository**
   → name it `blog-to-voiceover` → Create repository. Leave it empty — don't
   add a README there.

2. **Open Terminal** and push this folder to it (replace `YOUR-USERNAME`):

   ```bash
   cd path/to/blog-to-voiceover-cloud
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/blog-to-voiceover.git
   git push -u origin main
   ```

   Terminal will prompt for your GitHub login the first time (it'll open a
   browser to authenticate, or ask for a personal access token instead of a
   password — GitHub will show instructions if so).

3. **Create a free Render account**: go to render.com → sign up (GitHub
   sign-in is easiest, no card needed).

4. **New → Web Service** → connect the `blog-to-voiceover` repo you just
   pushed.

5. Set:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free

6. Click **Create Web Service**. Render builds and deploys (~2-3 min), then
   gives you a live URL like `https://blog-to-voiceover.onrender.com`.

7. Share that URL with your team member. They just open it and use it.

## Deploy it — without Terminal (GitHub web UI only)

If you'd rather not use git commands: create the empty GitHub repo as in
step 1 above, then on the repo page click **uploading an existing file**
and drag in `app.py`, `requirements.txt`, and this `README.md`. Commit
directly to `main`. Then continue from step 3 above.

## Notes

- Free tier detail: the app "sleeps" after 15 minutes with no visitors and
  takes about a minute to wake up on the next visit — normal for free
  hosting, no action needed.
- No API keys, accounts (for your team member), or per-use cost.
- To add more voices/accents, edit the `VOICES` dictionary in `app.py` —
  any edge-tts voice name works.
- If you ever update the app, just `git add . && git commit -m "update" &&
  git push` from the same folder — Render redeploys automatically.
