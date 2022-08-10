# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

from moon_position.moon_position import moon_eci


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


def visualise_bodies(position_vector_eci, transformation_BFK_to_ICRF, rotation_ICRF_to_KFK, beesat9_moon_vector):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.quiver(0, 0, 0, *(np.array([0, 0, 1])), color='steelblue')
    ax.quiver(*position_vector_eci, *(transformation_BFK_to_ICRF.apply(np.array([1, 0, 0]) * 1e6)), color='red')
    ax.quiver(*position_vector_eci, *(transformation_BFK_to_ICRF.apply(np.array([0, 1, 0]) * 1e6)), color='green')
    ax.quiver(*position_vector_eci, *(transformation_BFK_to_ICRF.apply(np.array([0, 0, 1]) * 1e6)), color='blue')

    ax.quiver(*position_vector_eci, *(rotation_ICRF_to_KFK.apply(np.array([1, 0, 0]) * 1e6)), color='red',
              linestyle="--")
    ax.quiver(*position_vector_eci, *(rotation_ICRF_to_KFK.apply(np.array([0, 1, 0]) * 1e6)), color='green',
              linestyle="--")
    ax.quiver(*position_vector_eci, *(rotation_ICRF_to_KFK.apply(np.array([0, 0, 1]) * 1e6)), color='blue',
              linestyle="--")

    ax.quiver(*position_vector_eci, *(beesat9_moon_vector.position.m / 100), color='orange')

    # draw sphere
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)

    earth_radius = 6371000
    x, y, z = x * earth_radius, y * earth_radius, z * earth_radius
    ax.plot_wireframe(x, y, z, color="k")  # Earth

    # plt.plot(*beesat9_eci.position.m, 'bo')  # Beesat9
    # plt.plot(*moon_eci.position.m, 'go')  # Moon
    ax.set_box_aspect([1, 1, 1])
    set_axes_equal(ax)
    plt.show()
