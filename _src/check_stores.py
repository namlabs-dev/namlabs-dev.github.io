"""Shows which namlabs games are public on Google Play and the App Store.

    python3 _src/check_stores.py

Flip the game's flag in stores.GAMES (Play) or add its slug to stores.IOS_LIVE
(App Store) once it's public, then rebuild.
"""
import json
import urllib.error
import urllib.request

from stores import GAMES, IOS, IOS_LIVE

PLAY = {'sudoku': ('sudoku', True), 'sky-hop': ('sky_hop', True),
        **{slug: (app, live) for slug, app, _, _, live in GAMES}}


def on_play(app):
    try:
        urllib.request.urlopen(f'https://play.google.com/store/apps/details?id=com.namlabs.{app}', timeout=20)
        return True
    except urllib.error.HTTPError:
        return False


def on_ios(app_id):
    with urllib.request.urlopen(f'https://itunes.apple.com/lookup?id={app_id}', timeout=20) as r:
        return json.load(r)['resultCount'] > 0


if __name__ == '__main__':
    print(f'{"game":15} {"Play":14} App Store')
    for slug, (app, flag) in PLAY.items():
        p, i = on_play(app), on_ios(IOS[slug])
        note = lambda public, set_: ('public' if public else 'not yet') + ('' if public == set_ else ' ← update stores.py')
        print(f'{slug:15} {note(p, flag):14} {note(i, slug in IOS_LIVE)}')
