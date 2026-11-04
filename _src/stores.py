"""Game pages built straight from each game's Google Play listing.

The listing text lives in the game's own repo (store/listing/<lang>/*.txt, or
store/listing.md for Logic Puzzles), so the page always says what Play says.
"""
import os
import pathlib
import re

REPOS = pathlib.Path(os.environ.get('NAMLABS_REPOS', '/home/namth/Development'))
PLAY_LANG = {'en': 'en-US', 'vi': 'vi-VN', 'ja': 'ja-JP'}

# slug, Play package suffix, short name, card colours, released on Play?
GAMES = [
    ('logic-puzzles', 'logic_puzzles', 'Logic Puzzles', ('#f97316', '#ef4444'), False),
    ('park-out', 'park_out', 'Park Out', ('#f59e0b', '#475569'), False),
    ('water-sort', 'water_sort', 'Water Sort', ('#4f46e5', '#14b8a6'), False),
    ('tangle-out', 'tangle_out', 'Tangle Out', ('#ec4899', '#8b5cf6'), False),
    ('tile-trio', 'tile_trio', 'Tile Trio', ('#0e7490', '#f97316'), False),
]


def _from_md(app, lang):
    """Title, short and full description of one language in store/listing.md."""
    md = (REPOS / app / 'store/listing.md').read_text(encoding='utf-8')
    part = re.split(r'^## ', md, flags=re.M)
    block = next(p for p in part if f'({PLAY_LANG[lang]})' in p.splitlines()[0])
    fields = re.findall(r'^\*\*(.+?)\*\*\n(.*?)(?=^\*\*|\Z)', block, flags=re.M | re.S)
    title, short, full = (v.strip() for _, v in fields[:3])
    return title, short, full


def _from_txt(app, lang):
    d = REPOS / app / 'store/listing' / PLAY_LANG[lang]
    return tuple((d / f).read_text(encoding='utf-8').strip()
                 for f in ('title.txt', 'short_description.txt', 'full_description.txt'))


def _is_head(line, nxt, stars):
    """Listings either mark headings with ★, or use a short line right before a list."""
    if stars:
        return line.startswith('★')
    return len(line) <= 30 and nxt.startswith('•') and not line.startswith('•')


def listing(app, lang):
    """{title, short, intro: [p], sections: [(head, [p], [bullet])], outro}"""
    md = REPOS / app / 'store/listing.md'
    title, short, full = (_from_md if md.exists() else _from_txt)(app, lang)
    lines = [l.strip() for l in full.splitlines() if l.strip()]
    # Closing lines ("Small breaks, sharper mind...") are the ones after the last bullet.
    last = max((i for i, l in enumerate(lines) if l.startswith('•')), default=len(lines) - 1)
    lines, outro = lines[:last + 1], lines[last + 1:]
    intro, sections = [], []
    stars = any(l.startswith('★') for l in lines)
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if _is_head(line, nxt, stars):
            head = line.lstrip('★ ').strip()
            sections.append((head.capitalize() if head.isupper() else head, [], []))
        elif not sections:
            intro.append(line)
        elif line.startswith('•'):
            sections[-1][2].append(line.lstrip('• ').strip())
        else:
            sections[-1][1].append(line)
    return {'title': title, 'short': short, 'intro': intro, 'sections': sections, 'outro': ' '.join(outro)}
