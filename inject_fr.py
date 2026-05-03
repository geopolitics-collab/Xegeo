#!/usr/bin/env python3
"""
Inject into all French GeoPolo articles:
  1. Google AdSense — after the 2nd <p> in the article body
  2. 13 social share buttons — before <footer> (or </body>)

Anti-duplication: each marker is checked before every injection.
"""
import os, re, glob

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "articles")

# ── Markers ──────────────────────────────────────────────
ADSENSE_MARKER = "ca-pub-7897922032846846"
SHARE_MARKER   = "shr-block"

# ── AdSense script ───────────────────────────────────────
ADSENSE = (
    '\n<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    'adsbygoogle.js?client=ca-pub-7897922032846846" crossorigin="anonymous"></script>\n'
)

# ── Share buttons CSS (injected once into <style> or new <style>) ──
SHARE_CSS = """
/* ── SHARE BUTTONS ── */
.shr-block{margin:2.5rem 0;padding:1.4rem 1.6rem;background:#f9f7f4;border-top:2px solid #e5ddd0;border-bottom:2px solid #e5ddd0}
.shr-label{font-family:monospace;font-size:.62rem;letter-spacing:.18em;text-transform:uppercase;color:#8a807a;margin-bottom:.9rem;font-weight:600}
.shr-list{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem;padding:0;margin:0}
.shr-list li{margin:0;padding:0}
.shr{display:inline-flex;align-items:center;padding:.36rem .82rem;font-family:monospace;font-size:.68rem;font-weight:600;letter-spacing:.04em;border:1px solid #ccc5bb;background:#fff;color:#3a3530;cursor:pointer;text-decoration:none;transition:background .2s,color .2s,border-color .2s;white-space:nowrap}
.shr:hover,.shr-cp:hover{background:#0c0d12;color:#fff;border-color:#0c0d12}
.shr-x:hover{background:#000;border-color:#000}
.shr-wa:hover{background:#25d366;border-color:#25d366;color:#fff}
.shr-fb:hover{background:#1877f2;border-color:#1877f2;color:#fff}
.shr-tg:hover{background:#229ed9;border-color:#229ed9;color:#fff}
.shr-li:hover{background:#0a66c2;border-color:#0a66c2;color:#fff}
.shr-rd:hover{background:#ff4500;border-color:#ff4500;color:#fff}
.shr-bsky:hover{background:#0085ff;border-color:#0085ff;color:#fff}
.shr-ms:hover{background:#1877f2;border-color:#1877f2;color:#fff}
.shr-tt:hover{background:#010101;border-color:#010101;color:#fff}
.shr-sc:hover{background:#fffc00;border-color:#f0e800;color:#000}
.shr-sg:hover{background:#3a76f0;border-color:#3a76f0;color:#fff}
.shr-em:hover{background:#555;border-color:#555;color:#fff}
.shr-cp{background:#fff;border:1px solid #ccc5bb;color:#3a3530;font-family:monospace;font-size:.68rem;font-weight:600;letter-spacing:.04em;padding:.36rem .82rem;cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.shr-cp:hover{background:#1a8a6e;border-color:#1a8a6e;color:#fff}
@media(max-width:580px){.shr,.shr-cp{padding:.3rem .6rem;font-size:.6rem}}
"""

