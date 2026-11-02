#!/usr/bin/env python3
"""Generate the Affectosphere corporate site's static pages (nav v2).

Tab structure: Affectosphere / ビジョン / 技術 / お問い合わせ.
The former 概念, CAI and できること pages are folded into Affectosphere and
技術; their old URLs stay as redirect stubs so existing links keep working.
"""
import os

# Output goes to the repository root (this file lives in tools/).
DST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUP_CONTACT = "https://lab.affectosphere.group/contact/"

NAV = [
    ("Affectosphere", "affectosphere.html"),
    ("ビジョン", "vision.html"),
    ("技術", "technology.html"),
    ("お問い合わせ", "contact.html"),
]

MARK = """<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">
          <circle cx="16" cy="16" r="12.5" fill="none" stroke="currentColor" stroke-width="1" opacity="0.28"/>
          <circle cx="16" cy="16" r="9" fill="none" stroke="currentColor" stroke-width="1.25"/>
          <circle cx="16" cy="16" r="4.75" fill="none" stroke="#C4974A" stroke-width="1.25"/>
          <circle cx="16" cy="16" r="1.75" fill="currentColor"/>
        </svg>"""


def header(current):
    def tabs():
        out = []
        for label, href in NAV:
            cur = ' aria-current="page"' if href == current else ""
            out.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
        return ("\n" + " " * 8).join(out)

    return f"""<header class="site-header">
  <div class="wrap brand-row">
    <a class="brand" href="index.html" aria-label="Affectosphere ホーム">
      {MARK}
      <span class="brand-name">
        <b>Affectosphere</b>
        <span>Emotion AI Company</span>
      </span>
    </a>
    <div class="header-actions">
      <a class="ghost-square" href="contact.html">お問い合わせ</a>
      <button class="nav-toggle" type="button" aria-label="メニューを開く" aria-expanded="false" data-nav-toggle>
        <svg width="20" height="14" viewBox="0 0 20 14" fill="none" aria-hidden="true">
          <path d="M0 1h20M0 7h20M0 13h20" stroke="currentColor" stroke-width="1.5"/>
        </svg>
      </button>
    </div>
  </div>

  <nav class="nav-band" aria-label="主要メニュー">
    <div class="wrap">
      <ul>
        {tabs()}
      </ul>
    </div>
  </nav>

  <div class="nav-drawer" data-nav-drawer>
    <div class="wrap">
      <ul>
        {tabs()}
      </ul>
    </div>
  </div>
</header>"""


def contact_block(heading, body):
    return f"""<section class="surface-ink">
  <div class="ink-grid" aria-hidden="true"></div>
  <div class="wrap contact-block">
    <p class="eyebrow">Contact</p>
    <h2>{heading}</h2>
    <p>{body}</p>
    <p><a class="mail" href="{GROUP_CONTACT}" target="_blank" rel="noopener">お問い合わせフォームへ <span aria-hidden="true">&#8599;</span></a></p>
  </div>
</section>"""


FOOTER = """<footer class="site-footer">
  <div class="wrap inner">
    <p class="fbrand">Affectosphere</p>
    <p class="ftag">感情AIを、社会へ。Affectosphere時代に、感情最適化された暮らしをつくる。</p>
    <div class="flinks">
      <a href="index.html">ホーム</a>
      <a href="affectosphere.html">Affectosphere</a>
      <a href="vision.html">ビジョン</a>
      <a href="technology.html">技術</a>
      <a href="contact.html">お問い合わせ</a>
      <a href="company.html">会社概要</a>
      <a href="https://lab.affectosphere.group/" target="_blank" rel="noopener">研究グループ &#8599;</a>
      <a href="https://news.affectosphere.group/" target="_blank" rel="noopener">ニュース &#8599;</a>
    </div>
  </div>
  <div class="wrap copy">&copy; 2026 AFFECTOSPHERE &middot; EMOTION AT THE CORE OF AI</div>
</footer>"""


SITE_JS = """<script src="js/site.js" defer></script>"""


def page(filename, title, description, body, current=None, extra_head=""):
    html = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Affectosphere">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{extra_head}</head>
<body>

{header(current)}

<main>
{body}
</main>

{FOOTER}

{SITE_JS}
</body>
</html>
"""
    with open(os.path.join(DST, filename), "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", filename, len(html))


def redirect(filename, target, title, note):
    """Keep an old URL alive after its content moved."""
    html = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
<section class="surface-ink">
  <div class="ink-grid" aria-hidden="true"></div>
  <div class="wrap page-head">
    <p class="eyebrow">Moved</p>
    <h1>このページは移動しました。</h1>
    <p class="lead">{note} 自動で移動しない場合は、<a class="link-amber" href="{target}">こちら</a>をご覧ください。</p>
  </div>
</section>
</main>
</body>
</html>
"""
    with open(os.path.join(DST, filename), "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", filename, len(html), "(redirect ->", target + ")")


def head_section(eyebrow, h1, lead):
    return f"""<section class="surface-ink">
  <div class="ink-grid" aria-hidden="true"></div>
  <div class="wrap page-head">
    <p class="eyebrow reveal">{eyebrow}</p>
    <h1 class="reveal">{h1}</h1>
    <p class="lead reveal">{lead}</p>
  </div>
</section>"""


def sec(num, kicker, title, lead=None, body="", band=""):
    lead_html = f'\n    <p class="lead">{lead}</p>' if lead else ""
    cls = "band" + (f" {band}" if band else "")
    return f"""<section class="{cls}">
  <div class="wrap">
    <header class="sec-head reveal">
      <p class="eyebrow">{num} &mdash; {kicker}</p>
      <h2>{title}</h2>{lead_html}
    </header>
{body}
  </div>
</section>"""


def cards3(items):
    """items: (no, title, text) or (no, title, text, sublabel)."""
    out = []
    for it in items:
        n, t, d = it[0], it[1], it[2]
        sub = f'<p class="sublabel">{it[3]}</p>' if len(it) > 3 else ""
        out.append(
            f'      <article class="card reveal"><p class="no">{n}</p>'
            f"<h3>{t}</h3><p>{d}</p>{sub}</article>")
    return '    <div class="cards c3">\n' + "\n".join(out) + "\n    </div>"


def rows(items, wide=False, accent=False):
    """items: (meta, heading, text); heading may be empty."""
    cls = "rows wide" if wide else "rows"
    pcls = ' class="accent"' if accent else ""
    out = []
    for meta, heading, text in items:
        h = f"\n          <h3>{heading}</h3>" if heading else ""
        out.append(f"""      <li class="reveal">
        <div><span class="meta">{meta}</span></div>
        <div class="body">{h}
          <p{pcls}>{text}</p>
        </div>
      </li>""")
    return f'    <ul class="{cls}">\n' + "\n".join(out) + "\n    </ul>"


