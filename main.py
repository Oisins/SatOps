import math

import cv2
import numpy as np
from scipy.spatial.transform import Rotation

from moon_position.moon_position import beesat9_apparent_moon_angle_BFK, beesat9_eci, \
    transformation_BFK_to_ICRF, beesat9_moon_vector
from moon_position.visualisation import visualise_bodies
from utils import find_earth_circle, segment_earth_moon, find_moon, find_earth_edge

camera_angle_width = 15
camera_angle_height = 11.5 * 2

# Load image and convert to b/w
# img_original = cv2.imread("bilder/csm_Beesat9_Moon-01-04-2020_61fb3aba42.jpg")
# img_original = cv2.imread("bilder/9-7.jpg")
img_original = cv2.imread("bilder/B4-Slot11-Horizon.jpg")
img_grey = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
im_bw = cv2.threshold(img_grey, 60, 255, cv2.THRESH_BINARY)[1]

cv2.imwrite("out/0-original.jpg", img_original)
cv2.imwrite("out/1-grey.jpg", img_grey)
cv2.imwrite("out/2-bw.jpg", im_bw)

image_height, image_width, _ = img_original.shape

# Use Gauss filter to extract edges
im_gauss = cv2.Laplacian(im_bw, cv2.CV_8U)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
cv2.imwrite("out/3-gauss.jpg", cv2.dilate(im_gauss, kernel, iterations=2))

# Segment Earth and Moon
earth_mask, moon_mask = segment_earth_moon(im_bw)
im_earth = im_bw & earth_mask
im_moon = im_bw & moon_mask

# Find Moon in image
moon_position, moon_radius = find_moon(im_moon)

# Determine apparent center of earth and radius
points = np.array([find_earth_edge(x, im_earth) for x in range(im_gauss.shape[1])])  # TODO: Hier wird Kante gesucht. Es muss iwie unterschieden werden, ob der Pixel gefunden wurde und wenn nicht soll dieser Wert aus dem Array entfernt werden
apparent_earth_radius, earth_center = find_earth_circle(points)

# Place chord on earths edge and calculate slope
m_sekante = (points[0][1] - points[-1][1]) / (points[0][0] - points[-1][0])
m_radius = -1 / m_sekante

# Calculate reference point. Point lies on intersection of earth and a line perpendicular to the previously calculated
# chord passing through the center of the earth
print("Earth center", earth_center)
print("Earth radius", apparent_earth_radius)
print()

roll_angle = -math.atan(m_sekante)
print("Rollwinkel", math.degrees(roll_angle))

moon_position_relativ = moon_position - np.array(img_original.shape[:2][::-1]) / 2
# print("Y-Distance Moon to cross-hairs", moon_position_relativ[0])

# Calculate intersection between Cross-hairs and earth's edge
earth_edge_relative = earth_center[1] - math.sqrt(
    apparent_earth_radius ** 2 - (img_original.shape[1] / 2 - earth_center[0]) ** 2) - img_original.shape[0] / 2
print("Y-Distance Earth edge to Cross-Hairs", earth_edge_relative)

# Draw onto image
img_original = cv2.line(img_original, points[0], points[-1], color=(0, 0, 255), thickness=3)
img_original = cv2.circle(img_original, earth_center, int(apparent_earth_radius), (0, 255, 0), 3,
                          lineType=cv2.LINE_AA)  # Earth Horizon
img_original = cv2.circle(img_original, np.round(moon_position).astype(int), int(moon_radius), (0, 255, 0), 3)  # Moon

# Cross-hairs
img_original = cv2.line(img_original, (0, int(img_original.shape[0] / 2)),
                        (img_original.shape[1], int(img_original.shape[0] / 2)), thickness=1, color=(255, 255, 255))
img_original = cv2.line(img_original, (int(img_original.shape[1] / 2), 0),
                        (int(img_original.shape[1] / 2), img_original.shape[0]), thickness=1, color=(255, 255, 255))
cv2.imwrite("out/4-augmented.jpg", img_original)

# Jan Rechnung
alpha = math.acos(6_371_000 / beesat9_eci.position.length().m)
beta = math.pi / 2 - alpha  # der Winkel zwischen Satellit und Erdhorziont

L = math.cos(roll_angle) * earth_edge_relative
vert_camera_angle_radians = math.radians(2 * 11.5)  # der vertikale Öffnungswinkel Beesat-9  in radian
omega = vert_camera_angle_radians / math.cos(
    roll_angle)  # der wahre Öffungswinkel senkrecht zur Erdtangente (durch drehung vom KOS wird großer als original)

c = 1200 / math.cos(roll_angle)  # das Bild ist horizontal 1200 pixel groß
epsilon = L / c * omega
pitch_angle = -(math.pi / 2 - beta - epsilon)  # Der Nickwinkel relativ zur Flugrichtung (Drehung nach oben = positiv)
print("Pitch Angle:", math.degrees(pitch_angle))

# Moon soll linie
image_yaw = moon_position_relativ[0] / 1600 * math.radians(camera_angle_width)
yaw_angle = -(beesat9_apparent_moon_angle_BFK + image_yaw)
# print("Image yaw", image_yaw)
print("Total yaw", math.degrees(yaw_angle))

# pitch_angle = 0
roll_angle = 0
# yaw_angle = 0

# 'xzy', [yaw_angle, pitch_angle, roll_angle]
rotation_BFK_to_KFK = Rotation.from_euler('xzy', [yaw_angle, pitch_angle, roll_angle], degrees=False)
print(rotation_BFK_to_KFK.as_matrix())

transformation_BFK_to_ICRF = Rotation.from_matrix(transformation_BFK_to_ICRF)

rotation_ICRF_to_KFK = transformation_BFK_to_ICRF * rotation_BFK_to_KFK.inv()

visualise_bodies(beesat9_eci, transformation_BFK_to_ICRF, rotation_ICRF_to_KFK, beesat9_moon_vector)

print("Final Euler Angles", rotation_ICRF_to_KFK.as_euler("xzy", degrees=True))
print("Final Quat.", rotation_ICRF_to_KFK.as_quat())

cv2.imshow("IMG2", img_original)
cv2.waitKey(0)
