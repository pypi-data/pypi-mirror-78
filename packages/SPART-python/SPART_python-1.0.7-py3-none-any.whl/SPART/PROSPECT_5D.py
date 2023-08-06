"""
SPART-python

PROSPECT 5D model.

Feret et al. - PROSPECT-D: Towards modeling leaf optical properties
    through a complete lifecycle
"""
import numpy as np
import scipy.integrate as integrate


class LeafBiology:
    """
    Class to hold leaf biology variables.

    Parameters
    ----------
    Cab : float
        Chlorophyll concentration, micro g / cm ^ 2
    Cca : float
        Carotenoid concentration, micro g / cm ^ 2
    Cw : float
        Equivalent water thickness, cm
    Cdm : float
        Leaf mass per unit area, g / cm ^ 2
    Cs : float
        Brown pigments (from SPART paper, unitless)
    Cant : float
        Anthocyanin content, micro g / cm ^ 2
    N : float
        Leaf structure parameter. Unitless.

    Attributes
    ----------
    Cab : float
        Chlorophyll concentration, micro g / cm ^ 2
    Cca : float
        Carotenoid concentration, micro g / cm ^ 2
    Cw : float
        Equivalent water thickness, cm
    Cdm : float
        Leaf mass per unit area, g / cm ^ 2
    Cs : float
        Fraction senescent material (brown pigment from SPART paper, unitless)
    Cant : float
        Anthocyanin content, micro g / cm ^ 2
    N : float
        Leaf structure parameter. Unitless.
    rho_thermal : float
        Reflectance in the thermal range. SPART assumption: 0.01
    tau_thermal : float
        Transmittance in the thermal range. SPART assumption: 0.01
    """

    def __init__(self, Cab, Cca, Cw, Cdm, Cs, Cant, N):
        self.Cab = Cab
        self.Cca = Cca
        self.Cw = Cw
        self.Cdm = Cdm
        self.Cs = Cs
        self.Cant = Cant
        self.N = N
        self.rho_thermal = 0.01
        self.tau_thermal = 0.01


class LeafOptics:
    """
    Class to hold leaf optics information.

    Parameters
    ----------
    refl : np.array
        Spectral reflectance of the leaf, 400 to 2400 nm
    tran : np.array
        Spectral transmittance of the leaf, 400 to 2400 nm
    kChlrel : np.array
        Relative portion of chlorophyll contribution to reflecntace
        / transmittance in the spectral range, 400 to 2400 nm

    Attributes
    ----------
    refl : np.array
        Spectral reflectance of the leaf, 400 to 2400 nm
    tran : np.array
        Spectral transmittance of the leaf, 400 to 2400 nm
    kChlrel : np.array
        Relative portion of chlorophyll contribution to reflecntace
        / transmittance in the spectral range, 400 to 2400 nm
    """
    def __init__(self, refl, tran, kChlrel):
        self.refl = refl
        self.tran = tran
        self.kChlrel = kChlrel