# ── Home ────────────────────────────────────────────────────────────────────
HERO = """<section class="hero" aria-labelledby="hero-heading">
  <img class="hero-bg" src="hero/town-poster.webp" alt="" aria-hidden="true" width="1800" height="990">
  <canvas class="hero-canvas" data-hero-town aria-hidden="true"></canvas>

  <div class="hero-panels" aria-hidden="true">
    <div class="hero-dash left" data-hero-dash="field"
         data-names='["喜び","信頼","恐れ","驚き","悲しみ","嫌悪","怒り","期待"]'>
      <p class="pk">Affectosphere &middot; Field</p>
      <h3 class="pt">場の感情を追う</h3>
      <div class="row"><span>観測人数</span><span class="v"><span data-f="n">&ndash;</span></span></div>
      <ul data-f="bars" class="bars"></ul>
      <dl>
        <dt>場の確信度</dt><dd data-f="certainty">&ndash;</dd>
        <dt>干渉</dt><dd data-f="agreement">&ndash;</dd>
      </dl>
      <p class="pn">例示分布（実データではありません）</p>
    </div>

    <div class="hero-dash right" data-hero-dash="person"
         data-modes='["街を歩く","公園にいる"]'>
      <p class="pk">Person &middot; Tracking</p>
      <h3 class="pt">ひとりの感情を追う</h3>
      <div class="row"><span class="v" data-f="id">&ndash;</span><span data-f="mode">&ndash;</span></div>
      <svg class="spark" viewBox="0 0 100 26" preserveAspectRatio="none" aria-hidden="true">
        <path data-f="spark-area" d="" fill="#C4974A" fill-opacity="0.14"></path>
        <polyline data-f="spark" points="" fill="none" stroke="#C4974A" stroke-width="1.4"
                  stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"></polyline>
      </svg>
      <dl>
        <dt>最も強い感情</dt><dd><span data-f="top">&ndash;</span> <span data-f="topv">&ndash;</span></dd>
        <dt>確信度</dt><dd data-f="pcertainty">&ndash;</dd>
        <dt>覚醒度</dt><dd data-f="arousal">&ndash;</dd>
      </dl>
      <p class="pn">例示分布（実データではありません）</p>
    </div>
  </div>

  <div class="hero-wash" aria-hidden="true"></div>

  <div class="wrap hero-inner">
    <p class="eyebrow reveal">Affectosphere &middot; Emotion AI Company</p>
    <h1 id="hero-heading" class="reveal">
      <span class="era">Affectosphere時代に、</span>
      <span class="line">感情AIを社会へ広げ、</span>
      <span class="line">生活を最適化する。</span>
    </h1>
    <p class="sub reveal">
      感情は、社会を満たす環境になりました。その時代に、感情を理解するAIをあらゆる現場へ届け、
      暮らしと社会をより良くする：<strong>感情最適化された時代</strong>をつくる会社です。
    </p>
    <div class="cta reveal">
      <a class="btn btn-solid" href="technology.html">技術とできることを見る <span class="arw">&rarr;</span></a>
      <a class="btn btn-ghost" href="affectosphere.html">Affectosphereとは <span class="arw">&rarr;</span></a>
    </div>
  </div>
</section>"""

HOME_CONCEPT = """    <div class="figrow reveal">
      <div class="measure">
        <p class="lead">感情は、個人の内面を超えて、言葉・声・行動として社会のあらゆる場所にあふれ、社会を満たす環境になりました。私たちはこれを <strong>Affectosphere（情動圏）</strong> と呼びます。この環境を測り、理解し、活かす層が、感情AIです。</p>
        <p class="lead" style="margin-top:1.1rem">その技術の土台が <strong>Affective Computing（AC／感情計算）</strong>、備えるべき力を体系化した枠組みが <strong>CAI（計算論的感情知性）</strong>です。事業の接点はACに集まり、CAIはその全体像を示します。</p>
        <p style="margin-top:1.6rem"><a class="btn btn-ghost" href="affectosphere.html">Affectosphere を詳しく見る <span class="arw">&rarr;</span></a></p>
      </div>
      <div class="fig"><img src="img/aff-tracking.webp" alt="街のなかの感情を観測する様子の図" width="1024" height="1024" loading="lazy"></div>
    </div>"""

HOME_WHAT = rows([
    ("01 ／ 設計・実装", "場面別の感情AIの設計・実装",
     "目的の整理、扱えるデータと倫理上の制約の確認、技術の選定・組み合わせ、試作、評価、組み込みまで。受託研究開発としてお引き受けします。"),
    ("02 ／ 基盤モデル", "感情基盤モデルの提供",
     "多様な感情タスクを一つで扱う感情基盤モデル <strong>Affeline</strong>。研究用・非商用のライセンスで Hugging Face に公開しているほか、商用利用のライセンスとAPIの形でご提供します。"),
    ("03 ／ データ", "感情データの分析・作成",
     "注釈者間の不一致の分析、受け取り方の割れが分かる感情データの作成。お手元のデータの分析も、データそのものの提供も行います。"),
    ("04 ／ 評価・教育", "感情AIの評価・監査と倫理教育",
     "感情AIの判定の偏りや妥当性を検証します。導入前の点検、評価の設計、企業・開発者向けの感情AI倫理教育まで。"),
], wide=True) + """
    <div class="measure-wide reveal" style="margin-top:2.5rem">
      <p class="note">あわせて、メディア活動・書籍・セミナー、展示会での感情AIアートの展示を通じて、感情AIの使い方そのものを社会に広げます。</p>
      <p style="margin-top:1.6rem"><a class="btn btn-ghost" href="technology.html">技術とできることを見る <span class="arw">&rarr;</span></a></p>
    </div>"""

HOME_PROBLEMS = """<section class="surface-ink band ink">
  <div class="ink-grid" aria-hidden="true"></div>
  <div class="wrap" style="position:relative">
    <header class="sec-head reveal">
      <p class="eyebrow">04 &mdash; Problems</p>
      <h2 style="color:#F4F2ED">感情AIを使いたい企業の、3つの壁</h2>
      <p class="lead" style="color:var(--ink-dim)">感情を扱う機能を自社のサービスや組織に取り入れたい。そう考えた企業が実際にぶつかるのは、この3つです。</p>
    </header>
    <ul class="rows wide">
      <li class="reveal">
        <div><span class="meta">01 ／ 合わない</span></div>
        <div class="body">
          <h3>場面ごとに、必要な感情もデータも精度も違う。</h3>
          <p>汎用の道具では目的に合わず、専用に作るにはデータと専門知識が要ります。どの技術をどう組み合わせるかの判断が、社内では難しい。</p>
        </div>
      </li>
      <li class="reveal">
        <div><span class="meta">02 ／ 揺れる</span></div>
        <div class="body">
          <h3>汎用の大規模言語モデルは、結果が揺れる。</h3>
          <p>実行ごとに判定が変わり、確からしさも分かりません。重要な判断の根拠にしにくく、品質を保証できません。</p>
        </div>
      </li>
      <li class="reveal">
        <div><span class="meta">03 ／ 危うい</span></div>
        <div class="body">
          <h3>感情の推定を誤ると、人を傷つける。</h3>
          <p>用途によっては規制の対象にもなります（EUのAI規則は、感情認識を用途に応じて禁止・規制しています）。社内に判断できる人材がいないことが、導入をためらわせます。</p>
        </div>
      </li>
    </ul>
  </div>
</section>"""

