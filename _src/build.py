"""Builds the namlabs pages that come in English, Vietnamese and Japanese.

    python3 _src/build.py

Writes the home page, the Sudoku and Sky Hop pages, a page for each game in
stores.GAMES (text read from the game repo's Play listing; set NAMLABS_REPOS if
the repos aren't in /home/namth/Development), the Sudoku guide and the technique
articles for every language, then refreshes sitemap.xml. The
privacy policies and other hand-written pages are left alone.
"""
import datetime
import json
import pathlib
import re

from diagrams import DIAGRAMS
import en
import ja
import vi
from stores import GAMES, IOS, IOS_LIVE, listing

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://namlabs.dev'
TODAY = datetime.date.today().isoformat()
TEXT = {'en': en.T, 'vi': vi.T, 'ja': ja.T}
PLAY = 'https://play.google.com/store/apps/details?id=com.namlabs.'
TECHS = ('naked-single', 'hidden-single', 'naked-pairs', 'pointing-pairs', 'x-wing')
ORG = {'@id': f'{SITE}/#org', '@type': 'Organization', 'name': 'namlabs', 'url': f'{SITE}/'}
PLAY_ICON = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="play" '
             'viewBox="0 0 24 24"><path fill="currentColor" d="M4 2.8v18.4c0 .9 1 1.4 1.7.9l15.5-9.2a1 1 0 0 0 '
             '0-1.8L5.7 1.9C5 1.4 4 1.9 4 2.8Z"/></symbol></svg>')
PAGES = []  # (path, lastmod) for the sitemap


def href(lang, path=''):
    """Site-relative link to [path] in [lang]; English lives at the root."""
    return '/' + ('' if lang == 'en' else f'{lang}/') + path


def play(app, lang):
    return PLAY + app + ('' if lang == 'en' else f'&amp;hl={lang}')


def shot(game, lang, n):
    return f'/img/{game}/' + ('' if lang == 'en' else f'{lang}/') + f'shot-{n}.webp'


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def text(html):
    """Plain text of an HTML snippet, for meta tags and JSON-LD."""
    return re.sub(r'<[^>]+>', '', html).replace('&amp;', '&').replace('&nbsp;', ' ')


def ld(data):
    return ('<script type="application/ld+json">\n'
            + json.dumps({'@context': 'https://schema.org', **data}, ensure_ascii=False, indent=2)
            + '\n</script>')


def play_badge(lang):
    """Google's own localized "Get it on Google Play" badge, used as their guidelines ask."""
    code = {'en': 'en_us/badges/static/images/badges/en'}.get(lang, f'{lang}/badges/static/images/badges/{lang}')
    return f'https://play.google.com/intl/{code}_badge_web_generic.png'


def btn_play(app, lang, t, cls='play-badge'):
    # en's PNG has transparent padding on every side; vi and ja only above and below.
    return (f'<a class="{cls} {"pad" if lang == "en" else "tight"}" href="{play(app, lang)}"><img src="{play_badge(lang)}" '
            f'alt="{t["gp_badge_alt"]}" width="646" height="250"></a>')


def btn_ios(slug, lang, t, cls='store-badge'):
    """Apple's own localized "Download on the App Store" badge (img/badges), used unmodified."""
    return (f'<a class="{cls}" href="https://apps.apple.com/app/id{IOS[slug]}"><img src="/img/badges/app-store-{lang}.svg" '
            f'alt="{t["as_badge_alt"]}" width="{108 if lang == "ja" else 120}" height="40"></a>')


def stores(slug, app, lang, t, play_live=True, small=False):
    """Store badges for a game: Google Play when it's public there, the App Store once Apple has released it."""
    out = btn_play(app, lang, t, 'play-badge sm' if small else 'play-badge') if play_live else ''
    if slug in IOS_LIVE:
        out += btn_ios(slug, lang, t, 'store-badge sm' if small else 'store-badge')
    return out


