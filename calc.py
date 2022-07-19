from skyfield.api import load, wgs84
from datetime import datetime

from skyfield.sgp4lib import EarthSatellite
from skyfield.timelib import Timescale

ts = load.timescale()

timestamp = ts.utc(2022, 2, 15, 12, 36, 43)

line1 = '1 44412U 19038AC  22045.39596195  .00006669  00000-0  36191-3 0  9996'
line2 = '2 44412  97.6206  14.1119 0020861 195.3802 164.6798 15.14703389144055'
beesat9 = EarthSatellite(line1, line2, 'Beesat 9', ts)

# stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=cubesat&FORMAT=tle'
# satellites = load.tle_file(stations_url)
# satellites = {sat.name: sat for sat in satellites}
# print('Loaded', len(satellites), 'satellites')

# beesat9 = satellites["BEESAT 9"]

now = beesat9.at(timestamp)

ra, dec, alt = now.radec()

print(dec)

print(90 + 67 + dec.degrees)
