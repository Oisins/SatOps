import cv2
import matplotlib.pyplot as plt
# Bild einbinden
import numpy as np

img = cv2.imread('csm_Beesat2_Maldives-06-04-2020_c4a2fae91a.jpg')

# Bild in graustufen konvertieren
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Bild anzeigen
bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]
# a = np.bincount(gray.ravel())
# plt.plot(a)
# plt.show()
cv2.imshow('AP5-Bild1', bw)

# Bild offen halten und dann wieder schließen
cv2.waitKey(0)
cv2.destroyAllWindows()

# Tangente an Erde legen