HOME_VISION = rows([
    ("01", "見落とされない。",
     "相談の奥にある苦しさが、定型的な返答で流されない。確信が低いときは「わからない」と示し、人の判断へ渡す。"),
    ("02", "噛み合う。",
     "対話AIが、顧客の怒りや不安を読み落とさない。読み取った感情に対して、次の一手を返す。"),
    ("03", "取りこぼさない。",
     "少数言語、小規模な領域、聞こえにくい人。採算に合わないとして切り捨てられてきた場所にも届く。"),
    ("04", "偽られない。",
     "盛り上がりを演出するために感情を捏造しない。測れていないことは、測れていないと示す。"),
]) + """
    <div class="measure-wide reveal" style="margin-top:2.5rem">
      <p class="lead">この状態を、特定の業界だけでなく、暮らしのあらゆる場面で当たり前にする。それが私たちの言う<strong>感情最適化された時代</strong>です。感情AIを社会へ広げることが、その手段になります。</p>
      <p style="margin-top:1.6rem"><a class="btn btn-ghost" href="vision.html">ビジョンを詳しく見る <span class="arw">&rarr;</span></a></p>
    </div>"""

HOME_ENGAGE = """    <div class="pipeline reveal">
      <div class="pstep"><p class="k">01 Talk</p><h4>相談</h4><p>現場の課題と、扱えるデータの範囲を伺います。感情AIが向かない場合は、そうお伝えします。</p></div>
      <div class="pstep"><p class="k">02 Design</p><h4>設計</h4><p>どの感情をどう測り、何を返すかを決めます。小さく始める範囲を定めます。</p></div>
      <div class="pstep accent"><p class="k">03 PoC</p><h4>実証</h4><p>限られた範囲で試し、現場にとって有用かを確かめます。</p></div>
      <div class="pstep"><p class="k">04 Deploy</p><h4>導入</h4><p>既存のシステムへ組み込み、運用に合わせて調整します。</p></div>
    </div>"""

HOME_RESEARCH = """    <div class="measure-wide reveal">
      <p class="lead">技術の土台は、代表が査読誌・国際会議で発表している研究です。論文、受賞、研究助成、研究テーマの一覧は、研究グループのサイトにまとめています。</p>
    </div>
    <div class="cards c2" style="margin-top:2.5rem">
      <article class="card reveal">
        <p class="no">Research</p>
        <h3>Affectosphere Group</h3>
        <p>研究グループのサイト。論文・受賞・研究助成・メンバー・研究テーマを掲載しています。</p>
        <p class="sublabel"><a class="link-amber" href="https://lab.affectosphere.group/" target="_blank" rel="noopener">研究グループサイトを見る &#8599;</a></p>
      </article>
      <article class="card reveal">
        <p class="no">News</p>
        <h3>Affectosphere News</h3>
        <p>感情AIの動向と、日々の発信をまとめたニュースサイト。</p>
        <p class="sublabel"><a class="link-amber" href="https://news.affectosphere.group/" target="_blank" rel="noopener">ニュースサイトを見る &#8599;</a></p>
      </article>
    </div>"""

HOME_FOUNDER = """    <div class="founder reveal">
      <div class="ava photo"><img src="img/keito-inoshita.webp" alt="井下 敬翔" width="582" height="420" loading="lazy"></div>
      <div>
        <h3>井下 敬翔 <small>Keito Inoshita</small></h3>
        <p class="role">Founder</p>
        <p>感情AIと自然言語処理の研究者。感情を確率分布・不確実性として扱う研究を、査読誌・国際会議で発表。Affectosphere時代に感情AIを社会へ普及させ、人の暮らしを最適化する：その実現のためにAffectosphereを立ち上げる。</p>
      </div>
    </div>"""


def build_home():
    body = "\n\n".join([
        HERO,
        sec("01", "Vision", "感情最適化された時代を、つくる。",
            "感情が社会を満たす環境になったいま、それを正しく扱えるかどうかで、暮らしの質が変わります。私たちが目指すのは、一つひとつの場面で感情が正しく扱われている状態です。",
            HOME_VISION),
        sec("02", "Concept", "感情が社会を満たす時代に、その環境を扱う感情AIを。", None,
            HOME_CONCEPT, band="cream"),
        sec("03", "What We Do", "他社のサービスと組織の「感情の部分」を担う。",
            "自社で最終サービスを作るのではなく、他社のサービスや組織の<strong>感情を扱う部分</strong>を引き受けます。場面ごとに適した感情AIを選び、組み合わせ、必要なら作る：一つの製品ではなく、感情AIの研究開発力そのものを提供するのが私たちの事業です。",
            HOME_WHAT),
        HOME_PROBLEMS,
        sec("05", "How to Start", "はじめかた。",
            "小さく試してから広げます。最初のご相談から導入まで、4つの段階で進めます。",
            HOME_ENGAGE),
        sec("06", "Research", "研究の裏付けは、グループサイトに。", None,
            HOME_RESEARCH, band="cream"),
        sec("07", "Founder", "代表", None, HOME_FOUNDER),
        contact_block("Affectosphere時代を、一緒に。",
                      "導入のご相談、共創・受託、取材など、お気軽にご連絡ください。"),
    ])
    page("index.html",
         "Affectosphere &mdash; 感情AIを社会へ広げ、生活を最適化する",
         "Affectosphereは、他社のサービスや組織の「感情の部分」を担う感情AIの会社です。場面別の設計・実装と受託研究開発、感情基盤モデルの提供、感情データ、評価・監査と倫理教育まで。",
         body, current="index.html")


# ── Affectosphere（旧 概念。事業の視点を足したもの） ────────────────────────
AFF_WHAT = """    <div class="figrow reveal">
      <div class="measure">
        <p class="lead">感情は、個人の内面を超えて、言葉・声・行動として社会のあらゆる場所にあふれました。SNS、対話AI、音声、行動ログ：やり取りの大半がデジタルに移り、感情の痕跡が社会に満ちています。</p>
        <p class="lead" style="margin-top:1.1rem">感情は、個人の属性から<strong>社会を満たす環境</strong>へと変わりました。私たちはこの環境を <strong>Affectosphere（情動圏）</strong> と呼び、これを測り、理解し、活かす層を事業領域としています。</p>
      </div>
      <div class="fig"><img src="img/aff-analysis.webp" alt="社会にあふれる感情のデータを読み解く様子の図" width="1024" height="1024" loading="lazy"></div>
    </div>"""

AFF_STEPS = rows([
    ("01", "感情は環境になった",
     "SNS・対話・音声・行動……感情のデータが社会を満たす。けれど、まだ正しく測られ・活かされていない。"),
    ("02", "感情AIが、その層を担う",
     "感情は曖昧で割れる。だから確率分布と不確実性のまま測り、理解し、表現し、活かす技術が要る。"),
    ("03", "暮らしが最適化される",
     "現場ごとに感情が活きることで、見落としが減り、対話が噛み合い、人の暮らしと社会がより良くなる。"),
])

AFF_FLOW = """    <div class="flow reveal">
      <div class="layer">
        <p class="k">Environment</p>
        <p class="t">Affectosphere ／ 情動圏</p>
        <p class="s">感情が、社会のあらゆる場所を満たす環境になった</p>
      </div>
      <p class="arrow">&darr; 感情AIが、測り・理解し・活かす &darr;</p>
      <div class="layer accent">
        <p class="k">AC・CAI ／ 私たちの役割</p>
        <p class="t">曖昧さを保ったまま、感情を扱う</p>
        <div class="chips"><span class="chip">測る・理解する</span><span class="chip">表現・受け渡す</span><span class="chip">活かす・最適化する</span></div>
      </div>
      <p class="arrow">&darr; 暮らしと事業へ &darr;</p>
      <div class="layer">
        <p class="k">Outcome</p>
        <p class="t">感情最適化された暮らし</p>
        <p class="s">対話・医療・教育・エンタメ・公共：あらゆる現場がより良くなる</p>
      </div>
      <p class="arrow">&#8635; より良い暮らしが、ふたたび情動圏を豊かにする</p>
    </div>"""

