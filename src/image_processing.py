import cv2


def load_image():
    img_original = cv2.imread("bilder/B4-Slot11-Horizon.jpg")
    img_grey = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    im_bw = cv2.threshold(img_grey, 60, 255, cv2.THRESH_BINARY)[1]

    image_height, image_width, _ = img_original.shape

    return img_original, im_bw, (image_height, image_width)


def filter_edges(img):
    return cv2.Laplacian(img, cv2.CV_8U)