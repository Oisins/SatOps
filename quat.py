import pandas as pd
from scipy.spatial.transform import Rotation

rot = Rotation.from_quat([-0.490834, 0.395866, 0.775337, 0.0349882])
rot_euler = rot.as_euler('xyz', degrees=True)
print(rot_euler)
rot_euler = rot.as_euler('yxz', degrees=True)
print(rot_euler)
rot_euler = rot.as_euler('xzy', degrees=True)
print(rot_euler)