AFF_MARKET = cards3([
    ("01", "接点が増えた",
     "顧客対応、対話AI、学習支援、医療介護、公共の窓口。人の気持ちが関わる業務の多くがデジタルのやり取りに移り、感情を扱える範囲がそのまま広がりました。"),
    ("02", "測れるようになった",
     "多タスク・多言語を一つで扱う基盤モデルと、不確実性を扱う手法が実用の域に入りました。領域ごとに専用モデルを作らずに届けられます。"),
    ("03", "要件になった",
     "感情データの扱いは社会的な論点です。較正された確率とプライバシー設計を示せるかどうかが、導入の判断を左右します。"),
]) + """
    <div class="measure-wide reveal" style="margin-top:2.5rem">
      <p class="note">感情AIの市場は、2024年の27.4億ドルから2030年に90.1億ドルへ成長すると見込まれています（MarketsandMarkets）。カメラ・マイクを備えたAIグラスの広がりで、文章以外から感情を読み取る環境も整いつつあります。</p>
    </div>"""

AFF_BIZ = rows([
    ("Engineering", "場面別の感情AIの設計・実装／受託研究開発",
     "目的の整理 &rarr; 技術の選定・組み合わせ &rarr; 試作 &rarr; 評価 &rarr; 組み込み。文章に加えて、視線・映像・音声を用いた計測の研究開発も進めています。"),
    ("Foundation Model", "感情基盤モデルの提供",
     "多様な感情タスクを一つで扱う感情基盤モデル <strong>Affeline</strong>。研究用・非商用のライセンスで Hugging Face に公開しているほか、商用利用のライセンスとAPIの形でご提供します。"),
    ("Data", "感情データの分析・作成",
     "注釈者間の不一致の分析、受け取り方の割れが分かる感情データの作成と提供。お手元のデータの分析も承ります。"),
    ("Assurance", "評価・監査と倫理教育",
     "感情AIの判定の偏りや妥当性の検証、導入前の点検、企業・開発者向けの感情AI倫理教育。"),
    ("Outreach", "普及活動",
     "メディア活動・書籍・セミナー、展示会での感情AIアートの展示。ここで得た認知と信頼を、技術のご相談につなげます。"),
], wide=True) + """
    <p class="reveal" style="margin-top:2.5rem"><a class="btn btn-ghost" href="technology.html">技術とできることを見る <span class="arw">&rarr;</span></a></p>"""

AFF_PILLARS = cards3([
    ("01", "遍在性", "感情は、社会のあらゆる場所を満たしている。"),
    ("02", "測定性", "その感情を、曖昧さごと測り、理解する。"),
    ("03", "最適化", "測って活かし、人の暮らしと社会をより良くする。"),
])


def build_affectosphere():
    body = "\n\n".join([
        head_section("Affectosphere",
                     "感情が社会を満たす環境を、事業の対象に。",
                     "感情は個人の内面にとどまらず、社会を満たす環境になりました。その環境を Affectosphere（情動圏）と呼び、これを測り、活かす層を私たちの事業領域としています。"),
        sec("01", "Affectosphere", "情動圏とは。", None, AFF_WHAT),
        sec("02", "The Story", "3つの段階。", None, AFF_STEPS, band="cream"),
        sec("03", "Structure", "環境から、暮らしへ。",
            "情動圏を感情AIが測り、理解し、活かすことで、暮らしが最適化される。そしてより良い暮らしが、ふたたび情動圏を豊かにします。",
            AFF_FLOW),
        sec("04", "Market", "事業機会としての情動圏。",
            "感情を扱う技術が、いま事業として成り立つ条件がそろいました。理由は3つです。",
            AFF_MARKET, band="cream"),
        sec("05", "Our Business", "私たちの事業領域。",
            "自社で最終サービスは作りません。他社のサービスや組織の「感情の部分」を担う形で、5つの活動を行います。",
            AFF_BIZ),
        sec("06", "Pillars", "3つの見方。", None, AFF_PILLARS, band="cream"),
        contact_block("この時代を、一緒に。",
                      "事業のご相談、共創・取材など、お気軽にご連絡ください。"),
    ])
    page("affectosphere.html",
         "Affectosphere &mdash; 情動圏という事業領域 ｜ Affectosphere",
         "感情は個人の属性から社会を満たす環境へ変わりました。Affectosphere（情動圏）という捉え方と、その環境を扱う事業領域・事業機会を示します。",
         body, current="affectosphere.html")


# ── Technology（AC・CAI の説明＋できること） ────────────────────────────────
TECH_AC = """    <div class="figrow reveal">
      <div class="measure">
        <p class="lead">ACの要点は、何を感じているかを一つに言い当てることではなく、どう受け取られうるかの幅を含めて扱うことです。同じ一文でも、読む人によって温かみと皮肉に割れます。その割れを潰さずに返すほうが、現場の判断には役立ちます。</p>
        <p class="lead" style="margin-top:1.1rem">Affectosphereは、ACの中核を<strong>感情基盤モデル</strong>として実装しています。極性・離散感情・皮肉・攻撃性・強度・側面別感情・共感などを、多言語で一つのモデルが扱います。</p>
      </div>
      <div class="fig"><img src="img/ac.webp" alt="感情計算（Affective Computing）の様子の図" width="1024" height="1024" loading="lazy"></div>
    </div>"""

TECH_CAI_WHAT = """    <div class="figrow flip reveal">
      <div class="measure">
        <p class="lead">ACの実装は「知覚（感情を検出する）」に偏りがちです。しかし、感情を社会で本当に活かすには、感じ取り、内に保ち、推し量り、表し、やりとりし、ふるまいを律する：という一連の力が要ります。</p>
        <p class="lead" style="margin-top:1.1rem">CAIは、この全体を6つの能力として定義し、何ができていて、何が足りないのかを見通せるようにする地図です。Affectosphereは、知覚に留まらず、この地図の全域に事業機会を見ています。</p>
      </div>
      <div class="fig"><img src="img/cai.webp" alt="感情を扱うAIの内部を観察する様子の図" width="1024" height="1024" loading="lazy"></div>
    </div>"""

TECH_ABILITIES = rows([
    ("01 Perception", "知覚",
     "感情を観測し、測定する力。Affectosphereは感情を<b>点ではなく確率分布</b>で捉え、<b>本質的な曖昧さとモデルの迷いを分離</b>して返します。感情基盤モデルが担う中核で、事業の接点も最も多い能力です。"),
    ("02 Representation", "表象",
     "感情を内部に<b>保ち、受け渡す</b>力。曖昧さを潰さずに表現し、人とAI・人と人のあいだで気持ちを伝える。既存サービスが最も手薄な領域であり、私たちが重視する機会です。"),
    ("03 Reasoning", "推論",
     "文脈から感情の<b>原因や推移を推し量る</b>力。なぜその感情が生じたのか、次にどう変化しうるかを、根拠とともに扱います。"),
    ("04 Generation", "生成",
     "感情を<b>表し、生み出す</b>力。状況に応じた適切な感情表現を、押し付けでなく設計可能な形で生成します。"),
    ("05 Interaction", "相互作用",
     "人とAIが感情を<b>やりとりする</b>力。読み取った感情に対して、行動推奨など<b>次の一手</b>を返し、対話や体験を噛み合わせます。"),
    ("06 Control", "制御",
     "感情的なふるまいを<b>律する</b>力。過度に迎合しない、不確実なときは控える：安全で誠実な振る舞いを設計要件に据えます。"),
], accent=True)

