import math

import cv2
import numpy as np
from scipy.spatial.transform import Rotation

from src.dictionary_satellites import *
from src.image_processing import load_image, filter_edges
from src.moon_position import calculate_apparent_moon_angle, create_bodies, create_lvlh
from moon_position.visualisation import visualise_bodies
from utils import fit_horizon_circle, segment_earth_moon, find_moon, find_earth_edge

mission = katalog1
camera_angle_width, camera_angle_height = mission["camera"]

print(f"Running Analysis on {mission['description']}")
# Load image and convert to b/w
img_original, im_bw, (image_height, image_width) = load_image("bilder/" + mission["image_file"])

# cv2.imwrite("out/0-original.jpg", img_original)
# cv2.imwrite("out/1-grey.jpg", img_grey)
# cv2.imwrite("out/2-bw.jpg", im_bw)

# Use Gauss filter to extract edges
im_edges = filter_edges(im_bw)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
cv2.imwrite("out/3-gauss.jpg", cv2.dilate(im_edges, kernel, iterations=2))

moon_eci, satellite_eci = create_bodies(mission=mission)
rotation_ECI_to_LVLH = create_lvlh(satellite_eci)

# Segment Earth and Moon
img_earth, img_moon = segment_earth_moon(im_bw)

# Find Moon in image
moon_position, moon_radius = find_moon(img_moon)

# Determine apparent center of earth and radius
horizon_points = find_earth_edge(img_earth)
img_earth *= 255
img_earth = cv2.cvtColor(img_earth, cv2.COLOR_GRAY2RGB)
for point in horizon_points:
    img_earth = cv2.circle(img_earth, point, radius=0, color=(0, 0, 255), thickness=-1)

apparent_earth_radius, earth_center = fit_horizon_circle(horizon_points)

# Place chord on earths edge and calculate slope
m_sekante = (horizon_points[0][1] - horizon_points[-1][1]) / (horizon_points[0][0] - horizon_points[-1][0])
# m_radius = -1 / m_sekante

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
img_original = cv2.line(img_original, horizon_points[0], horizon_points[-1], color=(0, 0, 255), thickness=3)
img_original = cv2.circle(img_original, earth_center, int(apparent_earth_radius), (0, 255, 0), 3,
                          lineType=cv2.LINE_AA)  # Earth Horizon
img_original = cv2.circle(img_original, np.round(moon_position).astype(int), int(moon_radius), (0, 255, 0), 3)  # Moon

# Cross-hairs
img_original = cv2.line(img_original, (0, int(img_original.shape[0] / 2)),
                        (img_original.shape[1], int(img_original.shape[0] / 2)), thickness=1, color=(255, 255, 255))
img_original = cv2.line(img_original, (int(img_original.shape[1] / 2), 0),
                        (int(img_original.shape[1] / 2), img_original.shape[0]), thickness=1, color=(255, 255, 255))
cv2.imwrite("out/4-augmented.jpg", img_original)

# Winkel zwischen Flugrichtung und Erdtangente bestimmen
beta = math.acos(6_371_000 / satellite_eci.position.length().m)

L = math.cos(roll_angle) * earth_edge_relative
vert_camera_angle_radians = camera_angle_height  # der vertikale Öffnungswinkel Beesat-9 in radiant
moon_angle_2d_img = vert_camera_angle_radians / math.cos(
    roll_angle)  # der wahre Öffungswinkel senkrecht zur Erdtangente (durch drehung vom KOS wird großer als original)

c = image_height / math.cos(roll_angle)
pitch_relative = L / c * moon_angle_2d_img  # Winkel Erdhorizont zu Fadenkreuz
pitch_angle = -(beta - pitch_relative)  # Der Nickwinkel relativ zur Flugrichtung (Drehung nach oben = positiv)
print("Pitch Angle:", math.degrees(pitch_angle))

# Gierwinkel berechnen
# Berechnung der Distanz des Mondes zum Mittelpunkt des Koordinatensystems
distance_center_moon = np.linalg.norm(moon_position_relativ)
# Erklärung für theta: ich berechne den Winkel zwischen der Hypothenuse H_1 und der y-Achse
moon_angle_2d_img = math.asin(moon_position_relativ[0] / distance_center_moon)
psi = moon_angle_2d_img - roll_angle
# Ich drehe das Kooridnatensystem um den Rollwinkel und theta um mit in der neuen x-Achse die Länge L_1 des Gierwinkels zu berechen
c_2 = distance_center_moon * math.sin(psi)  # pixel
image_yaw = c_2 * camera_angle_width / image_width  # relativer Gierwinkel

# image_yaw = moon_position_relativ[0] / image_width * camera_angle_width
apparent_moon_angle = calculate_apparent_moon_angle(satellite_eci, moon_eci, rotation_ECI_to_LVLH)
yaw_angle = -(apparent_moon_angle - image_yaw)
print("Image yaw", math.degrees(image_yaw))
print("Total yaw", math.degrees(yaw_angle))

# pitch_angle = math.radians(-10)
# pitch_angle = 0
# roll_angle = math.radians(10)
# roll_angle = 0
# yaw_angle = math.radians(10)
# yaw_angle = 0
# yaw_angle = beesat9_apparent_moon_angle_BFK  # Drehung um Z_Achse

# Die Kamera zeigt im Körperfesten Koordinatensystem in Z-Richtung. Mit der Transformation wird die Anbringung der
# Kamera kompensiert, sodass Drehungen der Konvention z=gieren, y=nicken, x=rollen folgen.
rotation_camera = Rotation.from_matrix(np.array([
    [0, 0, 1],
    [0, 1, 0],
    [-1, 0, 0]
]))

transformation_camera_to_target = Rotation.from_euler("XYZ", [yaw_angle, pitch_angle, roll_angle], degrees=False)

# Transformationen: ECI -> Bahnfest (LVLH) -> Kamera -> Target
transformation_ICRF_to_target = rotation_ECI_to_LVLH * rotation_camera * transformation_camera_to_target
transformation_ICRF_to_camera = rotation_ECI_to_LVLH * rotation_camera

print("Final Euler Angles", transformation_ICRF_to_target.as_euler("XYZ", degrees=True))
print("Final Quat.", transformation_ICRF_to_target.as_quat())
diff = transformation_ICRF_to_target.inv() * Rotation.from_quat(mission["reference_quaternions"])
print("Angular diff", diff.as_euler("XYZ", degrees=True))
visualise_bodies(satellite_eci, moon_eci, rotation_ECI_to_LVLH, transformation_ICRF_to_target)

cv2.imshow("Augmented Image", img_original)
cv2.waitKey(0)
