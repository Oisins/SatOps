# -*- coding: utf-8 -*-
import math

import ephem

moon = ephem.Moon()
moon.compute('2022-02-15 12:36:43')

print("Ra: ", moon.ra)
print("Dec: ", moon.dec)

beesat9 = ephem.readtle("Beesat 9",
                        "1 44412U 19038AC  22046.18869775  .00005670  00000-0  30817-3 0  9991",
                        "2 44412  97.6210  14.9061 0020921 192.4752 167.5964 15.14711800144170")
beesat9.compute('2022-02-15 12:36:43')

print("Ra", ephem.degrees(moon.ra + beesat9.ra))
print("Dec", ephem.degrees(moon.dec + beesat9.dec))

# beesat9.observe(moon)

print(beesat9.velocity)


print(moon.hlat)
# print(math.arccos(((Höhe Sat/a) * (b-a)) / Abstand Sat zu Mond))