TECH_PIPELINE = """    <div class="pipeline reveal">
      <div class="pstep"><p class="k">Input</p><h4>現場の入力</h4><p>テキスト・音声・行動など、作業前や対話の中で得られる情報。</p></div>
      <div class="pstep accent"><p class="k">Foundation Model</p><h4>感情基盤モデル</h4><p>多タスク・多言語を1モデルで。較正された推論を行う中核。</p></div>
      <div class="pstep"><p class="k">Output</p><h4>分布・不確実性・行動</h4><p>感情の確率分布＋曖昧さの分離＋次の行動推奨。</p></div>
      <div class="pstep"><p class="k">Field</p><h4>現場の判断へ</h4><p>人の判断を代替せず、見落としを減らす材料として届ける。</p></div>
    </div>"""

TECH_CORE = rows([
    ("Foundation Model", "感情基盤モデル",
     "極性・離散感情・皮肉・攻撃性・強度・側面別感情・共感などを、<b>多言語で一つのモデル</b>が扱います。用途ごとに専用モデルを作る必要がなく、<b>データの少ない領域にも軽い適応</b>で届く：従来の個別開発では難しかった展開を可能にします。"),
    ("Uncertainty", "不確実性の定量化",
     "<b>本質的な曖昧さ（aleatoric）</b>と<b>モデルの迷い（epistemic）</b>を数理的に分離して返します。MCMCに基づく事後分布から較正された不確実性を得る：この手法は代表の査読研究に基づきます。自信がないときは「わからない」と正直に示せるのが要です。"),
    ("Calibration", "較正",
     "出力される確率が、実際の確からしさと一致するように較正します。汎用LLMの「0.8」が本当に80%を意味しない問題を避け、<b>現場で意思決定に使える数値</b>にします。"),
    ("Multilingual", "多言語・ロングテール",
     "少数言語・小規模領域など、採算が合わず切り捨てられてきた<b>感情のロングテール</b>に、一つの基盤モデルから届きます。やさしい日本語を含む多言語に対応していきます。"),
    ("Evaluation", "評価と基準",
     "感情AIの評価指標（REACH・VEIL・TILT）を研究として公開し、<b>測り方の共通語</b>をつくります。誰もが同じものさしで質を測れることが、市場全体の信頼につながります。"),
    ("By Design", "設計原則",
     "顔を撮らない・個人を特定しない測り方を選べます。<b>不確実性を正直に示す／人の判断を代替しない</b>：倫理を後付けでなく設計要件に据えます。"),
], wide=True, accent=True)

TECH_CAPS = cards3([
    ("01", "感情を「分布」で返す",
     "怒り0.82のような点ではなく、較正された確率分布（例：温かみ38%・無関心31%・皮肉23%・怒り8%）で返す。受け取られ方の割れが見える。",
     "AC ／ CAI 知覚"),
    ("02", "曖昧さとAIの迷いを分離",
     "「言葉そのものが曖昧なのか（aleatoric）」「モデルが迷っているのか（epistemic）」を別の数値で返す。自信がないときは正直に示す。",
     "AC ／ CAI 知覚"),
    ("03", "多タスク・多言語を1モデルで",
     "極性・離散感情・皮肉・攻撃性・強度・側面別感情・共感などを、多言語で1つの基盤モデルが扱う。データの少ない領域にも軽い適応で届く。",
     "AC ／ 基盤モデル"),
    ("04", "次の行動を返す",
     "感情を返して終わりではなく、顧客が設定したルールに基づき「次にとるべき行動（例：有人対応へエスカレーション）」を返す。",
     "CAI 相互作用"),
    ("05", "モダリティ間の不一致を検出",
     "テキストで「大丈夫」、音声でフラストレーション：その食い違いを数値化します。テキストに加えて、視線・映像・音声からの計測にも対応を広げています。",
     "AC ／ マルチモーダル"),
    ("06", "個人を特定しない測り方",
     "組織や会場など多人数を対象とする場合も、個人を特定せず集団レベルで推定する設計を選べます。監視ではなく、包摂と改善のための測定です。",
     "AC ／ 集団推定"),
])

USECASES = [
    ("Marketing", "顧客理解・マーケティング", "business-flat",
     "口コミや問い合わせの感情が、肯定・否定など数段階にしか分けられない。",
     "感情の<b>内訳と確からしさ</b>を分布で返し、皮肉や不満の混ざり方まで見える形にする。"),
    ("CX / Chatbot", "対話AI・カスタマーサポート", "human-ai-interaction-flat",
     "汎用LLMの判定が実行ごとに揺れ、応答の品質を保証できない。",
     "較正された感情の分布と<b>行動推奨</b>を返し、「怒っている顧客は有人対応へ」など<b>次の一手</b>の判断材料にできる。"),
    ("Workplace", "社内のコミュニケーション・組織づくり", "data-augmentation-flat",
     "組織の状態を知りたいが、個人の監視になってしまう設計は使えない。",
     "本人の同意を得た社内アンケートなどから、<b>個人を特定せず集団レベル</b>で状態を推定する設計を採れる。"),
    ("Care", "医療・福祉・相談支援", "emotion-recognition-flat",
     "相談文や会話の奥にある不安・痛みの兆候が埋もれ、誤りが許されない。",
     "感情を<b>較正された確率</b>で示し、確信が低いときは「わからない」と返す。断定せず、<b>専門職の判断を補助</b>する道具として設計。"),
    ("Education", "教育・学習支援", "human-emotion-understanding-flat",
     "学びの場の戸惑いや意欲が、言葉にならず見えない。",
     "やり取りの感情を<b>曖昧さを保ったまま</b>捉え、つまずきや関心の変化を支援者が汲み取りやすくする。"),
    ("Venue", "店舗・展示・エンタメ", "application-development-flat",
     "来場者の反応を知りたいが、文章以外（視線・表情・声）の計測が必要になる。",
     "来場者の反応の把握と体験の設計を支える。文章に加えて<b>視線・映像・音声</b>の計測にも対応し、展示の現場で検証しながら届けます。"),
    ("Public", "地域・行政", "ethics-philosophy-flat",
     "問い合わせや声の感情が、件数としてしか扱われない。",
     "市民の声の感情を<b>多言語</b>で分布として捉え、やさしい日本語での応対や、見落としの少ない窓口対応を支える。"),
]
TECH_USECASES = "    <ul class=\"usecases\">\n" + "\n".join(
    f"""      <li class="reveal">
        <div class="uc-fig"><img src="img/{img}-800.webp" alt="" aria-hidden="true" width="800" height="800" loading="lazy"></div>
        <div class="uc-body">
          <p class="meta">{k}</p>
          <h3>{ja}</h3>
          <p class="before">{before}</p>
          <p class="after">{after}</p>
        </div>
      </li>""" for k, ja, img, before, after in USECASES) + "\n    </ul>"