def page(lang, path, *, title, desc, body, data, og='website', style='', preload=None, policy=None):
    t = TEXT[lang]
    url = SITE + href(lang, path)
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{href(l, path)}">\n' for l in TEXT)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}{href("en", path)}">\n'
    langs = ''.join(
        f'<a href="{href(l, path)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else '')
        + f' aria-label="{TEXT[l]["lang_name"]}" title="{TEXT[l]["lang_name"]}">{l.upper()}</a>' for l in TEXT)
    policy_link = f'\n      <a href="/{policy}/privacy-policy.html">{t["privacy_policy"]}</a>' if policy else ''
    pre = f'<link rel="preload" as="image" href="{preload}">\n' if preload else ''
    body_attr = f' style="{style}"' if style else ''
    html = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{alts}<meta name="robots" content="index, follow">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0a0a0f">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og}">
<meta property="og:site_name" content="namlabs">
<meta property="og:locale" content="{t["locale"]}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{ld(data)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://play.google.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700{"&family=Noto+Sans+JP:wght@400;500;700" if lang == "ja" else ""}&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/consent.js"></script>
{pre}</head>
<body{body_attr}>
{PLAY_ICON}
<header class="nav">
  <div class="wrap">
    <a class="logo" href="{href(lang)}"><img src="/icon-192.png" alt="" width="32" height="32">namlabs</a>
    <nav class="nav-links" aria-label="{t["menu"]}">
      <a href="{href(lang)}#games">{t["games"]}</a>
      <a class="hide-sm" href="{href(lang, "sudoku/techniques/")}">{t["guide"]}</a>
      <span class="langs">{langs}</span>
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer>
  <div class="wrap">
    <span>© 2026 namlabs</span>
    <nav>
      <a href="{href(lang, "sudoku/")}">Sudoku</a>
      <a href="{href(lang, "sky-hop/")}">Sky Hop</a>
      <a href="{href(lang, "sudoku/how-to-play.html")}">{t["how_to_play_sudoku"]}</a>
      <a href="{href(lang, "sudoku/techniques/")}">{t["techniques"]}</a>
      <a href="https://www.youtube.com/@namlabsdev" rel="me">YouTube</a>
      <a href="https://www.tiktok.com/@namlabsdev" rel="me">TikTok</a>
      <a href="https://www.facebook.com/namlabsdev" rel="me">Facebook</a>
      <a href="mailto:hoainamit91@gmail.com">{t["contact"]}</a>
      <a href="{href(lang, "privacy.html")}">{t["site_privacy"]["link"]}</a>{policy_link}
    </nav>
    <small class="tm">{t["gp_tm"]}</small>
  </div>
