""" This module contains the SEDs of the different physical
components that are allowed in the likelihood. The list
of currently allowed SEDs is:

* :py:func:`cmb`
* :py:func:`syncpl`
* :py:func:`sync_curvedpl`
* :py:func:`dustmbb`

These are referred to by name when defining the :py:class:`FMatrix`
object, which then composes the model as a linear sum of the
various components.

Notes
-----

All the SEDs in this file assume RJ units.




.. plot::
    :include-source:

    import matplotlib.pyplot as plt
    import numpy as np
    from mesmer.seds import *

    freqs = np.logspace(1, 3)
    c = cmb(freqs)
    s = syncpl(freqs, 100., -3)
    d = dustmbb(freqs, 100., 1.5, 20.)
    sc = sync_curvedpl(freqs, 100, -3, 0.05)
    fmatrix = FMatrix(['cmb', 'syncpl', 'dustmbb'])
    params = {
        'nu': freqs,
        'nu_ref_s': 100.,
        'nu_ref_d': 100.,
        'beta_d': 1.5,
        'T_d': 20.,
        'beta_s': -3.
    }
    f = np.sum(fmatrix(**params), axis=0)
    fig, ax = plt.subplots(1, 1)
    ax.loglog(freqs, c, label='cmb')
    ax.loglog(freqs, s, label='syncpl')
    ax.loglog(freqs, d, label='dustmbb')
    ax.loglog(freqs, sc, label='sync_curvedpl')
    ax.loglog(freqs, f, label='fmatrix (c+s+d)')
    ax.set_xlabel('frequency (GHz)')
    ax.set_ylabel('f(nu)')
    ax.set_xlim(23., 400.)
    ax.set_ylim(1e-2, 1e2)
    ax.legend()
    plt.show()

"""

import jax.numpy as np

__all__ = ["FMatrix", "cmb", "syncpl", "sync_curvedpl", "dustmbb"]


class FMatrix(object):
    """ Class to construct the foreground mixing matrix.
    This class models foreground SEDs of the different
    components of the sky model. This is an implementation of
    Equation (10) in 1608.00551, for a single set of
    spectral parameters.

    Examples
    --------

    >>> from mesmer.seds import FMatrix
    >>> fmatrix = FMatrix(['cmb', 'syncpl', 'dustmbb'])
    >>> pars = {
    ...     'nu': np.array([1, 100, 1000]),
    ...     'nu_ref_d' : 100.,
    ...     'nu_ref_s' : 100.,
    ...     'beta_s' : -3.,
    ...     'beta_d' : 1.5,
    ...     'T_d' : 20.,
    ... }
    >>> print(fmatrix(**pars).shape)
    (3, 3)

    """

    def __init__(self, components):
        """ Once instantiated this function evaluates the component SEDs
        with which this class was instantiated.

        As it is used in a variety of contexts, the
        :class:`mesmer.seds.FMatrix` can be called in a variety of ways.
        It must ultimately be passed the arguments for all of the component
        functions. This is usually done through keyword arguments, however,
        the frequency can be passed as the only positional argument.

        Parameters
        ----------
        components: list(str)
            List of function names. These functions, evaluated
            at a list of frequencies, will give the mixing
            matrix, `F`.

        Returns
        -------
        ndarray
            Array of shape (ncomps, nfreqs), representing the component
            SEDs evaluated for the requested frequencies.
        """
        assert isinstance(components, list)
        # check that the list of components correspond to existing functions
        for component in components:
            assert component in ["dustmbb", "syncpl", "cmb", "sync_curvedpl"]
        self.components = components

    def __call__(self, *args, **parameters) -> np.ndarray:
        """


        """
        if parameters:
            self.parameters = parameters
        if args:
            self.parameters.update(*args)
        # evaluate each component function for the point in parameter space
        # specified by `parameters` N.B that each `comp_func` is passed all
        # the parameters - this requires that no two functions share argument
        # names.
        outputs = [
            globals()[comp_func](**self.parameters)[None]
            for comp_func in self.components
        ]
        return np.concatenate(list(outputs))