TECH_OFFER = """    <div class="cards c2">
      <article class="card reveal"><p class="no">A</p><h3>場面別の設計・実装（受託研究開発）</h3><p>目的の整理 &rarr; 技術の選定・組み合わせ &rarr; 試作 &rarr; 評価 &rarr; 組み込み。一つの製品ではなく、感情AIの研究開発力そのものを場面ごとに提供します。</p></article>
      <article class="card reveal"><p class="no">B</p><h3>感情基盤モデルと感情APIの提供</h3><p>多様な感情タスクを一つで扱う感情基盤モデル Affeline。研究用・非商用のライセンスで公開するほか、商用利用のライセンスと、用途に合わせたAPIの形でご提供します。</p></article>
      <article class="card reveal"><p class="no">C</p><h3>評価・監査と倫理教育</h3><p>感情AIの判定の偏りや妥当性を検証します。導入前の点検、評価の設計、企業・開発者向けの感情AI倫理教育まで。</p></article>
      <article class="card reveal"><p class="no">D</p><h3>感情データの分析・作成</h3><p>注釈者間の不一致の分析、受け取り方の割れが分かる感情データの作成と提供。お手元のデータの分析も承ります。</p></article>
    </div>
    <p class="reveal" style="margin-top:2.5rem"><a class="btn btn-solid" href="contact.html">導入・PoCを相談する <span class="arw">&rarr;</span></a></p>"""

TECH_COMPARE = """    <div class="reveal">
      <table class="compare">
        <thead><tr><th>観点</th><th>汎用LLM／既存の感情AI</th><th>Affectosphere</th></tr></thead>
        <tbody>
          <tr><td>感情の出力</td><td class="them">点推定・数段階の分類</td><td class="us">較正された確率分布</td></tr>
          <tr><td>曖昧さ</td><td class="them">1つに合算</td><td class="us">本質的曖昧さ × 推定ブレを分離</td></tr>
          <tr><td>多タスク・多言語</td><td class="them">都度プロンプト／都度専用モデル</td><td class="us">1基盤モデルで統合・少数領域に強い</td></tr>
          <tr><td>次の行動</td><td class="them">返さない</td><td class="us">行動推奨を返す</td></tr>
          <tr><td>導入</td><td class="them">顧客任せ</td><td class="us">現場に合わせた応用支援込み</td></tr>
          <tr><td>倫理</td><td class="them">較正・プライバシーが曖昧</td><td class="us">不確実性を正直に・顔を撮らない選択肢</td></tr>
        </tbody>
      </table>
      <p class="note" style="margin-top:1.2rem">※ 性能・有用性は、各現場での検証を前提にお伝えします。</p>
    </div>"""

TECH_HONESTY = cards3([
    ("&#10003;", "示すこと",
     "何をどこまで測れているかを、能力ごとに示します。評価の方法と結果は、導入をご判断いただく前にお渡しします。"),
    ("&rarr;", "広げること",
     "視線・映像・音声への対応、より多くの言語・領域への展開を、現場での検証とあわせて進めています。"),
    ("!", "偽らないこと",
     "確信が低いときは「わからない」と示します。測れていないことを、測れたことにはしません。"),
]) + """
    <div class="measure-wide reveal" style="margin-top:2.5rem">
      <p class="lead">CAIの枠組みも、感情を分布と不確実性で扱う手法も、代表の査読研究に基づいています。論文・受賞・研究助成の一覧は <a class="link-amber" href="https://lab.affectosphere.group/" target="_blank" rel="noopener">研究グループサイト</a> にまとめています。私たちは、能力ごとに「どこまでできているか」を正直に示したうえでお引き受けします。</p>
    </div>"""


TECH_DATA = rows([
    ("01", "個人を特定しない選択肢",
     "顔を撮らない、個人を特定しない測り方を選べます。多人数を対象とする場合も、個人を特定せず集団レベルで推定する設計を採れます。"),
    ("02", "不確実なときは、そう返す",
     "確信が低いときは「わからない」と示します。確からしさを偽らないことを、出力の要件にしています。"),
    ("03", "人の判断を代替しない",
     "出力は判断材料です。最終的な判断と解釈は人に委ねる前提で、画面も運用も設計します。"),
    ("04", "扱う範囲は、導入ごとに取り決める",
     "対象とするデータの範囲、保存、利用の範囲は、導入のたびに明文化します。具体的な取り扱いは個別のご相談のうえ定めます。"),
])


def build_technology():
    body = "\n\n".join([
        head_section("Technology",
                     "ACとCAI：感情を扱う技術と、その地図。",
                     "事業の接点が多いのは <strong>Affective Computing（AC／感情計算）</strong>です。私たちはACを土台に据え、その全体像を示す枠組みとして <strong>CAI（計算論的感情知性）</strong>を用います。ここでは両者の説明と、具体的にできることを示します。"),
        sec("01", "Affective Computing", "AC：感情を測り、扱う技術。",
            "ACは、人の感情を計算機が測り、扱うための技術領域です。テキスト・音声・行動などに残る感情の痕跡を対象にします。顧客対応、対話AI、学習支援、医療介護、公共の窓口：事業の接点はこの層に集まります。",
            TECH_AC),
        sec("02", "CAI", "測るだけでは、足りない。",
            "CAI（Computational Affective Intelligence／計算論的感情知性）は、感情を扱うAIが備えるべき能力を体系化した枠組みです。代表の査読研究に基づき、Affectosphereのすべての技術は、この地図の上に設計されます。",
            TECH_CAI_WHAT, band="cream"),
        sec("03", "The Six Abilities", "CAI の6能力。",
            "それぞれの力の意味と、Affectosphereの取り組みを示します。事業としての接点が多いのは、ACが担う「知覚」です。",
            TECH_ABILITIES),
        sec("04", "Core Technology", "技術の中身。",
            "テキスト・音声・行動などの入力を、感情基盤モデルが処理し、分布・不確実性・行動推奨として返します。その中身を6つに分けて示します。",
            TECH_PIPELINE + "\n" + TECH_CORE, band="cream"),
        sec("05", "What We Can Do", "具体的に、できること。",
            "ACとCAIの能力を、使える機能として並べます。各項目に、ACとCAIのどこに当たるかを添えました。",
            TECH_CAPS),
        sec("06", "Use Cases", "現場で、こう活きる。",
            "同じ1つの基盤モデルを、現場の文脈に合わせて導入します。以下は想定する活用像です（有用性は各現場の検証を前提とします）。",
            TECH_USECASES, band="cream"),
        sec("07", "How We Deliver", "提供のかたち。",
            "単品のAPIから、現場に合わせた導入支援、受託・顧問まで。要望に合わせて選べます。",
            TECH_OFFER),
        sec("08", "Data &amp; Privacy", "データの扱い。",
            "感情データは、扱いが社会的な論点になっている領域です。私たちが設計上の前提にしていることを示します。",
            TECH_DATA, band="cream"),
        sec("09", "Why Affectosphere", "汎用AIでは、できないこと。", None, TECH_COMPARE),
        sec("10", "Honesty", "正直に、できることを示す。", None, TECH_HONESTY, band="cream"),
        contact_block("あなたの現場に、感情の正直な測りを。",
                      "導入のご相談、技術評価・PoC、共創・取材など、ご連絡ください。"),
    ])
    page("technology.html", "技術 &mdash; AC・CAIとできること ｜ Affectosphere",
         "Affective Computing（AC）とCAI（計算論的感情知性）の説明と、感情AIで具体的にできること。感情基盤モデル、不確実性の定量化、較正、多言語、活用事例、提供のかたちまで。",
         body, current="technology.html")


