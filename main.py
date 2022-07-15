import cv2
import numpy as np

from utils import find_earth_circle, segment_earth_moon

img_grey = cv2.imread("bilder/csm_Beesat9_Moon-01-04-2020_61fb3aba42.jpg", cv2.IMREAD_GRAYSCALE)

im_bw = cv2.threshold(img_grey, 30, 255, cv2.THRESH_BINARY)[1]
im_gauss = cv2.Laplacian(im_bw, cv2.CV_8U)


def find_line(x, img):
    #                         x, y
    return x, np.argmax(img[:, x] > 0)


earth_mask, moon_mask = segment_earth_moon(im_bw)

im_earth = im_bw & earth_mask

points = np.array([find_line(x, im_earth) for x in range(im_gauss.shape[1])])

earth_radius, earth_center = find_earth_circle(points)

im_bgr = cv2.cvtColor(im_bw.astype(np.float32), cv2.COLOR_GRAY2BGR)

img_rgb = cv2.line(im_bgr, points[0], points[-1], color=(0, 0, 255))

m_sekante = (points[0][1] - points[-1][1]) / (points[0][0] - points[-1][0])
m_radius = -1 / m_sekante

dx = np.cos(np.arctan(m_radius)) * earth_radius
dy = dx * m_radius

print(m_sekante)
print(m_radius)

y = earth_center[1] + dy
x = earth_center[0] + dx
print("Earth center", earth_center)
print("Earth radius", earth_radius)
print(y)


im_rgb = cv2.circle(im_bgr, earth_center, int(earth_radius), (0, 255, 0), 1)
im_rgb = cv2.circle(im_rgb, np.round([x, y]).astype(int), 5, (0, 0, 255), -1)
im2 = cv2.resize(img_rgb, (0, 0), fx=5, fy=5)

cv2.imshow("IMG2", im2)
cv2.waitKey(0)
