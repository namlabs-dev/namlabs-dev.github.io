"""Copies each store game's Play icon and screenshots into /img as small WebP files.

    python3 _src/images.py
"""
import pathlib

from PIL import Image

from build import ROOT
from stores import GAMES, REPOS


def save(src, dst, size):
    dst.parent.mkdir(parents=True, exist_ok=True)
    Image.open(src).convert('RGB').resize(size, Image.LANCZOS).save(dst, 'WEBP', quality=80, method=6)


def main():
    for slug, app, *_ in GAMES:
        store = REPOS / app / 'store'
        icon = store / 'graphics/icon-512.png'
        if not icon.exists():
            icon = store / 'play_icon_512.png'
        for n in (128, 256):
            save(icon, ROOT / f'img/{slug}/icon-{n}.webp', (n, n))
        for lang in ('en', 'vi', 'ja'):
            out = ROOT / 'img' / slug / ('' if lang == 'en' else lang)
            for old in out.glob('shot-*.webp'):
                old.unlink()
            for png in sorted((store / f'graphics/{lang}/phone-screenshots').glob('*.png')):
                save(png, out / f'shot-{png.stem}.webp', (540, 960))
        print(slug)


if __name__ == '__main__':
    main()