# ── Vision ──────────────────────────────────────────────────────────────────
VISION_WHYNOW = cards3([
    ("01", "感情が、環境になった",
     "やり取りの大半がデジタルに移り、感情の痕跡が社会に満ちた。測る対象が、個人から場へ。"),
    ("02", "技術が、追いついた",
     "多タスク・多言語を一つで扱う基盤モデルと、不確実性を扱う手法が成熟。ロングテールに届く。"),
    ("03", "倫理が、問われている",
     "感情データの扱いが社会的な論点に。正直さとプライバシーを設計に組み込む企業が求められる。"),
])

VISION_THESIS = """    <div class="figrow reveal">
      <div class="measure">
        <p class="lead">感情を件数やスコアとしてではなく、曖昧さを保った分布として正しく測り、現場ごとに活かす。すると、相談の奥の苦しさは見落とされにくくなり、対話は噛み合い、学びの戸惑いは汲まれ、ライブの一体感は誰も取りこぼしません。</p>
        <p class="lead" style="margin-top:1.1rem"><strong>一つひとつの場面で感情が正しく扱われること</strong>：その積み重ねが、暮らしと社会をより良くします。私たちはそれを「感情最適化された社会」と呼びます。</p>
      </div>
      <div class="fig"><img src="img/aff-personal.webp" alt="一人ひとりの感情が正しく扱われる様子の図" width="1024" height="1024" loading="lazy"></div>
    </div>"""

VISION_ROADMAP = """    <div class="roadmap">
      <div class="phase reveal"><p class="k">Now ／ 今</p><h3>現場へ届ける</h3><ul>
        <li>場面別の設計・実装と受託研究開発</li><li>感情基盤モデルと感情APIの提供</li>
        <li>感情データの分析・作成</li><li>評価・監査と倫理教育</li></ul></div>
      <div class="phase reveal"><p class="k">Next ／ 近未来</p><h3>広げる</h3><ul>
        <li>視線・映像・音声へ本格展開</li><li>感情の受け渡し（表象）の標準化</li>
        <li>多言語・少数領域への普及</li><li>より多くの現場・産業へ横展開</li></ul></div>
      <div class="phase reveal"><p class="k">Future ／ 将来</p><h3>社会の標準に</h3><ul>
        <li>感情が正しく扱われる社会インフラ</li><li>感情最適化された暮らしの常態化</li>
        <li>測り方の共通語が市場の基準に</li><li>CAIの全能力をカバー</li></ul></div>
    </div>"""

VISION_PROMISE = rows([
    ("01", "正直に測る。", "自信がないときは「わからない」と示し、演出のために感情を捏造しません。"),
    ("02", "取りこぼさない。", "少数言語・小規模・まれな状況。切り捨てられてきた誰かの気持ちに届きます。"),
    ("03", "人を代替しない。", "感情AIは、人の判断を支える道具。最終的な判断と解釈は、人に委ねます。"),
    ("04", "倫理を設計に。", "プライバシーと誠実さを、後付けでなく最初から設計に組み込みます。"),
])


def build_vision():
    body = "\n\n".join([
        head_section("Vision", "Affectosphere時代を、ひらく。",
                     "感情が社会を満たす環境になった時代に、感情AIを社会へ普及させ、暮らしを感情最適化する。私たちは、その時代をひらく中核でありたいと考えています。"),
        sec("01", "Why Now", "なぜ、いまなのか。",
            "SNS、対話AI、音声、行動ログ。感情は、個人の内面を超えて、社会のあらゆる場所にデータとしてあふれ出しました。感情は、個人の属性から<strong>社会を満たす環境</strong>へと変わったのです。一方で、それを曖昧さごと正しく測り、活かす技術はまだ整っていません。基盤モデルと不確実性の技術が成熟したいま、この環境を扱う準備が初めて整いました。",
            VISION_WHYNOW),
        sec("02", "The Thesis", "感情最適化された社会とは。", None, VISION_THESIS, band="cream"),
        sec("03", "Roadmap", "今 &rarr; 近未来 &rarr; 将来。",
            "段階を踏んで、感情AIを社会へ広げます（将来像は構想を含みます）。", VISION_ROADMAP),
        sec("04", "Our Promise", "私たちの約束。", None, VISION_PROMISE, band="cream"),
        contact_block("Affectosphere時代を、一緒に。",
                      "共創・導入・投資・取材など、この時代を一緒につくる仲間を探しています。"),
    ])
    page("vision.html", "ビジョン &mdash; Vision ｜ Affectosphere",
         "Affectosphere時代をひらく。感情が社会を満たす時代に、感情AIを普及させ、暮らしを感情最適化する。なぜ今か、ロードマップ、そして私たちの約束。",
         body, current="vision.html")


# ── Contact ─────────────────────────────────────────────────────────────────
CONTACT_TYPES = rows([
    ("導入・PoC", "", "感情AIを自社のプロダクトや業務に組み込みたい。まず小さく試したい。"),
    ("受託研究開発・技術顧問", "", "場面別の感情AIの設計・実装、評価・監査、導入設計の受託、技術顧問。"),
    ("講演・研修", "", "感情AI・AC・CAI・不確実性・AI倫理をテーマにした講演、社内勉強会。"),
    ("データ提供", "", "感情データの分析、受け取り方の割れが分かる感情データの作成・提供。"),
    ("共創・投資", "", "共同研究、実証（PoC）のご提案を歓迎します。一緒に時代をつくる相手を探しています。"),
    ("取材", "", "感情AI、CAI、Affectosphereという考え方についての取材。"),
])

CONTACT_FAQ = rows([
    ("Q 01", "汎用のLLMでは足りませんか。",
     "汎用LLMは感情を点推定で返し、出力される確率が実際の確からしさと一致しないことがあります。私たちは較正された確率分布と、曖昧さの分離を返します。要件によっては汎用LLMで足りる場合もあるため、まず現場のご事情を伺います。"),
    ("Q 02", "どんなデータが必要ですか。",
     "テキストが中心です。視線・映像・音声にも対応を広げています。既存のやり取りの記録があれば、小さな範囲から始められます。"),
    ("Q 03", "日本語以外でも使えますか。",
     "多言語を一つの基盤モデルで扱います。やさしい日本語を含め、対応する範囲を広げていきます。"),
    ("Q 04", "顔を撮らずに使えますか。",
     "個人を特定しない測り方を重視しています。多人数を対象とする場合も、個人を撮らずに集団レベルで推定する設計を採れます。"),
    ("Q 05", "まず何から始められますか。",
     "限られた範囲のPoCから始めるのが確実です。相談・設計・実証・導入の4段階で進めます。"),
    ("Q 06", "どんな技術が土台になっていますか。",
     "代表が査読誌・国際会議で発表している感情AIの研究が土台です。感情基盤モデルは公開済みで、商用利用のライセンスとAPIの形でご提供します。性能・有用性は、各現場での検証を前提にお伝えします。"),
    ("Q 07", "EUのAI規則など、規制面はどうなりますか。",
     "感情認識は用途に応じて禁止・規制の対象です。導入の可否と設計上の制約の整理を、評価・監査の一環として行います。"),
])