def cmb(nu: np.ndarray, *args, **kwargs) -> np.ndarray:
    """ Function to compute CMB SED, as a function of frequency.

    This function computes the scaling of the Brightness temperature
    as a function of frequency. See for example Equation (3) of
    Ichiki + 2014 (A concise review of foreground emission).

    The definition of brightness temperature is:

    .. math::

        f_{CMB}(\\nu) = e^x \\frac{x}{(e^x - 1)^2}

    Parameters
    ----------
    nu: float, or array_like(float)
        Frequency in GHz, :math:`\\nu`.

    Returns
    -------
    ndarray
        CMB brightness temperature sed  evaluated at frequency nu.
    """
    x = 0.0176086761 * nu
    ex = np.exp(x)
    sed = ex * (x / (ex - 1)) ** 2
    return sed


def syncpl(
    nu: np.ndarray, nu_ref_s: np.float32, beta_s: np.float32, *args, **kwargs
) -> np.ndarray:
    """ Function to compute synchrotron power law SED, given by:

    .. math::
        f_{\\rm sync}(\\nu) = \\left(\\nu / \\nu_s \\right)^{\\beta_s}

    Parameters
    ----------
    nu: float, or array_like(float)
        Frequency in GHz, :math:`\\nu`.
    nu_ref_s: float
        Reference frequency in GHz, :math:`\\nu_s`.
    beta_s: float
        Power law index in RJ units, :math:`\\beta_s`.

    Returns
    -------
    array_like(float)
        Synchroton SED relative to reference frequency.
    """
    return (nu / nu_ref_s) ** beta_s


def sync_curvedpl(
    nu: np.ndarray,
    nu_ref_s: np.float32,
    beta_s: np.float32,
    beta_c: np.float32,
    *args,
    **kwargs
) -> np.ndarray:
    """ Function to compute curved synchrotron power law SED,
    given by:

    .. math::

        f_{\\rm syncpl}(\\nu) = \\left(\\nu / \\nu_s \\right)^{\\beta_s +
        \\beta_c \\ln(\\nu / \\nu_s)}

    Parameters
    ----------
    nu: float, or array_like(float)
        Frequency in GHz, :math:`\\nu`.
    nu_ref_s: float
        Reference frequency in GHz, :math:`\\nu_s`.
    beta_s: float
        Power law index in RJ units, :math:`\\beta_s``.
    beta_c: float
        Power law index curvature, :math:`\\beta_c`.

    Returns
    -------
    array_like(float)
        Synchroton SED relative to reference frequency.
    """
    return (nu / nu_ref_s) ** (beta_s + beta_c * np.log(nu / nu_ref_s))


def dustmbb(
    nu: np.ndarray,
    nu_ref_d: np.float32,
    beta_d: np.float32,
    T_d: np.float32,
    *args,
    **kwargs
) -> np.ndarray:
    """ Function to compute modified blackbody dust SED, given by:

    .. math::

        f_{\\rm dust}(\\nu) = \\left(\\nu / \\nu_d \\right)^{1 + \\beta_d}
        \\frac{e^{h \\nu_d / (k_B T_d)} - 1} {e^{h \\nu / (k_B T_d)} - 1}

    Recall that:

    .. math::

        B_\\nu(\\nu, T) = \\frac{2h\\nu^3}{c^2}\\frac{1}{e^{h\\nu/kT} - 1}.


    Parameters
    ----------
    nu: float or array_like(float)
        Freuency at which to calculate SED, :math:`\\nu`.
    nu_ref_d: float
        Reference frequency in GHz, :math:`\\nu_d`.
    beta_d: float
        Power law index of dust opacity, :math:`\\beta_d`.
    T_d: float
        Temperature of the dust, :math:`T_d`.

    Returns
    -------
    array_like(float)
        SED of dust modified black body relative to reference frequency.
    """
    x_to = np.float32(0.0479924466) * nu / T_d
    x_from = np.float32(0.0479924466) * nu_ref_d / T_d
    sed = (nu / nu_ref_d) ** (1.0 + beta_d)
    sed *= (np.exp(x_from) - 1) / (np.exp(x_to) - 1)
    return sed