# ── Share buttons HTML block ──────────────────────────────
SHARE_HTML = """<div class="shr-block">
  <div class="shr-label">Partager l'article</div>
  <ul class="shr-list">
    <li><a class="shr shr-x"    href="#" onclick="shr('x');return false">𝕏</a></li>
    <li><a class="shr shr-wa"   href="#" onclick="shr('wa');return false">WhatsApp</a></li>
    <li><a class="shr shr-fb"   href="#" onclick="shr('fb');return false">Facebook</a></li>
    <li><a class="shr shr-tg"   href="#" onclick="shr('tg');return false">Telegram</a></li>
    <li><a class="shr shr-li"   href="#" onclick="shr('li');return false">LinkedIn</a></li>
    <li><a class="shr shr-rd"   href="#" onclick="shr('rd');return false">Reddit</a></li>
    <li><a class="shr shr-bsky" href="#" onclick="shr('bsky');return false">Bluesky</a></li>
    <li><a class="shr shr-ms"   href="#" onclick="shr('ms');return false">Messenger</a></li>
    <li><a class="shr shr-tt"   href="#" onclick="shr('tt');return false">TikTok</a></li>
    <li><a class="shr shr-sc"   href="#" onclick="shr('sc');return false">Snapchat</a></li>
    <li><a class="shr shr-sg"   href="#" onclick="shr('sg');return false">Signal</a></li>
    <li><a class="shr shr-em"   href="#" onclick="shr('em');return false">Email</a></li>
    <li><button class="shr-cp"  onclick="shr('cp')">Copier le lien</button></li>
  </ul>
</div>
<script>
(function(){
  if(window._shrFn) return;
  window._shrFn = true;
  window.shr = function(p){
    var u = encodeURIComponent(window.location.href);
    var h = document.querySelector('h1');
    var t = encodeURIComponent(h ? h.textContent.trim() : document.title);
    var urls = {
      x:    'https://twitter.com/intent/tweet?url='+u+'&text='+t,
      wa:   'https://wa.me/?text='+t+'%20'+u,
      fb:   'https://www.facebook.com/sharer/sharer.php?u='+u,
      tg:   'https://t.me/share/url?url='+u+'&text='+t,
      li:   'https://www.linkedin.com/sharing/share-offsite/?url='+u,
      rd:   'https://reddit.com/submit?url='+u+'&title='+t,
      bsky: 'https://bsky.app/intent/compose?text='+t+'%20'+u,
      ms:   'https://www.facebook.com/dialog/send?link='+u+'&app_id=966242223397198',
      tt:   'https://www.tiktok.com/share?url='+u,
      sc:   'https://www.snapchat.com/scan?attachmentUrl='+u,
      sg:   'https://signal.me/share?url='+u+'&text='+t,
      em:   'mailto:?subject='+t+'&body='+u
    };
    if(p === 'cp'){
      navigator.clipboard.writeText(window.location.href).then(function(){
        var btn = document.querySelector('.shr-cp');
        if(!btn) return;
        var old = btn.textContent;
        btn.textContent = '✓ Copié !';
        btn.style.background = '#1a8a6e';
        btn.style.color = '#fff';
        setTimeout(function(){ btn.textContent = old; btn.style.background=''; btn.style.color=''; }, 2200);
      });
    } else {
      window.open(urls[p], '_blank', 'noopener,width=660,height=460');
    }
  };
})();
</script>"""

# ── Body start patterns ───────────────────────────────────
BODY_PATTERNS = [
    re.compile(r'<div\s+class="wrap"[^>]*>', re.I),
    re.compile(r'<section\s+class="article-body"[^>]*>', re.I),
    re.compile(r'<article\b[^>]*>', re.I),
    re.compile(r'<main\b[^>]*>', re.I),
]

# End-of-article anchors (tried in order)
END_ANCHORS = ["<footer", "</main>", "</body>"]


def find_body_start(content):
    for pat in BODY_PATTERNS:
        m = pat.search(content)
        if m:
            return m.end()
    return None


def inject_adsense(content):
    """Insert AdSense after the 2nd </p> in the article body."""
    if ADSENSE_MARKER in content:
        return content, False

    body_start = find_body_start(content)
    search_from = body_start if body_start else 0
    closes = [m.end() for m in re.finditer(r'</p>', content[search_from:], re.I)]

    if not closes:
        return content, False

    # After 2nd paragraph if available, else after 1st
    target = closes[1] if len(closes) >= 2 else closes[0]
    idx = search_from + target
    return content[:idx] + ADSENSE + content[idx:], True


def inject_share(content):
    """Insert share block + CSS before <footer> (or </body>)."""
    if SHARE_MARKER in content:
        return content, False

    # Inject CSS into existing <style> block or add new one before </head>
    if "</style>" in content and SHARE_MARKER not in content:
        content = content.replace("</style>", SHARE_CSS + "\n</style>", 1)
    elif "</head>" in content:
        content = content.replace("</head>", f"<style>{SHARE_CSS}</style>\n</head>", 1)

    # Find best anchor for share block
    for anchor in END_ANCHORS:
        pos = content.find(anchor)
        if pos != -1:
            content = content[:pos] + SHARE_HTML + "\n" + content[pos:]
            return content, True

    # Last-resort: append before </html>
    if "</html>" in content:
        content = content.replace("</html>", SHARE_HTML + "\n</html>")
        return content, True

    return content, False


def process(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    original  = content
    ads_done  = False
    shr_done  = False

    content, ads_done = inject_adsense(content)
    content, shr_done = inject_share(content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return ads_done, shr_done


def main():
    files = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html")))
    print(f"🗞  GeoPolo FR — {len(files)} articles\n")

    ads_total = shr_total = skipped = errors = 0

    for fp in files:
        name = os.path.basename(fp)
        try:
            ads, shr = process(fp)
            if ads or shr:
                tag = []
                if ads: tag.append("AdSense"); ads_total += 1
                if shr: tag.append("Share×13"); shr_total += 1
                print(f"  ✅ {name}  [{', '.join(tag)}]")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ❌ {name}: {e}")

    print(f"\n✅ AdSense: {ads_total}  |  Share: {shr_total}  |  ignorés: {skipped}  |  erreurs: {errors}")


if __name__ == "__main__":
    main()
