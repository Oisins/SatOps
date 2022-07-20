# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt


def visualise_bodies(beesat9_eci, transformation_BFK_to_ICRF, beesat9_moon_vector):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.quiver(0, 0, 0, *(np.array([0, 0, 1])), color='steelblue')
    ax.quiver(*beesat9_eci.position.m, *(transformation_BFK_to_ICRF @ np.array([1, 0, 0]) * 1e6), color='red')
    ax.quiver(*beesat9_eci.position.m, *(transformation_BFK_to_ICRF @ np.array([0, 1, 0]) * 1e6), color='green')
    ax.quiver(*beesat9_eci.position.m, *(transformation_BFK_to_ICRF @ np.array([0, 0, 1]) * 1e6), color='blue')

    ax.quiver(*beesat9_eci.position.m, *(beesat9_moon_vector.position.m / 100), color='orange')

    # draw sphere
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)

    earth_radius = 6371000
    x, y, z = x * earth_radius, y * earth_radius, z * earth_radius
    ax.plot_wireframe(x, y, z, color="k")

    plt.plot(*beesat9_eci.position.m, 'bo')
    # plt.plot(*moon_eci.position.m, 'go')  # Moon

    plt.show()
