from enum import IntEnum


class TrackType(IntEnum):
    invalid = 0
    true_track_angle = 1
    magnetic_heading = 2
    true_heading = 3


class Integrity(IntEnum):
    """
    NIC
    (HPL)
    """

    unknown = 0
    """
    Unknown
    """
    less_than_20_nm = 1
    """
    < 20.0 NM
    """
    less_than_8_nm = 2
    """
    < 8.0 NM
    """
    less_than_4_nm = 3
    """
    < 4.0 NM
    """
    less_than_2_nm = 4
    """
    < 2.0 NM
    """
    less_than_1_nm = 5
    """
    < 1.0 NM
    """
    less_than_0_6_nm = 6
    """
    < 0.6 NM
    """
    less_than_0_2_nm = 7
    """
    < 0.2 NM
    """
    less_than_0_1_nm = 8
    """
    < 0.1 NM
    """
    less_than_75_m_hpl_and_112_m_vpl = 9
    """
    HPL < 75 m and VPL < 112 m
    """
    less_than_25_m_hpl_and_37_5_m_vpl = 10
    """
    HPL < 25 m and VPL < 37.5 m
    """
    less_than_7_5_m_hpl_and_11_m_vpl = 11
    """
    HPL < 7.5 m and VPL < 11 m
    """


class Accuracy(IntEnum):
    """
    NACp
    (HFOM)
    """

    unknown = 0
    """
    Unknown
    """
    less_than_10_nm = 1
    """
    < 10.0 NM
    """
    less_than_4_nm = 2
    """
    < 4.0 NM
    """
    less_than_2_nm = 3
    """
    < 2.0 NM
    """
    less_than_1_nm = 4
    """
    < 1.0 NM
    """
    less_than_0_5_nm = 5
    """
    < 0.5 NM
    """
    less_than_0_3_nm = 6
    """
    < 0.3 NM
    """
    less_than_0_1_nm = 7
    """
    < 0.1 NM
    """
    less_than_0_05_nm = 8
    """
    < 0.05 NM
    """
    less_than_30_m_hfom_and_45_m_vfom = 9
    """
    HFOM < 30 m and VFOM < 45 m
    """
    less_than_10_m_hfom_and_15_m_vfom = 10
    """
    HFOM < 10 m and VFOM < 15 m
    """
    less_than_3_m_hfom_and_4_m_vfom = 11
    """
    HFOM < 3 m and VFOM < 4 m
    """


class AddressType(IntEnum):
    ads_b_icao = 0
    """
    ADS-B with ICAO address
    """
    ads_b_self_assigned = 1
    """
    ADS-B with Self-assigned address
    """
    tis_b_icao = 2
    """
    TIS-B with ICAO address
    """
    tis_b_track_file_id = 3
    """
    TIS-B with track file ID
    """
    surface_vehicle = 4
    """
    Surface Vehicle
    """
    ground_station_beacon = 5
    """
    Ground Station Beacon
    """


class EmitterCategory(IntEnum):
    no_aircraft_type_information = 0
    """
    no aircraft type information
    """
    light = 1
    """
    Light (ICAO) < 15 500 lbs
    """
    small = 2
    """
    Small - 15 500 to 75 000 lbs
    """
    large = 3
    """
    Large - 75 000 to 300 000 lbs
    """
    high_vortex_large = 4
    """
    High Vortex Large (e.g., aircraft such as B757)
    """
    heavy = 5
    """
    Heavy (ICAO) - > 300 000 lbs
    """
    highly_maneuverable = 6
    """
    Highly Maneuverable > 5G acceleration and high speed
    """
    rotorcraft = 7
    """
    Rotorcraft
    """
    glider_or_sailplane = 9
    """
    Glider/sailplane
    """
    lighter_than_air = 10
    """
    Lighter than air
    """
    parachutist_or_sky_diver = 11
    """
    Parachutist/sky diver
    """
    ultra_light_or_hang_glider_or_paraglider = 12
    """
    Ultra light/hang glider/paraglider
    """
    unmanned_aerial_vehicle = 14
    """
    Unmanned aerial vehicle
    """
    space_or_transatmospheric_vehicle = 15
    """
    Space/transatmospheric vehicle
    """
    surface_emergency_vehicle = 17
    """
    Surface vehicle — emergency vehicle
    """
    surface_service_vehicle = 18
    """
    Surface vehicle — service vehicle
    """
    point_obstacle = 19
    """
    Point Obstacle (includes tethered balloons)
    """
    cluster_obstacle = 20
    """
    Cluster Obstacle
    """
    line_obstacle = 21
    """
    Line Obstacle
    """


class EmergencyPriorityCode(IntEnum):
    no_emergency = 0
    general_emergency = 1
    medical_emergency = 2
    minimum_fuel = 3
    no_communication = 4
    unlawful_interference = 5
    downed_aircraft = 6
