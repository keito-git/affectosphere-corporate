# Affectosphere — corporate site

The company site for Affectosphere: a static site of hand-written HTML and one
hand-written stylesheet. No framework, no build step. Netlify publishes the
repository root as-is.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | Home: vision, what we do, the three barriers, how to start, research, founder |
| `affectosphere.html` | The Affectosphere (情動圏) framing and the business areas |
| `vision.html` | Why now, the thesis, the roadmap, our promises |
| `technology.html` | AC and CAI, the six abilities, capabilities, use cases, delivery, data handling |
| `contact.html` | What we hear, FAQ, and the hand-off to the enquiry form |
| `company.html` | Company profile, founder, related sites |
| `thanks.html` | Form thank-you page (kept, currently unlinked) |
| `concept.html`, `cai.html`, `solutions.html` | Redirect stubs for retired URLs |
| `style.css` | The whole design system |
| `js/` | Hero WebGL town scene, hero dashboards, site behaviour |
| `img/`, `hero/` | Illustrations, the founder portrait, the hero poster fallback |
| `og/` | Open Graph cards, one per page |
| `robots.txt`, `sitemap.xml` | Generated alongside the pages |
| `tools/gen_corporate.py` | Generates every HTML file, plus robots.txt and sitemap.xml |
| `tools/gen_og.py` | Renders the Open Graph cards with headless Chrome |

## Editing

The HTML files are generated. Edit the copy in `tools/gen_corporate.py`, then:

```sh
python3 -I tools/gen_corporate.py
```

It rewrites every page in place. Edit the HTML directly only for a one-off
experiment, and fold the change back into the generator afterwards.

`style.css` is maintained by hand and is not generated.

The Open Graph cards are rendered separately, and only need re-running when a
page title changes:

```sh
python3 -I tools/gen_og.py
```

## Domain

The canonical host is `https://affectosphere.group`. `www` is redirected to it
in `netlify.toml`. Changing the host means changing `SITE` in
`tools/gen_corporate.py`, `HOST` in `tools/gen_og.py`, and the redirect.

## Enquiries

The site has no form and no email address on it. Every contact route points at
the research group's enquiry form at <https://lab.affectosphere.group/contact/>.
