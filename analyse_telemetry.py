import datetime

import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation

df = pd.read_csv("telemetry/beesat9_3/APID89-Daten-B9-14.07.22.csv", encoding="UTF-8", sep=";")
df["RecordingTime"] = pd.to_datetime(df["RecordingTime"], utc=True)
df.set_index("RecordingTime", inplace=True)
print(df.describe())

rot = Rotation.from_quat(
    df[["ACS quaternion X []", "ACS quaternion Y []", "ACS quaternion Z []", "ACS quaternion SC []"]])
df[["ACS X", "ACS Y", "ACS Z"]] = rot.as_euler('xyz', degrees=True)

rot = Rotation.from_quat(
    df[["Desired quaternion X []", "Desired quaternion Y []", "Desired quaternion Z []", "Desired quaternion SC []"]])
df[["ACS X_soll", "ACS Y_soll", "ACS Z_soll"]] = rot.as_euler('xyz', degrees=True)

rot = Rotation.from_quat(
    df[["Error Quaternion X []", "Error Quaternion Y []", "Error Quaternion Z []", "Error Quaternion Scalar []"]])
df[["ACS X_err", "ACS Y_err", "ACS Z_err"]] = rot.as_euler('xyz', degrees=True)

# df[["Wheel Accelaration 0 [rpm/s]", "Wheel Accelaration 1 [rpm/s]", "Wheel Accelaration 2 [rpm/s]"]].plot()
# df[["ACS X", "ACS Y", "ACS Z", "ACS X_soll", "ACS Y_soll", "ACS Z_soll"]].plot()
#
# plt.axvline(datetime.datetime(2022, 7, 14, 17, 5, 21), color="red")
# plt.axvline(datetime.datetime(2022, 7, 14, 17, 5, 36), color="red")
# plt.axvline(datetime.datetime(2022, 7, 14, 17, 5, 51), color="red")
# plt.show()
#
df[["ACS X_err", "ACS Y_err", "ACS Z_err"]].plot()

img_start = datetime.datetime(2022, 7, 14, 17, 5, 21)
img_end = datetime.datetime(2022, 7, 14, 17, 5, 51)

plt.axvspan(img_start, img_end, color='red', alpha=.1)
plt.ylim([-25, 40])
plt.title("Abweichung Lageregelung")
plt.xlabel("Zeitpunkt")
plt.ylabel("Abweichung in °")

ax = plt.gca()
ax.annotate("Suspend Mode", xy=(datetime.datetime(2022, 7, 14, 17, 6, 13), 0), xycoords='data',
            xytext=(0.85, 0.6), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=6),
            horizontalalignment='center', verticalalignment='top',
            )
ax.annotate("Bildaufnahme", xy=(img_end, 15), xycoords='data',
            xytext=(0.85, 0.7), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=6),
            horizontalalignment='center', verticalalignment='top',
            )

plt.grid()
plt.savefig("acs_error.png", dpi=500)
plt.show()

df[["Gyro PDH X [deg/s]", "Gyro PDH Y [deg/s]", "Gyro PDH Z [deg/s]"]].plot()
plt.title("Drehraten")
plt.xlabel("Zeitpunkt")
plt.ylabel("Drehrate in °/s")
plt.axvspan(img_start, img_end, color='red', alpha=.1)
plt.annotate("Bildaufnahme", xy=(img_end, 1), xycoords='data',
             xytext=(0.85, 0.7), textcoords='axes fraction',
             arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=6),
             horizontalalignment='center', verticalalignment='top',
             )
plt.grid()
plt.savefig("acs_rotation.png", dpi=500)
plt.show()
