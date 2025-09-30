"""
convex_hull.py
--
This file contains a SINGLE function `convex_hull(points, include_collinear=False, eps=1e-12)`
that returns the convex hull of 2D points.

READ THIS FIRST:
- Imagine your points are pushpins on a board.
- Stretch a rubber band around every pin and let it snap tight.
- The rubber band outlines the "convex hull" — the outer boundary.
- This function returns the CORNER POINTS of that boundary in COUNTERCLOCKWISE order.

IMPORTANT:
- THERE IS NO "MAIN" CODE THAT RUNS AUTOMATICALLY HERE.
- Import this function from another file and call it with your points.
- Example (in a different file):
      from convex_hull import convex_hull
      pts = [(0,0),(1,0),(1,1),(0,1),(0.5,0.5)]
      print(convex_hull(pts))
- If you want a tiny runnable demo, scroll to the very bottom for a commented
  "if __name__ == '__main__':" section. It is COMMENTED OUT on purpose so this
  module feels safe to read. You can uncomment it to try it.

ABOUT THE ALGORITHM (Andrew's Monotone Chain):
- Step 1: Sort the points (by x, then y) removing duplicates.
- Step 2: Build the "lower" boundary by scanning left to right, keeping only left turns.
- Step 3: Build the "upper" boundary by scanning right to left, again keeping left turns.
- Step 4: Concatanate lower and upper together (skipping duplicate endpoints).

WHY IT'S SHORT:
- Each point is pushed at most once and popped at most once (after sorting).

TWO MODES:
- include_collinear=False (default): keep only CORNERS (typical convex hull).
- include_collinear=True: additionally keep points that lie exactly on the hull edges.
  (Interior points are never kept in either mode.)

Furthermore
- Duplicates are removed up front.
- `eps` is a tiny threshold to treat "almost zero" as zero (floating-point safety).
"""

from __future__ import annotations
from typing import Sequence, Tuple, List

# A point is just a pair of floats: (x, y)
Point = Tuple[float, float]


def _cross(o: Point, a: Point, b: Point) -> float:
    """
    The "turn test" using 2D cross product.
    Think of arrows OA and OB (from O to A, and from O to B).

    Returns:
        > 0  to Left turn (good for a CCW boundary)
        < 0  to Right turn (bad; creates an inward dent)
        = 0  to Collinear (on a straight line)
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _polygon_area2(poly: Sequence[Point]) -> float:
    """
    Twice the signed area of a polygon (shoelace formula).
    We only use this to detect the special case "all points are collinear".
    """
    if len(poly) < 3:
        return 0.0
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - y1 * x2
    return s


def convex_hull(points: Sequence[Point], *, include_collinear: bool=False, eps: float=1e-12) -> List[Point]:
    """
    Compute the convex hull of 2D points using Andrew's Monotone Chain algorithm.

    Args:
        points:
            A sequence (list/tuple/etc.) of (x, y) pairs. They can be ints or floats.
        include_collinear (default False):
            - False to return only the "corner" points of the hull.
            - True  to also keep points that lie on the hull edges (collinear with an edge).
        eps (default 1e-12):
            A tiny threshold so that tiny rounding errors count as zero.

    Returns:
        A list of points forming the convex hull in COUNTERCLOCKWISE order,
        with no repeated first/last point.

    Behavior guarantees:
        - Duplicate points are removed internally.
        - If there is only 0 or 1 unique point, we return that immediately.
        - If ALL points are perfectly collinear:
            • include_collinear=False  to return just the two endpoints (if distinct).
            • include_collinear=True   to return ALL unique points in sorted order.
    """
    #  Step 0: Normalize & sort inputs 
    # Convert to floats and remove duplicates with set(), then sort by (x, y).
    uniq = sorted(set((float(x), float(y)) for (x, y) in points))
    n = len(uniq)
    if n <= 1:
        # 0 or 1 unique point to that's the hull.
        return uniq.copy()

    #  Step 1: Build LOWER hull (left to right) 
    lower: List[Point] = []
    for p in uniq:
        # While we have at least two points in the "stack" and the last turn is "not allowed",
        # we pop the last point. "Not allowed" depends on the mode:
        # - include_collinear=False: we pop on right turns OR collinear (turn <= eps).
        # - include_collinear=True:  we pop ONLY on right turns (turn < -eps),
        #   so collinear points can remain (they become part of the boundary list).
        while len(lower) >= 2:
            turn = _cross(lower[-2], lower[-1], p)
            if include_collinear:
                if turn < -eps:          # a right turn to drop the middle point
                    lower.pop()
                else:                     # left turn or collinear to keep it
                    break
            else:
                if turn <= eps:           # right turn or collinear to drop the middle point
                    lower.pop()
                else:                     # left turn to keep it
                    break
        lower.append(p)

    #  Step 2: Build UPPER hull (right to left) 
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

    # Step 3: Stitch lower and upper 
    # The last point of each list is the starting point of the other list.
    # We skip them to avoid duplicates.
    hull = lower[:-1] + upper[:-1]

    #  Step 4: Special handling if everything was collinear 
    # If include_collinear=True and the polygon area is ~0, then just return
    # all unique points in sorted order (this is often useful for assignments).
    if include_collinear and abs(_polygon_area2(hull)) <= eps:
        return uniq

    # If somehow the hull list ended empty (degenerate inputs), return sensible defaults.
    if len(hull) == 0:
        if include_collinear:
            return uniq
        else:
            return [uniq[0], uniq[-1]] if uniq[0] != uniq[-1] else [uniq[0]]

    return hull



# OPTIONAL: A tiny built-in demo. It is COMMENTED OUT on purpose so this file
# has no side effects when you import it. If you want to try it directly:
# 1) Remove the leading '#' from the lines below.
# 2) Run:  python convex_hull.py

#
# if __name__ == "__main__":
#     # Example points: a square with one interior point.
#     pts = [(0,0), (1,0), (1,1), (0,1), (0.5,0.5)]
#     print("Corners only:", convex_hull(pts))
#     print("Include edge-collinear:", convex_hull(pts, include_collinear=True))
#
#     # Try a triangle with points exactly on edges (to see include_collinear):
#     tri = [(0,0),(3,0),(0,3),(1,0),(2,0),(0,1),(0,2)]
#     print("Triangle corners only:", convex_hull(tri))
#     print("Triangle include edge points:", convex_hull(tri, include_collinear=True))
#