def PROSPECT_5D(leafbio, optical_params):
    """
    PROSPECT_5D model.

    Parameters
    ----------
    leafbio : LeafBiology
        Object holding user specified leaf biology model parameters.
    optical_params : dict
        Optical parameter constants. Loaded externally and passed in.

    Returns
    -------
    LeafOptics
        Contains attributes relf, tran, kChlrel for reflectance, transmittance
        and contribution of chlorophyll over the 400 nm to 2400 nm spectrum
    """
    # Leaf parameters
    Cab = leafbio.Cab
    Cca = leafbio.Cca
    Cw = leafbio.Cw
    Cdm = leafbio.Cdm
    Cs = leafbio.Cs
    Cant = leafbio.Cant
    N = leafbio.N

    # Model constants
    nr = optical_params['nr']
    Kdm = optical_params['Kdm']
    Kab = optical_params['Kab']
    Kca = optical_params['Kca']
    Kw = optical_params['Kw']
    Ks = optical_params['Ks']
    Kant = optical_params['Kant']

    # Compact leaf layer
    Kall = (Cab * Kab + Cca * Kca + Cdm * Kdm + Cw * Kw + Cs * Ks +
            Cant * Kant) / N

    # Non-conservative scattering (normal case)
    j = np.where(Kall > 0)[0]
    t1 = (1 - Kall) * np.exp(-Kall)

    def expint(x):
        # NOTE: differences in final output come from this integral
        # which evaluates slightly different (10 decimal places) than matlab
        # Exponential integral from expint command in matlab
        def intergrand(t):
            return np.exp(-t) / t
        return integrate.quad(intergrand, x, np.inf)

    t2 = Kall ** 2 * np.vectorize(expint)(Kall)[0]
    tau = np.ones((len(t1), 1))
    tau[j] = t1[j] + t2[j]
    kChlrel = np.zeros((len(t1), 1))
    kChlrel[j] = Cab * Kab[j] / (Kall[j] * N)

    t_alph = calculate_tav(40, nr)
    r_alph = 1 - t_alph
    t12 = calculate_tav(90, nr)
    r12 = 1 - t12
    t21 = t12 / (nr ** 2)
    r21 = 1 - t21

    # top surface side
    denom = 1 - r21 * r21 * tau ** 2
    Ta = t_alph * tau * t21 / denom
    Ra = r_alph + r21 * tau * Ta

    # bottom surface side
    t = t12 * tau * t21 / denom
    r = r12 + r21 * tau * t

    # Stokes equations to compute properties of next N-1 layers (N real)

    # Normal case
    D = np.sqrt((1 + r + t) * (1 + r - t) * (1 - r + t) * (1 - r - t))
    rq = r ** 2
    tq = t ** 2
    a = (1 + rq - tq + D) / (2 * r)
    b = (1 - rq + tq + D) / (2 * t)

    bNm1 = b ** (N - 1)
    bN2 = bNm1 ** 2
    a2 = a ** 2
    denom = a2 * bN2 - 1
    Rsub = a * (bN2 - 1) / denom
    Tsub = bNm1 * (a2 - 1) / denom

    # Case of zero absorption
    j = np.where(r + t >= 1)[0]
    Tsub[j] = t[j] / (t[j] + (1 - t[j]) * (N - 1))
    Rsub[j] = 1 - Tsub[j]

    # Reflectance and transmittance of the leaf:
    #   combine top llayer with next N-1 layers
    denom = 1 - Rsub * r
    tran = Ta * Tsub / denom
    refl = Ra + Ta * Rsub * t / denom

    leafopt = LeafOptics(refl, tran, kChlrel)

    return leafopt


def calculate_tav(alpha, nr):
    """
    Calculate average transmissitivity of a dieletrie plane surface.

    Parameters
    ----------
    alpha : float
        Maximum incidence angle defining the solid angle.
    nr : float
        Refractive index

    Returns
    -------
    float
        Transmissivity of a dielectric plane surface averages over all
        directions of incidence and all polarizations.

    NOTE
    ----
    Lifted directly from original SPART matlab calculations.
    Papers cited in original PROSPECT model:
    Willstatter-Stoll Theory of Leaf Reflectance Evaluated
    by Ray Tracinga - Allen et al.
    Transmission of isotropic radiation across an interface
    between two dielectrics - Stern
    """
    rd = np.pi / 180
    n2 = nr ** 2
    n_p = n2 + 1
    nm = n2 - 1
    a = (nr + 1) * (nr + 1) / 2
    k = -(n2 - 1) * (n2 - 1) / 4
    sa = np.sin(alpha * rd)

    b1 = 0
    if alpha != 90:
        b1 = np.sqrt((sa ** 2 - n_p / 2) * (sa ** 2 - n_p / 2) + k)
    b2 = sa ** 2 - n_p / 2
    b = b1 - b2
    b3 = b ** 3
    a3 = a ** 3
    ts = (k ** 2 / (6 * b3) + k / b - b / 2) - (k ** 2 / (6 * a3) + k / a
                                                - a / 2)

    tp1 = -2 * n2 * (b - a) / (n_p ** 2)
    tp2 = -2 * n2 * n_p * np.log(b / a) / (nm ** 2)
    tp3 = n2 * (1 / b - 1 / a) / 2
    tp4 = (16 * n2 ** 2 * (n2 ** 2 + 1) * np.log((2 * n_p * b - nm ** 2) /
                                                 (2 * n_p * a - nm ** 2))
           / (n_p ** 3 * nm ** 2))
    tp5 = (16 * n2 ** 3 * (1 / (2 * n_p * b - nm ** 2) - 1 / (2 * n_p * a -
                                                              nm ** 2))
           / n_p ** 3)
    tp = tp1 + tp2 + tp3 + tp4 + tp5
    tav = (ts + tp) / (2 * sa ** 2)

    return tav


if __name__ == '__main__':
    # Test cases, compare to original matlab outputs
    from SPART import load_optical_parameters
    leafbio = LeafBiology(40, 10, 0.02, 0.01, 0, 10, 1.5)
    leafopt = PROSPECT_5D(leafbio, load_optical_parameters())
    print(leafopt.tran)
    print(leafopt.refl)
    print(leafopt.kChlrel)