</footer>
</body>
</html>
'''
    out = ROOT / href(lang, path).lstrip('/')
    if path == '' or path.endswith('/'):
        out = out / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    PAGES.append((href(lang, path), TODAY))


def tiles(items):
    return '<div class="tiles">' + ''.join(
        f'<div class="tile"><h3>{h}</h3><p>{p}</p></div>' for _, h, p in items) + '</div>'


def steps(items):
    return '<div class="steps">' + ''.join(
        f'<div class="step"><h3>{h}</h3><p>{p}</p></div>' for h, p in items) + '</div>'


def facts(items):
    return '<div class="facts">' + ''.join(f'<span>{f}</span>' for f in items) + '</div>'


def fan(lang, imgs):
    """Three fanned screenshots; [imgs] are (game, shot number) pairs."""
    return ('<div class="fan rise d1" aria-hidden="true">'
            + ''.join(f'<img src="{shot(g, lang, n)}" alt="" width="540" height="960">' for g, n in imgs)
            + '</div>')


def section(head, inner, sub=''):
    p = f'<p>{sub}</p>' if sub else ''
    return f'<section><div class="wrap"><div class="sec-head"><h2>{head}</h2>{p}</div>{inner}</div></section>'


def tech_cards(lang):
    t = TEXT[lang]
    return '<div class="techs">' + ''.join(
        f'<a class="tech" href="{href(lang, f"sudoku/techniques/{k}.html")}">'
        f'<span class="lvl lvl-{t["tech"][k]["level"]}">{t["levels"][t["tech"][k]["level"]]}</span>'
        f'<h3>{t["tech"][k]["name"]}</h3><p>{t["tech"][k]["card"]}</p></a>' for k in TECHS) + '</div>'


# ── Home ──────────────────────────────────────────────────────────────────

POLICIES = [('block-puzzle', 'Block Puzzle'), ('bunny-steps', 'Bunny Steps'), ('caro', 'Caro'),
            ('color-link', 'Color Link'), ('gomoku', 'Gomoku'), ('island-bridges', 'Island Bridges'),
            ('kakuro', 'Kakuro'), ('lamp-logic', 'Lamp Logic'), ('logic-puzzles', 'Logic Puzzles'),
            ('loop-line', 'Loop Line'), ('mine-logic', 'Mine Logic'), ('number-cross', 'Number Cross'),
            ('park-out', 'Park Out'), ('pixel-logic', 'Pixel Logic'), ('racing-lines', 'Racing Lines'),
            ('sky-hop', 'Sky Hop'), ('star-place', 'Star Place'), ('sudoku', 'Sudoku'),
            ('tangle-out', 'Tangle Out'), ('tents-camp', 'Tents Camp'), ('tile-trio', 'Tile Trio'),
            ('water-sort', 'Water Sort'), ('xiangqi', 'Xiangqi'), ('youtube-tools', 'NamTH Video Tools')]


def game_card(lang, slug, app, name, colors, c, live=True):
    t = TEXT[lang]
    store = stores(slug, app, lang, t, live, small=True)
    soon = not store
    art = ''.join(f'<img src="{shot(slug, lang, n)}" alt="" loading="lazy" width="540" height="960">' for n in (1, 2, 3))
    store = f'<div class="game-stores">{store}</div>' if store else ''
    actions = (f'<div class="game-actions">{store}<a class="btn btn-details" href="{href(lang, slug + "/")}">'
               f'{t["details"]}<span aria-hidden="true">→</span></a></div>')
    badge = f'<span class="badge-soon">{t["soon"]}</span>' if soon else ''
    tags = ''.join(f'<span class="tag">{x}</span>' for x in c['tags'])
    tags = f'<div class="tags">{tags}</div>' if tags else ''
    return f'''<article class="game" style="--c1:{colors[0]};--c2:{colors[1]}">
  <div class="game-art" aria-hidden="true">{art}</div>
  <div class="game-body">
    <div class="game-title"><img src="/img/{slug}/icon-128.webp" alt="{t["icon_alt"].format(name)}" width="60" height="60"><div><div class="name-row"><h3>{name}</h3>{badge}</div><p>{c["sub"]}</p></div></div>
    <p>{c["p"]}</p>
    {tags}
    {actions}
  </div>
</article>'''


def home(lang):
    t, h = TEXT[lang], TEXT[lang]['home']
    cards = (game_card(lang, 'sudoku', 'sudoku', 'Sudoku', ('#8a2be2', '#6366f1'), h['sudoku'])
             + game_card(lang, 'sky-hop', 'sky_hop', 'Sky Hop', ('#2e2a84', '#c2477a'), h['sky_hop'])
             + ''.join(game_card(lang, slug, app, name, colors,
                                 h['logic'] if slug == 'logic-puzzles' else
                                 {'sub': t['game_meta'], 'p': esc(listing(app, lang)['short']), 'tags': []}, live)
                       for slug, app, name, colors, live in GAMES))
    policies = ''.join(f'<li><a href="/{s}/privacy-policy.html">{n}</a></li>' for s, n in POLICIES)
    body = f'''<section class="hero"><div class="wrap">
  <div>
    <span class="eyebrow rise"><i></i>{h["eyebrow"]}</span>
    <h1 class="rise d1">{h["h1"]}</h1>
    <p class="lead rise d2">{h["lead"]}</p>
    <div class="btn-row rise d2">
      <a class="btn btn-play" href="#games"><svg><use href="#play"/></svg><span><small>{h["browse"]}</small>{h["our_games"]}</span></a>
      <a class="btn btn-ghost" href="{href(lang, "sudoku/how-to-play.html")}">{h["learn"]} →</a>
    </div>
    {facts(h["facts"])}
  </div>
  {fan(lang, [("sky-hop", 1), ("sudoku", 1), ("logic-puzzles", 1)])}
