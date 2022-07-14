import cv2
import numpy as np


def findCircle(x1, y1, x2, y2, x3, y3):
    x12 = x1 - x2
    x13 = x1 - x3

    y12 = y1 - y2
    y13 = y1 - y3

    y31 = y3 - y1
    y21 = y2 - y1

    x31 = x3 - x1
    x21 = x2 - x1

    # x1^2 - x3^2
    sx13 = pow(x1, 2) - pow(x3, 2)

    # y1^2 - y3^2
    sy13 = pow(y1, 2) - pow(y3, 2)

    sx21 = pow(x2, 2) - pow(x1, 2)
    sy21 = pow(y2, 2) - pow(y1, 2)

    f = (((sx13) * (x12) + (sy13) *
          (x12) + (sx21) * (x13) +
          (sy21) * (x13)) // (2 *
                              ((y31) * (x12) - (y21) * (x13))))

    g = (((sx13) * (y12) + (sy13) * (y12) +
          (sx21) * (y13) + (sy21) * (y13)) //
         (2 * ((x31) * (y12) - (x21) * (y13))))

    c = (-pow(x1, 2) - pow(y1, 2) -
         2 * g * x1 - 2 * f * y1)

    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
    # where centre is (h = -g, k = -f) and
    # radius r as r^2 = h^2 + k^2 - c
    h = -g
    k = -f
    sqr_of_r = h * h + k * k - c

    # r is the radius
    r = round(np.sqrt(sqr_of_r), 5)

    print("Centre = (", h, ", ", k, ")")
    print("Radius = ", r)

    return h, k, r


img_grey = cv2.imread("bilder/csm_Beesat2_Maldives-06-04-2020_c4a2fae91a.jpg", cv2.IMREAD_GRAYSCALE)

im_bw = cv2.threshold(img_grey, 30, 255, cv2.THRESH_BINARY)[1]

print(im_bw.shape)


def find_thresh(x, img):
    #                         x, y
    return x, np.argmax(im_bw[:, x] > 0)


x1, y1 = find_thresh(0, im_bw)
x2, y2 = find_thresh(int(im_bw.shape[1]/2), im_bw)
x3, y3 = find_thresh(im_bw.shape[0], im_bw)
print(x1, y1)
print(x2, y2)
print(x3, y3)

x, y, r = findCircle(x1, y1, x2, y2, x3, y3)

im_rgb = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2RGB)
im = cv2.circle(im_rgb, (x, y), int(r), (0, 0, 255), 2)

cv2.imshow("IMG", im)
cv2.waitKey(0)
