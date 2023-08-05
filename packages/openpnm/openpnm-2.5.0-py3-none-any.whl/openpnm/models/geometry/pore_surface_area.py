r"""

.. autofunction:: openpnm.models.geometry.pore_surface_area.sphere
.. autofunction:: openpnm.models.geometry.pore_surface_area.cube

"""
import numpy as _np


def sphere(target, pore_diameter='pore.diameter', throat_area='throat.area'):
    r"""
    Calculates internal surface area of pore bodies assuming they are spherical
    then subtracts the area of the neighboring throats in a crude way, by
    simply considering the throat cross-sectional area, thus not accounting
    for the actual curvature of the intersection.

    Parameters
    ----------
    target : OpenPNM Object
        The object for which these values are being calculated.  This
        controls the length of the calculated array, and also provides
        access to other necessary thermofluid properties.

    pore_diameter : string
        The dictionary key to the pore diameter array.

    throat_area : string
        The dictioanry key to the throat area array.  Throat areas are needed
        since their insection with the pore are removed from the computation.

    Returns
    -------
    value : NumPy ndarray
        Array containing pore surface area values.

    """
    network = target.project.network
    R = target[pore_diameter]/2
    Asurf = 4*_np.pi*R**2
    Tn = network.find_neighbor_throats(pores=target.Ps, flatten=False)
    Tsurf = _np.array([_np.sum(network[throat_area][Ts]) for Ts in Tn])
    value = Asurf - Tsurf
    return value


def circle(target, pore_diameter='pore.diameter', throat_area='throat.area'):
    r"""
    Calculates internal surface area of pore bodies assuming they are circular
    then subtracts the area of the neighboring throats in a crude way, by
    simply considering the throat cross-sectional area, thus not accounting
    for the actual curvature of the intersection.

    Parameters
    ----------
    target : OpenPNM Object
        The object for which these values are being calculated.  This
        controls the length of the calculated array, and also provides
        access to other necessary thermofluid properties.

    pore_diameter : string
        The dictionary key to the pore diameter array.

    throat_area : string
        The dictioanry key to the throat area array.  Throat areas are needed
        since their insection with the pore are removed from the computation.

    Returns
    -------
    value : NumPy ndarray
        Array containing pore surface area values.

    """
    network = target.project.network
    R = target[pore_diameter]/2
    Asurf = 2*_np.pi*R
    Tn = network.find_neighbor_throats(pores=target.Ps, flatten=False)
    Tsurf = _np.array([_np.sum(network[throat_area][Ts]) for Ts in Tn])
    value = Asurf - Tsurf
    return value


def cube(target, pore_diameter='pore.diameter', throat_area='throat.area'):
    r"""
    Calculates internal surface area of pore bodies assuming they are cubes
    then subtracts the area of the neighboring throats.

    Parameters
    ----------
    target : OpenPNM Object
        The object for which these values are being calculated.  This
        controls the length of the calculated array, and also provides
        access to other necessary thermofluid properties.

    pore_diameter : string
        The dictionary key to the pore diameter array.

    throat_area : string
        The dictioanry key to the throat area array.  Throat areas are needed
        since their insection with the pore are removed from the computation.

    Returns
    -------
    value : NumPy ndarray
        Array containing pore surface area values.

    """
    network = target.project.network
    D = target[pore_diameter]
    Tn = network.find_neighbor_throats(pores=target.Ps, flatten=False)
    Tsurf = _np.array([_np.sum(network[throat_area][Ts]) for Ts in Tn])
    value = 6*D**2 - Tsurf
    return value


def square(target, pore_diameter='pore.diameter', throat_area='throat.area'):
    r"""
    Calculates internal surface area of pore bodies assuming they are squares
    then subtracts the area of the neighboring throats.

    Parameters
    ----------
    target : OpenPNM Object
        The object for which these values are being calculated.  This
        controls the length of the calculated array, and also provides
        access to other necessary thermofluid properties.

    pore_diameter : string
        The dictionary key to the pore diameter array.

    throat_area : string
        The dictioanry key to the throat area array.  Throat areas are needed
        since their insection with the pore are removed from the computation.

    Returns
    -------
    value : NumPy ndarray
        Array containing pore surface area values.

    """
    network = target.project.network
    D = target[pore_diameter]
    Tn = network.find_neighbor_throats(pores=target.Ps, flatten=False)
    Tsurf = _np.array([_np.sum(network[throat_area][Ts]) for Ts in Tn])
    value = 4*D - Tsurf
    return value
