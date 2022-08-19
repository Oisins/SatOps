import math

#                  width                  height
beesat4_camera = [math.radians(11.5 * 2), math.radians(8.5 * 2)]
beesat9_camera = [math.radians(15 * 2), math.radians(11.5 * 2)]

beesat4 = {
    "description": 'Beesat-4 erstes Experiment',
    "TLE_line1": '1 41619U 16040W   22218.61421938  .00008402  00000+0  27192-3 0  9998',
    "TLE_line2": '2 41619  97.2136 267.9333 0007342 301.1193  58.9328 15.32264169328409',
    "date_time": '19 Jul 2022 11:19:21Z',
    "timestamp": (2022, 7, 19, 11, 19, 4),
    "image_file": "B4-Slot11-Horizon.jpg",
    "camera": beesat4_camera,
    "reference_quaternions": [0.3589, 0.6074, 0.46, 0.5389]
}

# TODO: Enter data
beesat9 = {
    "description": 'Beesat-9 4th Experiment',
    "TLE_line1": '1 44412U 19038AC  22219.16926898  .00004635  00000-0  23377-3 0  9994',
    "TLE_line2": '2 44412  97.6382 188.8558 0018684 323.6628  36.3335 15.17501972170382',
    "date_time": '5 Aug 2022 06:33:22Z',
    "timestamp": (2022, 8, 5, 6, 33, 22),
    "image_file": "2022-08-05_06-33-09_Earth-Horizon-Moon_1.jpg",
    "camera": beesat9_camera,
    "reference_quaternions": [0.6952, -0.4394, -0.0746, 0.5639]
}

stk_simulation = {
    "TLE_line1": '1 44412U 19038AC  22220.48804915  .00007782  00000+0  38970-3 0  9996',
    "TLE_line2": '2 44412  97.6380 190.1861 0018557 318.7515  41.2315 15.17523139170586',
    "date_time": '8 Aug 2022 01:00:00Z',
    "experiment": 'Beesat-9 STK Simulation',
}

katalog1 = {
    "description": 'Katalog Image of Moon and Earth (Beesat-9)',
    "TLE_line1": '1 44412U 19038AC  22045.39596195  .00006669  00000-0  36191-3 0  9996',
    "TLE_line2": '2 44412  97.6206  14.1119 0020861 195.3802 164.6798 15.14703389144055',
    "date_time": '15 Feb 2022 12:36:43Z',
    "timestamp": (2022, 2, 15, 12, 36, 43),
    "image_file": "9-7.jpg",
    "camera": beesat9_camera,
    "reference_quaternions": [-0.490834, 0.395866, 0.775337, 0.0349882]
}

__all__ = ["beesat4", "beesat9", "katalog1", "stk_simulation"]
