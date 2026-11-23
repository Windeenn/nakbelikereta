# Kalendar Meja Wanita Cantik 2027 — Landing Page

Landing page tempahan untuk **wanitacantik.sublee.my**.

- Copywriting: struktur **PAS** (Problem → Agitate → Solution) dalam funnel **TOFU → MOFU → BOFU**
  - TOFU: hero / hook
  - MOFU: masalah, agitasi, 4 ciri, untuk siapa, clicker
  - BOFU: harga, borang tempahan (hantar ke WhatsApp), FAQ, CTA akhir
- Harga: Kalendar RM35 · Clicker RM17 · Combo RM47
- Tempahan dihantar ke WhatsApp +6011 4301 0078

Laman statik (HTML/CSS/JS) — tiada build step.

## Deploy (GitHub Pages)

1. Settings → Pages → Source: *Deploy from a branch*, pilih branch & folder `/ (root)`.
2. Fail `CNAME` dah set ke `wanitacantik.sublee.my`.
3. Di DNS `sublee.my`, tambah rekod:
   ```
   Type: CNAME   Name: wanitacantik   Value: <username>.github.io
   ```
4. Tunggu DNS propagate, kemudian tick **Enforce HTTPS**.
