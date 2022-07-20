# -*- coding: utf-8 -*-
import ephem

moon = ephem.Moon()
# moon = ephem.Moon('2022-01-01 1:00:00')
moon.compute('2022-02-15 12:36:43')

print("Ra", moon.ra)
print("Dec", moon.dec)
