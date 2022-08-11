# -*- coding: utf-8 -*-
import math

import numpy as np
from scipy.spatial.transform import Rotation
from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite


def create_bodies(mission):
    # Step 1: Load TLEs, load Earth and create timestamp
    ts = load.timescale()
    timestamp = ts.utc(*mission["timestamp"])

    satellite = EarthSatellite(mission["TLE_line1"], mission["TLE_line2"], 'Beesat 9', ts)

    planets = load('de405.bsp')
    earth = planets['earth']
    moon = planets['moon']

    # Load Moon
    moon_eci = moon.at(timestamp) - earth.at(timestamp)
    # moon_icrf = moon.at(timestamp)
    # print("Moon Position Vector (ECI)", moon_eci.position.m)
    # print("Moon Distance (ECI)", moon_eci.position.length())
    # print("Moon Position Vector (ICRF)", moon_icrf.position.m)
    # print("Moon Distance (ICRF)", moon_icrf.position.length())

    # Step 2.1: Get Position and Velocity vector for Beesat 9 (seems to be in ECI Reference frame)
    satellite_eci = satellite.at(timestamp)

    return moon_eci, satellite_eci


def create_lvlh(satellite_eci):
    """
    Create rotation Matrix for rotating from ECI to LVLH
    Based on:
        https://space.stackexchange.com/questions/33803
        https://space.stackexchange.com/questions/48796

    """

    position_vector_eci = satellite_eci.position.m
    velocity_vector_eci = satellite_eci.velocity.m_per_s
    # position_vector_eci = np.array([0, 0, np.linalg.norm(position_vector_eci)])  # fixme: Testing only
    # velocity_vector_eci = np.array([np.linalg.norm(velocity_vector_eci), 0, 0])  # fixme: Testing only

    print("Satellite Position Vector (ECI) in m", position_vector_eci)
    print("Satellite Velocity Vector (ECI) in m/s", velocity_vector_eci)

    # Construct unit vectors for LVLH Reference frame
    # x - rot: Flugrichtung
    # y - grün: "Rechter Flügel"
    # z - blau: Nadir (zum Erdmittelpunkt)

    y = -np.cross(position_vector_eci, velocity_vector_eci) / np.linalg.norm(
        np.cross(position_vector_eci, velocity_vector_eci))
    z = -position_vector_eci / np.linalg.norm(position_vector_eci)
    x = -np.cross(z, y)

    # Construct transformation matrix
    rotation_ECI_to_LVLH = Rotation.from_matrix(np.column_stack([x, y, z]))

    print("Rotation ICRF to LVLH:\n", rotation_ECI_to_LVLH.as_matrix())

    return rotation_ECI_to_LVLH


def calculate_moon_vector(satellite_eci, moon_eci):
    return moon_eci.position.m - satellite_eci.position.m


def calculate_apparent_moon_angle(satellite_eci, moon_eci, rotation_ECI_to_LVLH):
    """ Calculate angle to moon in satellites XY-Plane in LVLH reference frame """

    satellite_moon_vector = calculate_moon_vector(satellite_eci, moon_eci)

    satellite_moon_vector_lvlh = rotation_ECI_to_LVLH.inv().apply(satellite_moon_vector)
    apparent_moon_angle = np.arctan(satellite_moon_vector_lvlh[1] / satellite_moon_vector_lvlh[0])

    print("Apparent Moon angle:", math.degrees(apparent_moon_angle))

    return apparent_moon_angle
