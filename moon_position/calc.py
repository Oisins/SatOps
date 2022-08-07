import numpy as np
from ephem import Observer, Moon
from skyfield.api import load, wgs84
from datetime import datetime

from skyfield.sgp4lib import EarthSatellite
from skyfield.timelib import Timescale

ts = load.timescale()

#timestamp = ts.utc(2022, 2, 15, 12, 36, 43)
#timestamp = ts.utc(2022, 7, 23, 19, 10, 0)
timestamp = ts.utc(2022, 7, 3, 6, 27, 52)

line1 = '1 44412U 19038AC  22045.39596195  .00006669  00000-0  36191-3 0  9996'
line2 = '2 44412  97.6206  14.1119 0020861 195.3802 164.6798 15.14703389144055'

line1 = '1 44412U 19038AC  22199.84785391  .00009760  00000+0  49051-3 0  9997'
line2 = '2 44412  97.6372 169.3721 0021063  30.9471 329.2998 15.17278340167459'
beesat9 = EarthSatellite(line1, line2, 'Beesat 9', ts)

planets = load('de405.bsp')
earth = planets['earth']
moon = planets['moon']

earth_center = Observer()
earth_center.lon = '0'
earth_center.lat = '0'
earth_center.elevation = -6371000
earth_center.date = "2022-07-23 19:10:0"


moon_earth = Moon()
moon_earth.compute(earth_center)
print("Az", moon_earth.az)
print("Ra", moon_earth.a_ra)
print("Dec", moon_earth.a_dec)

# barycentric = earth.at(timestamp).observe(moon)
# ra, dec, distance = moon_earth.az()
# print(ra)
# print(dec)
# print(distance)
print("")
barycentric = (earth + beesat9).at(timestamp).observe(moon) # im ICRF???
print("!!!", barycentric.position)
print("!!!", barycentric.position.length())
ra, dec, distance = barycentric.radec()
print(ra)
print(dec)
print(distance)

# stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=cubesat&FORMAT=tle'
# satellites = load.tle_file(stations_url)
# satellites = {sat.name: sat for sat in satellites}
# print('Loaded', len(satellites), 'satellites')

# beesat9 = satellites["BEESAT 9"]

now = beesat9.at(timestamp)

print("--- von Vici eingefügt --- ")

barycentric = (earth + beesat9).at(timestamp).observe(moon)
print("!!!", barycentric.position)
print("!!!", barycentric.position.length())
position_vector = barycentric.position.m

position_vector_norm = position_vector / np.linalg.norm(position_vector)
print(position_vector_norm)