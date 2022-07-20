# -*- coding: utf-8 -*-
import math

import numpy as np
from ephem import Moon
from matplotlib import pyplot as plt
from skyfield.sgp4lib import EarthSatellite
from skyfield.api import load

#### Step 1: Create Beesat 9 TLEs, load Earth and create timestamp
ts = load.timescale()
timestamp = ts.utc(2022, 2, 15, 12, 36, 43)
# timestamp = ts.utc(2022, 6, 3, 6, 27, 51)  # Beesat9 looking directly at moon: 3 Jul 2022 06:27:51.744

# TLE for 2022-02-15
line1 = '1 44412U 19038AC  22045.39596195  .00006669  00000-0  36191-3 0  9996'
line2 = '2 44412  97.6206  14.1119 0020861 195.3802 164.6798 15.14703389144055'
beesat9 = EarthSatellite(line1, line2, 'Beesat 9', ts)

planets = load('de405.bsp')
earth = planets['earth']
moon = planets['moon']

#### Load Moon
moon_eci = moon.at(timestamp) - earth.at(timestamp)
moon_icrf = moon.at(timestamp)
print("Moon Position Vector (ECI)", moon_eci.position.m)
print("Moon Distance (ECI)", moon_eci.position.length())
print("Moon Position Vector (ICRF)", moon_icrf.position.m)
print("Moon Distance (ICRF)", moon_icrf.position.length())

#### Step 2: Create VVLH (or LVLH) Coordinate System / Transformation
# VVLH can probably be created from the ECI instead of ICRF (or J2000) as
# https://space.stackexchange.com/questions/33803
# https://space.stackexchange.com/questions/48796

# Step 2.1: Get Position and Velocity vector for Beesat 9 (seems to be in ECI Reference frame)
beesat9_eci = beesat9.at(timestamp)
beesat9_icrf = (earth + beesat9).at(timestamp)

position_vector_eci = beesat9_eci.position.m
velocity_vector_eci = beesat9_eci.velocity.m_per_s
print("Beesat9 Position Vector (ECI) in m", position_vector_eci)
print("Beesat9 Velocity Vector (ECI) in m/s", velocity_vector_eci)

# Step 2.2: Construct unit vectors for LVLH Reference frame
z = np.cross(position_vector_eci, velocity_vector_eci) / np.linalg.norm(
    np.cross(position_vector_eci, velocity_vector_eci))
x = position_vector_eci / np.linalg.norm(position_vector_eci)
y = np.cross(z, x)
print("x:", x)
print("y:", y)
print("z:", z)

transformation_BFK_to_ICRF = np.column_stack([x, y, z])
print(transformation_BFK_to_ICRF)

print(transformation_BFK_to_ICRF @ np.array([0, 0, 1]))

# Step 2.3: Construct transformation matrix

# Step 3: Transform YPR relative to LVLH reference frame to ECI

# Step 4: Compare with ACS Data


# Step X: Calculate Beesat9 to Moon vector
beesat9_moon_vector = (earth + beesat9).at(timestamp).observe(moon)
print("!!!", beesat9_moon_vector.position)
print("!!!", beesat9_moon_vector.position.length())

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.quiver(0, 0, 0, *(np.array([0, 0, 1])), color='steelblue')
ax.quiver(*beesat9_eci.position.m, *(transformation_BFK_to_ICRF @ np.array([1, 0, 0]) * 1e6), color='red')
ax.quiver(*beesat9_eci.position.m, *(transformation_BFK_to_ICRF @ np.array([0, 1, 0]) * 1e6), color='green')
ax.quiver(*beesat9_eci.position.m, *(transformation_BFK_to_ICRF @ np.array([0, 0, 1]) * 1e6), color='blue')

ax.quiver(*beesat9_eci.position.m, *(beesat9_moon_vector.position.m / 100), color='orange')

# draw sphere
u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)

earth_radius = 6371000
# earth_radius = 10e10
x, y, z = x * earth_radius, y * earth_radius, z * earth_radius
ax.plot_wireframe(x, y, z, color="k")

plt.plot(*beesat9_eci.position.m, 'bo')
# plt.plot(*moon_eci.position.m, 'go')  # Moon

# ax.set_xlim([-1e11, 1e11])
# ax.set_ylim([-1e11, 1e11])
# ax.set_zlim([-1e11, 1e11])

beesat9_moon_vector_bfk = np.linalg.inv(transformation_BFK_to_ICRF) @ beesat9_moon_vector.position.m
print("Beesat9 -> Moon (BFK):", beesat9_moon_vector_bfk / np.linalg.norm(beesat9_moon_vector_bfk))
print("Apparent Moon angle:", math.degrees(np.arctan(beesat9_moon_vector_bfk[2] / beesat9_moon_vector_bfk[1])))
plt.show()
