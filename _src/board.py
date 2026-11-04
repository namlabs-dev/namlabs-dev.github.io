"""Small Sudoku diagrams for the technique guides.

Candidates are worked out from the placed digits, never typed in by hand,
so a diagram can't show a pencil mark the rules don't allow.
"""


def cell(name):
    """'R5C5' -> (4, 4)."""
    return int(name[1]) - 1, int(name[3]) - 1


def box(r, c):
    return r // 3 * 3 + c // 3


class Board:
    def __init__(self, givens):
        self.d = {cell(k): v for k, v in givens.items()}
        for (r, c), v in self.d.items():
            assert v not in self._seen(r, c, skip=(r, c)), f'duplicate {v} at R{r + 1}C{c + 1}'

    def _seen(self, r, c, skip=None):
        return {v for (rr, cc), v in self.d.items()
                if (rr, cc) != skip and (rr == r or cc == c or box(rr, cc) == box(r, c))}

    def cands(self, name):
        r, c = cell(name)
        if (r, c) in self.d:
            return set()
        return set(range(1, 10)) - self._seen(r, c)

    def spots(self, digit, names):
        """The cells among [names] where [digit] can still go."""
        return {n for n in names if digit in self.cands(n)}

    def html(self, label, *, area=(), key=(), src=(), no=(), new=None, marks=(), only=None, strike=None):
        """[area] shades a house, [key] rings the cells the move is about, [src] tints
        the digits doing the work, [no] hatches ruled-out cells, [new] places answers,
        [marks] shows candidates (just [only] if given) and [strike] crosses some out."""
        new, strike = new or {}, strike or {}
        area, key, src, no, marks = (set(map(cell, x)) for x in (area, key, src, no, marks))
        out = []
        for r in range(9):
            for c in range(9):
                name = f'R{r + 1}C{c + 1}'
                cls = [k for k, s in (('area', area), ('key', key), ('src', src), ('no', no)) if (r, c) in s]
                if c in (2, 5):
                    cls.append('br')
                if r in (2, 5):
                    cls.append('bb')
                if (r, c) in self.d:
                    inner = str(self.d[(r, c)])
                elif name in new:
                    assert new[name] in self.cands(name), f'{new[name]} cannot go in {name}'
                    cls.append('new')
                    inner = str(new[name])
                elif (r, c) in marks:
                    cs = self.cands(name)
                    gone = set(strike.get(name, ()))
                    assert gone <= cs, f'{name} has no candidate {gone - cs}'
                    if only is not None:
                        # One digit tracked across the grid: show it big, not in its pencil-mark slot.
                        assert only in cs, f'{name} has no candidate {only}'
                        k = 'x' if only in gone else 'k' if (r, c) in key else ''
                        inner = f'<span class="cand1 {k}">{only}</span>'
                    else:
                        spans = []
                        for v in range(1, 10):
                            k = ' class="x"' if v in gone else ' class="k"' if (r, c) in key else ''
                            spans.append(f'<i{k}>{v}</i>' if v in cs else '<i></i>')
                        inner = f'<span class="cands">{"".join(spans)}</span>'
                else:
                    inner = ''
                attr = f' class="{" ".join(cls)}"' if cls else ''
                out.append(f'<div{attr}>{inner}</div>')
        return (f'<div class="board" role="img" aria-label="{label}">'
                + ''.join(out) + '</div>')


def house_row(r):
    return [f'R{r}C{c}' for c in range(1, 10)]


def house_col(c):
    return [f'R{r}C{c}' for r in range(1, 10)]


def house_box(b):
    r0, c0 = b // 3 * 3, b % 3 * 3
    return [f'R{r0 + i + 1}C{c0 + j + 1}' for i in range(3) for j in range(3)]
