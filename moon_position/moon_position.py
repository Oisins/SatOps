# -*- coding: utf-8 -*-
import math

import numpy as np
from scipy.spatial.transform import Rotation
from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite

from .dictionary_satellites import beesat4, katalog1

mission = katalog1

#### Step 1: Create Beesat 9 TLEs, load Earth and create timestamp

ts = load.timescale()
timestamp = ts.utc(*mission["timestamp"])
# timestamp = ts.utc(2022, 8, 8, 1, 0, 0)
# timestamp = ts.utc(2022, 6, 3, 6, 27, 51)  # Beesat9 looking directly at moon: 3 Jul 2022 06:27:51.744

beesat9 = EarthSatellite(mission["TLE_line1"], mission["TLE_line2"], 'Beesat 9', ts)

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

# x - rot: Flugrichtung
# y - grün: "Rechter Flügel"
# z - blau: Nadir (zum Erdmittelpunkt)

y = np.cross(position_vector_eci, velocity_vector_eci) / np.linalg.norm(
    np.cross(position_vector_eci, velocity_vector_eci))
z = -position_vector_eci / np.linalg.norm(position_vector_eci)
x = np.cross(z, y)
print("x:", x)
print("y:", y)
print("z:", z)

# Step 2.3: Construct transformation matrix
transformation_ICRF_to_BFK = Rotation.from_matrix(np.column_stack([x, y, z]))
print(transformation_ICRF_to_BFK.as_matrix())

# print(transformation_BFK_to_ICRF @ np.array([0, 0, 1]))

# Step 3: Calculate Satellite to Moon vector
satellite_moon_vector = (earth + beesat9).at(timestamp).observe(moon)

satellite_moon_vector_bfk = transformation_ICRF_to_BFK.apply(satellite_moon_vector.position.m)
satellite_apparent_moon_angle_BFK = np.arctan(satellite_moon_vector_bfk[2] / satellite_moon_vector_bfk[1])

print("Beesat9 -> Moon (BFK):", satellite_moon_vector_bfk / np.linalg.norm(satellite_moon_vector_bfk))
print("Apparent Moon angle:", math.degrees(satellite_apparent_moon_angle_BFK))
