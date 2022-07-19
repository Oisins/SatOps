import math

import cv2
import numpy as np

from utils import find_earth_circle, segment_earth_moon, find_moon, find_earth_edge

# Load image and convert to b/w
# img_original = cv2.imread("bilder/csm_Beesat9_Moon-01-04-2020_61fb3aba42.jpg")
img_original = cv2.imread("bilder/9-7.jpg")
img_grey = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
im_bw = cv2.threshold(img_grey, 60, 255, cv2.THRESH_BINARY)[1]

# Use Gauss filter to extract edges
im_gauss = cv2.Laplacian(im_bw, cv2.CV_8U)

# Segment Earth and Moon
earth_mask, moon_mask = segment_earth_moon(im_bw)
im_earth = im_bw & earth_mask
im_moon = im_bw & moon_mask

# Find Moon in image
moon_position, moon_radius = find_moon(im_moon)

# Determine apparent center of earth and radius
points = np.array([find_earth_edge(x, im_earth) for x in range(im_gauss.shape[1])])
earth_radius, earth_center = find_earth_circle(points)

# Place chord on earths edge and calculate slope
m_sekante = (points[0][1] - points[-1][1]) / (points[0][0] - points[-1][0])
m_radius = -1 / m_sekante

# Calculate reference point. Point lies on intersection of earth and a line perpendicular to the previously calculated
# chord passing through the center of the earth
dx = np.cos(np.arctan(m_radius)) * earth_radius
dy = dx * m_radius

reference_point_x = earth_center[0] + dx
reference_point_y = earth_center[1] + dy
print("Earth center", earth_center)
print("Earth radius", earth_radius)
print()

print("Rollwinkel", math.degrees(math.atan(m_sekante)))

moon_position_relativ = moon_position - np.array(img_original.shape[:2][::-1]) / 2
print("Y-Distance Moon to cross-hairs", moon_position_relativ[0])

# Calculate intersection between Cross-hairs and earth's edge
earth_edge_relative = earth_center[1] - math.sqrt(
    earth_radius ** 2 - (img_original.shape[1] / 2 - earth_center[0]) ** 2) - img_original.shape[0] / 2
print("Y-Distance Earth edge to Cross-Hairs", earth_edge_relative)

# Draw onto image
img_original = cv2.line(img_original, points[0], points[-1], color=(0, 0, 255))
img_original = cv2.circle(img_original, earth_center, int(earth_radius), (0, 255, 0), 1)
img_original = cv2.circle(img_original, np.round([reference_point_x, reference_point_y]).astype(int),
                          1, (0, 0, 255), -1)
img_original = cv2.circle(img_original, np.round(moon_position).astype(int), int(moon_radius), (0, 255, 0), 2)
img_original = cv2.line(img_original, (0, int(img_original.shape[0] / 2)),
                        (img_original.shape[1], int(img_original.shape[0] / 2)), thickness=1, color=(255, 255, 255))
img_original = cv2.line(img_original, (int(img_original.shape[1] / 2), 0),
                        (int(img_original.shape[1] / 2), img_original.shape[0]), thickness=1, color=(255, 255, 255))

# img_original = cv2.resize(img_original, (1000, 1000))
cv2.imshow("IMG2", img_original)
cv2.waitKey(0)