</div></section>
<section id="games"><div class="wrap">
  <div class="sec-head"><h2>{h["our_games"]}</h2><p>{h["games_p"]}</p></div>
  <div class="games">{cards}</div>
</div></section>
{section(h["why_h"], tiles(h["tiles"]))}
{section(h["learn_h"], tech_cards(lang), h["learn_p"].format(href(lang, "sudoku/how-to-play.html")))}
<section><div class="wrap"><details class="more"><summary>{t["privacy_policies"]}</summary><ul class="policies">{policies}</ul></details></div></section>'''
    data = {'@graph': [
        {'@type': 'Organization', '@id': f'{SITE}/#org', 'name': 'namlabs', 'url': f'{SITE}/',
         'logo': f'{SITE}/icon-512.png', 'email': 'hoainamit91@gmail.com',
         'sameAs': ['https://play.google.com/store/apps/developer?id=namlabs',
                    'https://www.youtube.com/@namlabsdev',
                    'https://www.tiktok.com/@namlabsdev',
                    'https://www.facebook.com/namlabsdev']},
        {'@type': 'WebSite', '@id': f'{SITE}{href(lang)}#site', 'name': 'namlabs', 'alternateName': 'namlabs.dev',
         'url': SITE + href(lang),
         'inLanguage': lang, 'publisher': {'@id': f'{SITE}/#org'}}]}
    page(lang, '', title=h['title'], desc=h['desc'], body=body, data=data, preload=shot('sudoku', lang, 1))


# ── Game pages ────────────────────────────────────────────────────────────

def app_ld(lang, slug, app, name, genre, desc, play_live=True):
    installs = ([PLAY + app] if play_live else []) + ([f'https://apps.apple.com/app/id{IOS[slug]}'] if slug in IOS_LIVE else [])
    data = {'@type': 'MobileApplication', 'name': name, 'operatingSystem': 'Android, iOS' if slug in IOS_LIVE else 'Android',
            'applicationCategory': 'GameApplication', 'genre': genre, 'description': desc,
            'inLanguage': lang, 'url': SITE + href(lang, slug + '/'), 'image': f'{SITE}/img/{slug}/icon-256.webp',
            'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'publisher': ORG}
    if installs:
        data['installUrl'] = installs[0] if len(installs) == 1 else installs
    return data


def game_hero(lang, slug, app, name, g, fan_shots, extra_btn=''):
    t = TEXT[lang]
    return f'''<section class="hero"><div class="wrap">
  <div>
    <div class="app-head rise"><img src="/img/{slug}/icon-256.webp" alt="{t["icon_alt"].format(name)}" width="84" height="84"><div class="meta"><b>namlabs</b><br>{g["meta"]}</div></div>
    <h1 class="rise d1">{g["h1"]}</h1>
    <p class="lead rise d2">{g["lead"]}</p>
    <div class="btn-row rise d2">{stores(slug, app, lang, t)}{extra_btn}</div>
    {facts(g["facts"])}
  </div>
  {fan(lang, [(slug, n) for n in fan_shots])}
</div></section>'''


def shots(slug, lang, alts):
    return '<div class="shots">' + ''.join(
        f'<img src="{shot(slug, lang, i + 1)}" alt="{esc(a)}" loading="lazy" width="540" height="960">'
        for i, a in enumerate(alts)) + '</div>'


def cta(lang, slug, app, g):
    t = TEXT[lang]
    return f'''<section><div class="wrap"><div class="cta">
  <img class="app-icon" src="/img/{slug}/icon-256.webp" alt="" width="76" height="76">
  <h2>{g["cta_h"]}</h2><p>{g["cta_p"]}</p>
  <div class="btn-row">{stores(slug, app, lang, t)}</div>
