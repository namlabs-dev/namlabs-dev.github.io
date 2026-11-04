"""The example grids used in the Sudoku guides.

Each entry checks that the position really shows the move it is meant to show,
then returns the grid as HTML. Labels and captions live with each language.
"""
from board import Board, house_box, house_col, house_row


def last_cell(label):
    b = Board({'R5C1': 7, 'R5C2': 2, 'R5C3': 9, 'R5C4': 1, 'R5C6': 6, 'R5C7': 3, 'R5C8': 8, 'R5C9': 5})
    assert b.cands('R5C5') == {4}
    return b.html(label, area=house_row(5), key=['R5C5'], new={'R5C5': 4})


def naked_single(label):
    givens = {'R5C1': 1, 'R5C2': 2, 'R5C8': 3, 'R1C5': 4, 'R2C5': 5, 'R9C5': 6, 'R4C4': 7, 'R6C6': 8}
    b = Board(givens)
    assert b.cands('R5C5') == {9}
    return b.html(label, area=house_row(5) + house_col(5) + house_box(4), key=['R5C5'], src=givens,
                  new={'R5C5': 9})


def hidden_single(label):
    givens = {'R2C6': 5, 'R3C8': 5, 'R7C2': 5, 'R1C1': 8}
    b = Board(givens)
    assert b.spots(5, house_box(0)) == {'R1C3'}
    assert len(b.cands('R1C3')) > 1  # hidden: the cell itself still has other candidates
    blocked = [n for n in house_box(0) if n not in ('R1C1', 'R1C3')]
    return b.html(label, area=house_box(0), key=['R1C3'], src=['R2C6', 'R3C8', 'R7C2'], no=blocked,
                  new={'R1C3': 5})


def _naked_pair_board():
    return Board({'R1C3': 1, 'R1C4': 2, 'R1C6': 4, 'R1C8': 5, 'R1C9': 7,
                  'R2C1': 6, 'R3C2': 9, 'R6C5': 9})


def naked_pair(label):
    b = _naked_pair_board()
    assert b.cands('R1C1') == b.cands('R1C2') == {3, 8}
    assert b.cands('R1C5') == {3, 6, 8} and b.cands('R1C7') == {3, 6, 8, 9}
    return b.html(label, area=house_row(1), key=['R1C1', 'R1C2'], marks=['R1C1', 'R1C2', 'R1C5', 'R1C7'],
                  strike={'R1C5': (3, 8), 'R1C7': (3, 8)})


def pointing_pair(label):
    b = Board({'R1C2': 8, 'R1C3': 1, 'R2C1': 6, 'R3C2': 2, 'R3C3': 7, 'R7C1': 4})
    assert b.spots(4, house_box(0)) == {'R2C2', 'R2C3'}
    outside = [n for n in house_row(2) if n not in house_box(0)]
    assert b.spots(4, outside) == set(outside)
    return b.html(label, area=house_box(0), key=['R2C2', 'R2C3'], src=['R7C1'],
                  marks=['R2C2', 'R2C3'] + outside, only=4, strike={n: (4,) for n in outside})


def x_wing(label):
    b = Board({'R7C1': 7, 'R8C5': 7, 'R9C9': 7,
               'R2C2': 3, 'R2C4': 1, 'R2C6': 9, 'R2C8': 4,
               'R6C2': 8, 'R6C4': 2, 'R6C6': 6, 'R6C8': 5})
    corners = ['R2C3', 'R2C7', 'R6C3', 'R6C7']
    assert b.spots(7, house_row(2)) == {'R2C3', 'R2C7'}
    assert b.spots(7, house_row(6)) == {'R6C3', 'R6C7'}
    cols = house_col(3) + house_col(7)
    gone = sorted(b.spots(7, cols) - set(corners))
    assert gone == ['R1C3', 'R1C7', 'R3C3', 'R3C7', 'R4C3', 'R4C7', 'R5C3', 'R5C7'], gone
    return b.html(label, area=house_row(2) + house_row(6), key=corners, src=['R7C1', 'R8C5', 'R9C9'],
                  marks=corners + gone, only=7, strike={n: (7,) for n in gone})


DIAGRAMS = {
    'last-cell': last_cell,
    'naked-single': naked_single,
    'hidden-single': hidden_single,
    'naked-pair': naked_pair,
    'pointing-pair': pointing_pair,
    'x-wing': x_wing,
}
