import cv2
import numpy as np
import scipy.optimize


def segment_earth_moon(img):
    """
    Finds eath and moon in image and creates boolean masks for both
    :param img: b/w image of earth and moon
    :return:
    """

    num_labels, labels_im = cv2.connectedComponents(img)

    assert num_labels == 3, f"Number of Object should be 2 ({num_labels - 1} found)"

    mask1 = labels_im == 1
    mask2 = labels_im == 2

    mask1_is_moon = np.sum(mask1) < np.sum(mask2)
    moon_mask, earth_mask = (mask1, mask2) if mask1_is_moon else (mask2, mask1)

    img_earth = img & earth_mask
    img_moon = img & moon_mask

    return img_earth, img_moon


def fit_horizon_circle(points):
    """ Given a list of points on the circumference of the (perceived) earth, calculate radius and center """

    def calc_R(xc, yc):
        """ calculate the distance of each 2D points from the center (xc, yc) """
        return np.sqrt((x - xc) ** 2 + (y - yc) ** 2)

    def f_2(c):
        """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
        Ri = calc_R(*c)
        return Ri - Ri.mean()

    x = points[:, 0]
    y = points[:, 1]

    x_m = np.mean(x)
    y_m = np.mean(y)
    center_estimate = x_m, y_m
    result = scipy.optimize.least_squares(f_2, center_estimate)

    assert result.success, "Optimizer failed to find circle"

    Ri_2 = calc_R(*result.x)
    radius = Ri_2.mean()

    return radius, np.round(result.x).astype(int)


def find_moon(img):
    contours, hierarchy = cv2.findContours(img, 1, 2)
    (x, y), radius = cv2.minEnclosingCircle(contours[0])

    # img = cv2.cvtColor(img.astype(np.float32), cv2.COLOR_GRAY2BGR)

    # img = cv2.circle(img, np.round([x, y]).astype(int), int(radius), (0, 0, 255), -1)
    # img = cv2.resize(img, (0, 0), fx=5, fy=5)

    return np.array((x, y)), radius


def find_earth_edge(img):
    """ Return list of points (x, y) that represent the edge of the earth """
    points = []

    for x, col in enumerate(img.T):
        if np.sum(col) == 0:
            # TODO: Was hier tun?
            continue
        # TODO: Was hier tun?
        points.append((x, np.argmax(col)))

        #                         x, y
        # TODO: Wie verhält sich argmax wenn keine Kante da ist, also alle werte 0 sind und es kein maximum gibt
        #       -> Rückgabewert dieser Methode anpassen, sodass man erkennen kann, dass keine Kante vorhanden ist in der spalte
        #       -> z.B. return nan

    return np.array(points)