</div></div></section>'''


def pills(items):
    return '<div class="pills">' + ''.join(
        f'<span class="pill"><b style="color:{c}">●</b>{x}</span>' for c, x in items) + '</div>'


def sudoku(lang):
    t, g = TEXT[lang], TEXT[lang]['sudoku']
    more = f'<a class="btn btn-ghost" href="{href(lang, "sudoku/how-to-play.html")}">{t["how_to_play"]} →</a>'
    body = '\n'.join([
        game_hero(lang, 'sudoku', 'sudoku', 'Sudoku', g, (2, 1, 3), more),
        section(t['see_it'], shots('sudoku', lang, g['alts']), t['swipe']),
        section(g['love_h'], tiles(g['tiles'])),
        section(t['how_to_play'], steps(g['steps']),
                g['howto_p'].format(href(lang, 'sudoku/how-to-play.html'))),
        section(g['tech_h'], tech_cards(lang), g['tech_p'].format(href(lang, 'sudoku/techniques/'))),
        section(g['levels_h'], pills(zip(('#10b981', '#f59e0b', '#f43f5e', '#8b5cf6'), g['levels'])), g['levels_p']),
        cta(lang, 'sudoku', 'sudoku', g)])
    page(lang, 'sudoku/', title=g['title'], desc=g['desc'], body=body, style='--game:#8a2be2;--game-2:#6366f1', policy='sudoku',
         data=app_ld(lang, 'sudoku', 'sudoku', 'Sudoku', 'Puzzle', g['desc']))


def sky_hop(lang):
    t, g = TEXT[lang], TEXT[lang]['sky_hop']
    medals = zip(('#b45309', '#94a3b8', '#eab308', '#67e8f9'), g['medals'])
    body = '\n'.join([
        game_hero(lang, 'sky-hop', 'sky_hop', 'Sky Hop', g, (2, 1, 4)),
        section(t['see_it'], shots('sky-hop', lang, g['alts']), t['swipe']),
        section(t['how_to_play'], steps(g['steps'])),
        section(g['feat_h'], tiles(g['tiles'])),
        section(g['medals_h'], pills(medals), g['medals_p']),
        cta(lang, 'sky-hop', 'sky_hop', g)])
    page(lang, 'sky-hop/', title=g['title'], desc=g['desc'], body=body, style='--game:#4338ca;--game-2:#db2777', policy='sky-hop',
         data=app_ld(lang, 'sky-hop', 'sky_hop', 'Sky Hop', 'Arcade', g['desc']))


def soon_btn(t):
    return f'<span class="btn btn-ghost btn-soon">{t["soon_btn"]}</span>'


def listing_section(i, head, paras, bullets):
    """One heading of a Play description: rules become numbered steps, "Name — what it is"
    bullets become tiles and anything else a ticked list."""
    lead = ''.join(f'<p>{p}</p>' for p in paras)
    if bullets and all('—' in x for x in bullets):
        inner = '<div class="tiles">' + ''.join(
            '<div class="tile"><h3>{}</h3><p>{}</p></div>'.format(*re.split(r'\s*—\s*', x, maxsplit=1))
            for x in bullets) + '</div>'
    elif bullets and i == 0:
        inner = '<div class="steps">' + ''.join(f'<div class="step"><p>{x}</p></div>' for x in bullets) + '</div>'
    elif bullets:
        inner = '<ul class="checks">' + ''.join(f'<li>{x}</li>' for x in bullets) + '</ul>'
    else:
        inner = ''
    return f'<section><div class="wrap"><div class="sec-head"><h2>{head}</h2>{lead}</div>{inner}</div></section>'


def store_game(lang, slug, app, name, colors, live):
    """A game page made from the game's Play listing in [lang]."""
    t, raw = TEXT[lang], listing(app, lang)
    g = {k: esc(raw[k]) for k in ('title', 'short', 'outro')}
    intro = [esc(p) for p in raw['intro']]
    button = stores(slug, app, lang, t, live) or soon_btn(t)
    public = live or slug in IOS_LIVE
    more = ''.join(f'<p class="lead rise d2">{p}</p>' for p in intro[1:])
    n_shots = len(list((ROOT / 'img' / slug / ('' if lang == 'en' else lang)).glob('shot-*.webp')))
    alts = [t['shot_alt'].format(name, i) for i in range(1, n_shots + 1)]
    body = '\n'.join([
        f'''<section class="hero"><div class="wrap">
  <div>
    <div class="app-head rise"><img src="/img/{slug}/icon-256.webp" alt="{t["icon_alt"].format(name)}" width="84" height="84"><div class="meta"><b>namlabs</b><br>{t["game_meta"]}</div></div>
    <h1 class="rise d1">{g["title"]}</h1>
    <p class="lead rise d2">{intro[0]}</p>{more}
    <div class="btn-row rise d2">{button}</div>
  </div>
  {fan(lang, [(slug, n) for n in (2, 1, 3)])}
