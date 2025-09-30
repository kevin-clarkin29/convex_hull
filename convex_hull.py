from __future__ import annotations
from typing import Sequence, Tuple, List

Point = Tuple[float, float]

def _cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def _polygon_area2(poly: Sequence[Point]) -> float:
    if len(poly) < 3:
        return 0.0
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - y1 * x2
    return s

def convex_hull(points: Sequence[Point], *, include_collinear: bool=False, eps: float=1e-12) -> List[Point]:
    uniq = sorted(set((float(x), float(y)) for (x, y) in points))
    n = len(uniq)
    if n <= 1:
        return uniq.copy()
    
    lower: List[Point] = []
    for p in uniq:
        while len(lower) >= 2:
            turn = _cross(lower[-2], lower[-1], p)
            if include_collinear:
                if turn < -eps:
                    lower.pop()
                else:
                    break
            else:
                if turn <= eps:
                    lower.pop()
                else:
                    break
        lower.append(p)
    
    upper: List[Point] = []
    for p in reversed(uniq):
        while len(upper) >= 2:
            turn = _cross(upper[-2], upper[-1], p)
            if include_collinear:
                if turn < -eps:
                    upper.pop()
                else:
                    break
            else:
                if turn <= eps:
                    upper.pop()
                else:
                    break
        upper.append(p)
    
    hull = lower[:-1] + upper[:-1]
    if include_collinear and abs(_polygon_area2(hull)) <= eps:
        return uniq
    
    if len(hull) == 0:
        if include_collinear:
            return uniq
        else:
            return [uniq[0], uniq[-1]] if uniq[0] != uniq[-1] else [uniq[0]]
    return hull
