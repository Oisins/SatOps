# -*- coding: utf-8 -*-
import numpy as np
from skyfield.sgp4lib import EarthSatellite
from skyfield.api import load

#### Step 1: Create Beesat 9 TLEs, load Earth and create timestamp
ts = load.timescale()
timestamp = ts.utc(2022, 2, 15, 12, 36, 43)

# TLE for 2022-02-15
line1 = '1 44412U 19038AC  22045.39596195  .00006669  00000-0  36191-3 0  9996'
line2 = '2 44412  97.6206  14.1119 0020861 195.3802 164.6798 15.14703389144055'
beesat9 = EarthSatellite(line1, line2, 'Beesat 9', ts)

planets = load('de405.bsp')
earth = planets['earth']

#### Step 2: Create VVLH (or LVLH) Coordinate System / Transformation
# VVLH can probably be created from the ECI instead of ICRF (or J2000) as
# https://space.stackexchange.com/questions/33803
# https://space.stackexchange.com/questions/48796

# Step 2.1: Get Velocity vector for Beesat 9 (seems to be in ECI Reference frame)
position_vector = (earth + beesat9).at(timestamp).position.m
velocity_vector = (earth + beesat9).at(timestamp).velocity.m_per_s
print(position_vector)
print(velocity_vector)

# Step 2.2: Construct unit vectors for LVLH Reference frame
x = np.cross(position_vector, velocity_vector) / np.linalg.norm(np.cross(position_vector, velocity_vector))
z = position_vector / np.linalg.norm(position_vector)
y = np.cross(x, z)
print("x:", x)
print("y:", y)
print("z:", z)