</div></section>''',
        section(t['see_it'], shots(slug, lang, alts), t['swipe']),
        *(listing_section(i, esc(h), [esc(p) for p in ps], [esc(x) for x in bs])
          for i, (h, ps, bs) in enumerate(raw['sections'])),
        f'''<section><div class="wrap"><div class="cta">
  <img class="app-icon" src="/img/{slug}/icon-256.webp" alt="" width="76" height="76">
  <h2>{name}</h2><p>{g["outro"] if public and g["outro"] else g["short"]}</p>
  <div class="btn-row">{button}</div>
</div></div></section>'''])
    data = app_ld(lang, slug, app, name, 'Puzzle', raw['short'], play_live=live)
    page(lang, slug + '/', title=t['game_title'].format(raw['title']), desc=raw['short'], body=body, data=data,
         style=f'--game:{colors[0]};--game-2:{colors[1]}', policy=slug, preload=shot(slug, lang, 1))


# ── Guides ────────────────────────────────────────────────────────────────

def figures(lang, html):
    """Swaps each [[diagram]] marker for the grid and its caption."""
    def fig(m):
        label, caption = TEXT[lang]['boards'][m.group(1)]
        return f'<figure class="fig">{DIAGRAMS[m.group(1)](esc(label))}<figcaption>{caption}</figcaption></figure>'
    return re.sub(r'\[\[([a-z-]+)\]\]', fig, html)


def article(lang, path, crumbs, *, title, h1, desc, lead, body, faq=(), after='', published=TODAY):
    """[crumbs] are (name, path) pairs leading to this page, which comes last with path None."""
    t = TEXT[lang]
    trail = ' › '.join(f'<a href="{href(lang, p)}">{n}</a>' if p is not None else f'<span>{n}</span>'
                       for n, p in crumbs)
    faq_html = ''
    if faq:
        faq_html = f'<h2>{t["faq"]}</h2>' + ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in faq)
    store = f'''<div class="cta guide-cta">
  <img class="app-icon" src="/img/sudoku/icon-256.webp" alt="" width="76" height="76">
  <h2>{t["practise_h"]}</h2><p>{t["practise_p"]}</p>
  <div class="btn-row">{btn_play("sudoku", lang, t)}</div>
</div>'''
    body_html = f'''<section class="hero hero-guide"><div class="wrap">
  <div class="guide">
    <nav class="crumbs" aria-label="{t["breadcrumb"]}">{trail}</nav>
    <h1 class="rise">{h1}</h1>
    <p class="lead rise d1">{lead}</p>
  </div>
</div></section>
<section class="guide-body"><div class="wrap"><article class="guide prose">
{figures(lang, body)}
{faq_html}
{after}
{store}
</article></div></section>'''
    url = SITE + href(lang, path)
    graph = [
        {'@type': 'Article', 'headline': h1 if len(h1) <= 110 else title, 'description': desc,
         'image': f'{SITE}/og-image.png', 'datePublished': published, 'dateModified': TODAY,
         'inLanguage': lang, 'mainEntityOfPage': url, 'author': ORG,
         'publisher': {**ORG, 'logo': {'@type': 'ImageObject', 'url': f'{SITE}/icon-512.png'}}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': text(n), 'item': SITE + href(lang, p if p is not None else path)}
            for i, (n, p) in enumerate(crumbs)]}]
    if faq:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': text(q), 'acceptedAnswer': {'@type': 'Answer', 'text': text(a)}}
            for q, a in faq]})
    page(lang, path, title=title, desc=desc, body=body_html, og='article', data={'@graph': graph},
         style='--game:#8a2be2;--game-2:#6366f1', policy='sudoku')


def site_privacy(lang):
    """What the website itself collects; the apps have their own policies."""
    p = TEXT[lang]["site_privacy"]
    body = f'''<section class="hero hero-guide"><div class="wrap">
  <div class="guide">
    <h1 class="rise">{p["h1"]}</h1>
    <p class="lead rise d1">{p["lead"]}</p>
  </div>
