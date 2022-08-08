import math

import cv2
import numpy as np
from scipy.spatial.transform import Rotation

from moon_position.moon_position import satellite_apparent_moon_angle_BFK, beesat9_eci, \
    transformation_ICRF_to_BFK, satellite_moon_vector
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
edge_points = find_earth_edge(im_earth)
im_earth *= 255
im_earth = cv2.cvtColor(im_earth, cv2.COLOR_GRAY2RGB)
for point in edge_points:
    im_earth = cv2.circle(im_earth, point, radius=0, color=(0, 0, 255), thickness=-1)

# cv2.imshow("IMG2", cv2.resize(im_earth, fx=0.5, fy=0.5, dsize=None))
# cv2.waitKey(0)
apparent_earth_radius, earth_center = find_earth_circle(edge_points)

# Place chord on earths edge and calculate slope
m_sekante = (edge_points[0][1] - edge_points[-1][1]) / (edge_points[0][0] - edge_points[-1][0])
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
img_original = cv2.line(img_original, edge_points[0], edge_points[-1], color=(0, 0, 255), thickness=3)
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
vert_camera_angle_radians = math.radians(camera_angle_height)  # der vertikale Öffnungswinkel Beesat-9  in radian
omega = vert_camera_angle_radians / math.cos(
    roll_angle)  # der wahre Öffungswinkel senkrecht zur Erdtangente (durch drehung vom KOS wird großer als original)

c = image_height / math.cos(roll_angle)  # das Bild ist horizontal 1200 pixel groß
epsilon = L / c * omega
pitch_angle = -(beta - epsilon)  # Der Nickwinkel relativ zur Flugrichtung (Drehung nach oben = positiv)
print("Pitch Angle:", math.degrees(pitch_angle))

# Moon soll linie
image_yaw = moon_position_relativ[0] / image_width * math.radians(camera_angle_width)
yaw_angle = -(satellite_apparent_moon_angle_BFK + image_yaw)
# print("Image yaw", image_yaw)
# print("Total yaw", math.degrees(yaw_angle))

#pitch_angle = 0
roll_angle = 0
#yaw_angle = math.radians(90)
#yaw_angle = 0
# yaw_angle = beesat9_apparent_moon_angle_BFK  # Drehung um Z_Achse

# Die Kamera zeigt im Körperfesten Koordinatensystem in Z-Richtung. Mit der Transformation wird die Anbringung der
# Kamera kompensiert, sodass Drehungen der Konvention z=gieren, y=nicken, x=rollen folgen.
transformation_BFK_Camera = Rotation.from_matrix(np.array([
    [0, 0, 1],
    [0, -1, 0],
    [1, 0, 0]
]))
print("Camera\n", transformation_BFK_Camera.as_matrix())

# 'xzy', [yaw_angle, pitch_angle, roll_angle], sind das die Winkel vom Pixel- zum BFK?
# Vorher zyx
# Vorher
transformation_camera_to_target = Rotation.from_euler("XYZ", [roll_angle, pitch_angle, yaw_angle], degrees=False)

# hier Winkel minus ICRF-Winkel reintun, diese Winkel ins ICRF und dann diese Trafo anwenden, ist pixel zu bahnfest?

print("BFK to KFK:\n", transformation_camera_to_target.as_matrix())  # trafo north east down cs to body fixed cs

# richtige_rot = rotation_BFK_to_KFK.as_euler("xzy", degrees=True) - transformation_BFK_to_ICRF.as_euler("xzy", degrees=True)  # euler - bahnfest
# print("richtig:", richtige_rot)
#
# euler_winkel = richtige_rot + transformation_BFK_to_ICRF.as_euler("xzy", degrees=True)
# print("Euler-Winkel", euler_winkel)
#
# [ra_ICRF, pa_ICRF, ya_ICRF] = transformation_BFK_to_ICRF * [roll_angle, pitch_angle, yaw_angle]
# rot_ICRF_to_kf = Rotation.from_euler("xyz", [ra_ICRF, pa_ICRF, ya_ICRF], degrees=False) # das hier stimmt nicht
# [ra_kf, pa_kf, ya_kf] =  rot_ICRF_to_kf *  [ra_ICRF, pa_ICRF, ya_ICRF]
# print("Angles:", [ra_kf, pa_kf, ya_kf])

# Transformationen: ECI -> Bahnfest (BFK) -> Kamera -> Target

transformation_ICRF_to_target = transformation_ICRF_to_BFK * transformation_BFK_Camera * transformation_camera_to_target.inv()
transformation_ICRF_to_camera = transformation_ICRF_to_BFK * transformation_BFK_Camera
final_rotation = Rotation.from_euler('xyz', [transformation_ICRF_to_target.as_euler("xzy", degrees=False)], degrees=False)
print("final", final_rotation.as_euler("xyz", degrees=True))
visualise_bodies(beesat9_eci, transformation_ICRF_to_BFK, transformation_ICRF_to_target, satellite_moon_vector)

print("Final Euler Angles", transformation_ICRF_to_target.as_euler("xzy", degrees=True))
print("Final Quat.", transformation_ICRF_to_target.as_quat())

# cv2.imshow("IMG2", img_original)
# cv2.waitKey(0)


# Euler-Winkel im ICRF-System darstellen
# dann Sequenz auf diese dargestellten Winkel anwenden
