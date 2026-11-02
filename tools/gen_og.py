# -*- coding: utf-8 -*-
"""Render one Open Graph card per page.

The card is the research-group site's: a dark observation surface, the
concentric mark, the page title and a monospace footer. Rendered by headless
Chrome at 1200x630 so the Japanese type comes out right.

Usage:  python3 -I tools/gen_og.py
"""
import html as _html
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "og")
HOST = "affectosphere.group"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

# (output name, kicker, title, tagline)
CARDS = [
    ("home", "Affectosphere / Emotion AI Company",
     "感情AIを社会へ広げ、生活を最適化する。",
     "他社のサービスや組織の「感情の部分」を担う。"),
    ("affectosphere", "Affectosphere",
     "感情が社会を満たす環境を、事業の対象に。", ""),
    ("vision", "Vision",
     "Affectosphere時代を、ひらく。", ""),
    ("technology", "Technology",
     "ACとCAI：感情を扱う技術と、その地図。", ""),
    ("contact", "Contact", "お問い合わせ。", ""),
    ("company", "Company", "会社概要。", ""),
    ("thanks", "Thank you", "お問い合わせ、ありがとうございます。", ""),
]


def card(kicker, title, tagline):
    size = 62 if len(title) > 18 else 76
    tag = (f'<p class="tagline">{_html.escape(tagline)}</p>' if tagline else "")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ margin: 0 }}
* {{ margin: 0; padding: 0; box-sizing: border-box }}
body {{
  width: 1200px; height: 630px; background: #111318; color: #F4F2ED;
  font-family: "Hiragino Mincho ProN", "Noto Serif JP", serif;
  position: relative; overflow: hidden;
}}
.grid {{
  position: absolute; inset: 0;
  background-image:
    linear-gradient(to right, rgba(233,230,223,.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(233,230,223,.05) 1px, transparent 1px);
  background-size: 72px 72px;
}}
svg {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); }}
.inner {{ position: relative; height: 100%; padding: 74px 88px; display: flex; flex-direction: column; }}
.kicker {{
  font-family: "SF Mono", ui-monospace, monospace; font-size: 20px;
  letter-spacing: .22em; color: #9AA4B4; text-transform: uppercase;
}}
h1 {{ margin-top: auto; font-size: {size}px; line-height: 1.24; font-weight: 600; letter-spacing: -.01em; }}
.tagline {{ margin-top: 26px; font-size: 27px; line-height: 1.6; color: #CFCBC2; max-width: 30ch; }}
.foot {{
  margin-top: auto; padding-top: 34px; display: flex; justify-content: space-between;
  align-items: baseline; border-top: 1px solid #2B3341;
  font-family: "SF Mono", ui-monospace, monospace; font-size: 19px;
  letter-spacing: .12em; color: #6E7889;
}}
.amber {{ color: #C4974A }}
</style></head><body>
<div class="grid"></div>
<svg width="900" height="900" viewBox="0 0 200 200" fill="none">
  <g stroke="#E9E6DF" stroke-width=".25" opacity=".26">
    <circle cx="100" cy="100" r="26"/><circle cx="100" cy="100" r="44"/>
    <circle cx="100" cy="100" r="64"/><circle cx="100" cy="100" r="86"/>
  </g>
  <circle cx="100" cy="100" r="26" stroke="#C4974A" stroke-width=".45" opacity=".55"/>
</svg>
<div class="inner">
  <p class="kicker">{_html.escape(kicker)}</p>
  <h1>{_html.escape(title)}</h1>
  {tag}
  <div class="foot"><span>Affect<span class="amber">o</span>sphere</span><span>{HOST}</span></div>
</div>
</body></html>"""


def main():
    chrome = next((p for p in CHROME_CANDIDATES if os.path.exists(p)), None)
    if not chrome:
        raise SystemExit("No Chrome binary found; cannot render the cards.")
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="og-")
    try:
        for name, kicker, title, tagline in CARDS:
            src = os.path.join(tmp, "card.html")
            png = os.path.join(tmp, "card.png")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(card(kicker, title, tagline))
            if os.path.exists(png):
                os.remove(png)
            subprocess.run(
                [chrome, "--headless", "--disable-gpu", "--no-sandbox",
                 "--hide-scrollbars", "--force-device-scale-factor=1",
                 "--window-size=1200,630", f"--screenshot={png}",
                 "--virtual-time-budget=4000", "file://" + src],
                check=False, capture_output=True)
            if not os.path.exists(png):
                raise SystemExit("render failed for " + name)
            dst = os.path.join(OUT, name + ".png")
            shutil.copyfile(png, dst)
            print("wrote og/%s.png" % name, os.path.getsize(dst))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