</div></section>
<section class="guide-body"><div class="wrap"><article class="guide prose">
{p["body"]}
<p><button type="button" class="btn btn-ghost" id="consent-change">{p["change"]}</button></p>
</article></div></section>'''
    page(lang, 'privacy.html', title=p['title'], desc=p['lead'], body=body,
         data={'@type': 'WebPage', 'name': p['title'], 'url': SITE + href(lang, 'privacy.html'), 'publisher': ORG})


def how_to_play(lang):
    t, g = TEXT[lang], TEXT[lang]['howto']
    after = f'<h2>{g["next_h"]}</h2><p>{g["next_p"]}</p>{tech_cards(lang)}'
    article(lang, 'sudoku/how-to-play.html', [('namlabs', ''), ('Sudoku', 'sudoku/'), (t['how_to_play'], None)],
            title=g['title'], h1=g['h1'], desc=g['desc'], lead=g['lead'], body=g['body'], faq=g['faq'],
            after=after)


def techniques(lang):
    t, g = TEXT[lang], TEXT[lang]['hub']
    crumbs = [('namlabs', ''), ('Sudoku', 'sudoku/')]
    article(lang, 'sudoku/techniques/', crumbs + [(t['techniques'], None)], title=g['title'], h1=g['h1'],
            desc=g['desc'], lead=g['lead'], body=f'{g["body"]}<h2>{t["all_techniques"]}</h2>{tech_cards(lang)}')
    for i, k in enumerate(TECHS):
        a = t['tech'][k]
        nav = []
        if i:
            p = TECHS[i - 1]
            nav.append(f'<a class="prev" href="{href(lang, f"sudoku/techniques/{p}.html")}"><small>{t["prev"]}</small>{t["tech"][p]["name"]}</a>')
        if i + 1 < len(TECHS):
            n = TECHS[i + 1]
            nav.append(f'<a class="next" href="{href(lang, f"sudoku/techniques/{n}.html")}"><small>{t["next"]}</small>{t["tech"][n]["name"]}</a>')
        after = '<nav class="pager">' + ''.join(nav) + '</nav>'
        article(lang, f'sudoku/techniques/{k}.html',
                crumbs + [(t['techniques'], 'sudoku/techniques/'), (a['name'], None)],
                title=a['title'], h1=a['h1'], desc=a['desc'], lead=a['lead'], body=a['body'], after=after)


# ── Sitemap ───────────────────────────────────────────────────────────────

def sitemap():
    """Rewrites the generated pages' entries and keeps every other <url> as it was."""
    path = ROOT / 'sitemap.xml'
    ours = {SITE + p for p, _ in PAGES}
    old = re.findall(r'  <url><loc>(.*?)</loc><lastmod>(.*?)</lastmod></url>', path.read_text(encoding='utf-8'))
    rest = [(loc, mod) for loc, mod in old if loc not in ours]
    rows = [(SITE + p, m) for p, m in PAGES] + rest
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    + ''.join(f'  <url><loc>{l}</loc><lastmod>{m}</lastmod></url>\n' for l, m in rows)
                    + '</urlset>\n', encoding='utf-8')


if __name__ == '__main__':
    for lang in TEXT:
        home(lang)
        sudoku(lang)
        sky_hop(lang)
        for game in GAMES:
            store_game(lang, *game)
        how_to_play(lang)
        techniques(lang)
        site_privacy(lang)
    sitemap()
    print(f'{len(PAGES)} pages')
