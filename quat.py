import pandas as pd
from scipy.spatial.transform import Rotation

rot = Rotation.from_quat([-0.4901, 0.396, 0.7756, 0.035])
rot_euler = rot.as_euler('xyz', degrees=True)
print(rot_euler)
rot_euler = rot.as_euler('yxz', degrees=True)
print(rot_euler)
rot_euler = rot.as_euler('xzy', degrees=True)
print(rot_euler)