CONTACT_ROUTE = f"""    <div class="formcard reveal">
      <h3>お問い合わせフォーム</h3>
      <p class="note">お問い合わせは、研究グループサイトのフォームでまとめて受け付けています。企業からのご相談も、同じ窓口に届きます。</p>
      <p style="margin-top:1.75rem"><a class="btn btn-solid" href="{GROUP_CONTACT}" target="_blank" rel="noopener">お問い合わせフォームへ <span class="arw">&#8599;</span></a></p>
      <p class="note" style="margin-top:1.75rem">ご用件（導入・PoC ／ 受託研究開発・技術顧問 ／ 講演・研修 ／ データ提供 ／ 共創・投資 ／ 取材）を書き添えていただくと、お返事が早くなります。</p>
    </div>
    <div class="measure-wide reveal" style="margin-top:2.5rem">
      <p class="note">研究の内容については <a class="link-amber" href="https://lab.affectosphere.group/" target="_blank" rel="noopener">研究グループサイト</a>、日々の発信については <a class="link-amber" href="https://news.affectosphere.group/" target="_blank" rel="noopener">ニュースサイト</a> もご覧ください。</p>
    </div>"""


def build_contact():
    body = "\n\n".join([
        head_section("Contact", "お問い合わせ。",
                     "導入のご相談、受託・技術顧問、講演、共創・投資、取材まで、広く受け付けています。研究グループサイトのお問い合わせフォームからご連絡ください。"),
        sec("01", "What We Hear", "こんなご相談を受けています。", None, CONTACT_TYPES),
        sec("02", "FAQ", "よくあるご質問。", None, CONTACT_FAQ, band="cream"),
        sec("03", "Contact", "お問い合わせフォームへ。", None, CONTACT_ROUTE),
        contact_block("Affectosphere時代を、一緒に。",
                      "お返事は、代表の井下から直接お送りします。"),
    ])
    page("contact.html", "お問い合わせ &mdash; Contact ｜ Affectosphere",
         "Affectosphere へのお問い合わせ。導入・PoC、受託・技術顧問、講演・研修、共創・投資、取材など、広く受け付けています。",
         body, current="contact.html")


# ── Company ─────────────────────────────────────────────────────────────────
COMPANY_PROFILE = """    <ul class="rows wide">
      <li class="reveal">
        <div><span class="meta">社名</span></div>
        <div class="body"><p>Affectosphere</p></div>
      </li>
      <li class="reveal">
        <div><span class="meta">代表者</span></div>
        <div class="body"><p>井下 敬翔（Keito Inoshita）</p></div>
      </li>
      <li class="reveal">
        <div><span class="meta">事業内容</span></div>
        <div class="body">
          <ul class="plain">
            <li>場面別の感情AIの設計・実装／受託研究開発</li>
            <li>感情基盤モデルと感情APIの提供</li>
            <li>感情データの分析・作成</li>
            <li>感情AIの評価・監査、企業・開発者向けの倫理教育</li>
            <li>講演・研修、執筆、展示を通じた感情AIの普及</li>
          </ul>
        </div>
      </li>
      <li class="reveal">
        <div><span class="meta">技術領域</span></div>
        <div class="body"><p>感情AI（Affective Computing）、計算論的感情知性（CAI）、自然言語処理、不確実性の定量化。</p></div>
      </li>
      <li class="reveal">
        <div><span class="meta">お問い合わせ</span></div>
        <div class="body"><p><a class="link-amber" href="%s" target="_blank" rel="noopener">お問い合わせフォーム &#8599;</a></p></div>
      </li>
    </ul>""" % GROUP_CONTACT

COMPANY_FOUNDER = """    <div class="founder reveal">
      <div class="ava photo"><img src="img/keito-inoshita.webp" alt="井下 敬翔" width="582" height="420" loading="lazy"></div>
      <div>
        <h3>井下 敬翔 <small>Keito Inoshita</small></h3>
        <p class="role">Founder</p>
        <p>感情AIと自然言語処理の研究者。関西大学大学院商学研究科 博士課程後期課程に在籍し、感情を確率分布・不確実性として扱う研究を査読誌・国際会議で発表しています。感情AIの能力を体系化した枠組み（CAI）と、多タスク・多言語を一つで扱う感情基盤モデルが、この事業の土台です。</p>
        <p style="margin-top:1.2rem"><a class="link-amber" href="https://lab.affectosphere.group/" target="_blank" rel="noopener">論文・受賞・研究助成の一覧（研究グループサイト） &#8599;</a></p>
      </div>
    </div>"""

COMPANY_SITES = """    <div class="cards c2">
      <article class="card reveal">
        <p class="no">Research</p>
        <h3>Affectosphere Group</h3>
        <p>研究グループのサイト。論文・受賞・研究助成・メンバー・研究テーマを掲載しています。</p>
        <p class="sublabel"><a class="link-amber" href="https://lab.affectosphere.group/" target="_blank" rel="noopener">研究グループサイトを見る &#8599;</a></p>
      </article>
      <article class="card reveal">
        <p class="no">News</p>
        <h3>Affectosphere News</h3>
        <p>感情AIの動向と、日々の発信をまとめたニュースサイト。</p>
        <p class="sublabel"><a class="link-amber" href="https://news.affectosphere.group/" target="_blank" rel="noopener">ニュースサイトを見る &#8599;</a></p>
      </article>
    </div>"""


def build_company():
    body = "\n\n".join([
        head_section("Company", "会社概要。",
                     "Affectosphereは、他社のサービスや組織の「感情の部分」を担う感情AIの会社です。場面ごとに適した感情AIを選び、組み合わせ、必要なら作ります。"),
        sec("01", "Profile", "会社概要。", None, COMPANY_PROFILE),
        sec("02", "Founder", "代表。", None, COMPANY_FOUNDER, band="cream"),
        sec("03", "Related Sites", "関連サイト。",
            "研究の成果と日々の発信は、別のサイトにまとめています。", COMPANY_SITES),
        contact_block("Affectosphere時代を、一緒に。",
                      "導入のご相談、受託研究開発、講演、共創・投資、取材まで、広く受け付けています。"),
    ])
    page("company.html", "会社概要 &mdash; Company ｜ Affectosphere",
         "Affectosphere の会社概要。代表者、事業内容、技術領域、関連サイト、お問い合わせ窓口。",
         body, current="company.html")


def build_thanks():
    body = """<section class="surface-ink">
  <div class="ink-grid" aria-hidden="true"></div>
  <div class="wrap page-head">
    <p class="eyebrow">Thank you</p>
    <h1>お問い合わせ、ありがとうございます。</h1>
    <p class="lead">内容を確認のうえ、通常 2&ndash;3 営業日以内にご返信します。しばらくお待ちください。</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <p><a class="btn btn-ghost" href="index.html">ホームへ戻る <span class="arw">&rarr;</span></a></p>
  </div>
</section>"""
    page("thanks.html", "送信しました ｜ Affectosphere",
         "お問い合わせを受け付けました。", body)


def build_redirects():
    redirect("concept.html", "affectosphere.html",
             "移動しました ｜ Affectosphere",
             "「概念」のページは Affectosphere ページになりました。")
    redirect("cai.html", "technology.html",
             "移動しました ｜ Affectosphere",
             "CAI の説明は「技術」ページに入りました。")
    redirect("solutions.html", "technology.html",
             "移動しました ｜ Affectosphere",
             "「できること」の内容は「技術」ページに入りました。")


if __name__ == "__main__":
    build_home()
    build_affectosphere()
    build_technology()
    build_vision()
    build_contact()
    build_company()
    build_thanks()
    build_redirects()
