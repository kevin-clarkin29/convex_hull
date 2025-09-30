# sanity check for convex_hull
# - shows the difference between default mode (corners only)
#   and include_collinear=True (keeps edge points)
# - this specific input has an interior point, so both lines match

from convex_hull import convex_hull

# A unit square plus one interior point (0.5, 0.5)
pts = [(0,0), (1,0), (1,1), (0,1), (0.5,0.5)]

# Corners-only hull (default)
print(convex_hull(pts))

# Keep edge-collinear points (no effect here since the extra point is interior)
print(convex_hull(pts, include_collinear=True))
