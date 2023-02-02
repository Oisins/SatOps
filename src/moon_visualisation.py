# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

from src.moon_position import calculate_moon_vector


def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])


def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)


def visualise_bodies(satellite_eci, moon_eci, rotation_ECI_to_LVLH, rotation_ICRF_to_KFK):
    plt.figure()
    ax = plt.axes(projection='3d')

    satellite_postion = satellite_eci.position.m

    ax.quiver(*satellite_postion, *(rotation_ECI_to_LVLH.apply(np.array([1, 0, 0]) * 1e6)), color='red')
    ax.quiver(*satellite_postion, *(rotation_ECI_to_LVLH.apply(np.array([0, 1, 0]) * 1e6)), color='green')
    ax.quiver(*satellite_postion, *(rotation_ECI_to_LVLH.apply(np.array([0, 0, 1]) * 1e6)), color='blue')

    ax.quiver(*satellite_postion, *(rotation_ICRF_to_KFK.apply(np.array([1, 0, 0]) * 1e6)), color='red',
              linestyle="--")
    ax.quiver(*satellite_postion, *(rotation_ICRF_to_KFK.apply(np.array([0, 1, 0]) * 1e6)), color='green',
              linestyle="--")
    ax.quiver(*satellite_postion, *(rotation_ICRF_to_KFK.apply(np.array([0, 0, 1]) * 1e6)), color='blue',
              linestyle="--")

    ax.quiver(*satellite_postion, *(calculate_moon_vector(satellite_eci, moon_eci) / 100), color='orange')

    # Draw Earth as 3D Mesh Sphere
    # https://stackoverflow.com/a/11156353
    earth_radius = 6371000

    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)

    x, y, z = x * earth_radius, y * earth_radius, z * earth_radius
    ax.plot_wireframe(x, y, z, color="k")  # Earth

    # plt.plot(*beesat9_eci.position.m, 'bo')  # Beesat9
    # plt.plot(*moon_eci.position.m, 'go')  # Moon
    ax.set_box_aspect([1, 1, 1])

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    set_axes_equal(ax)
    plt.show()
