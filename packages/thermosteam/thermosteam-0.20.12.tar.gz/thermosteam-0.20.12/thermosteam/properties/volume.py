# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# A significant portion of this module originates from:
# Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
# Copyright (C) 2020 Caleb Bell <Caleb.Andrew.Bell@gmail.com>
# 
# This module is under a dual license:
# 1. The UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
# 
# 2. The MIT open-source license. See
# https://github.com/CalebBell/thermo/blob/master/LICENSE.txt for details.
"""
All data and methods related to the vapor pressure of a chemical.

References
----------
.. [1] Yen, Lewis C., and S. S. Woods. "A Generalized Equation for Computer
       Calculation of Liquid Densities." AIChE Journal 12, no. 1 (1966):
       95-99. doi:10.1002/aic.690120119
.. [2] Rackett, Harold G. "Equation of State for Saturated Liquids."
       Journal of Chemical & Engineering Data 15, no. 4 (1970): 514-517.
       doi:10.1021/je60047a012
.. [3] Gunn, R. D., and Tomoyoshi Yamada. "A Corresponding States
        Correlation of Saturated Liquid Volumes." AIChE Journal 17, no. 6
        (1971): 1341-45. doi:10.1002/aic.690170613
.. [4] Yamada, Tomoyoshi, and Robert D. Gunn. "Saturated Liquid Molar
       Volumes. Rackett Equation." Journal of Chemical & Engineering Data 18,
       no. 2 (1973): 234-36. doi:10.1021/je60057a006
.. [5] Hales, J. L, and R Townsend. "Liquid Densities from 293 to 490 K of
       Nine Aromatic Hydrocarbons." The Journal of Chemical Thermodynamics
       4, no. 5 (1972): 763-72. doi:10.1016/0021-9614(72)90050-X
.. [6] Bhirud, Vasant L. "Saturated Liquid Densities of Normal Fluids."
       AIChE Journal 24, no. 6 (November 1, 1978): 1127-31.
       doi:10.1002/aic.690240630
.. [7] Hankinson, Risdon W., and George H. Thomson. "A New Correlation for
       Saturated Densities of Liquids and Their Mixtures." AIChE Journal
       25, no. 4 (1979): 653-663. doi:10.1002/aic.690250412
.. [8] Campbell, Scott W., and George Thodos. "Prediction of Saturated
       Liquid Densities and Critical Volumes for Polar and Nonpolar
       Substances." Journal of Chemical & Engineering Data 30, no. 1
       (January 1, 1985): 102-11. doi:10.1021/je00039a032.
.. [9] Mchaweh, A., A. Alsaygh, Kh. Nasrifar, and M. Moshfeghian.
       "A Simplified Method for Calculating Saturated Liquid Densities."
       Fluid Phase Equilibria 224, no. 2 (October 1, 2004): 157-67.
       doi:10.1016/j.fluid.2004.06.054
.. [10] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
        Chemistry and Physics, 95E. [Boca Raton, FL]: CRC press, 2014.
.. [11] Thomson, G. H., K. R. Brobst, and R. W. Hankinson. "An Improved
        Correlation for Densities of Compressed Liquids and Liquid Mixtures."
        AIChE Journal 28, no. 4 (July 1, 1982): 671-76. doi:10.1002/aic.690280420
.. [12] Goodman, Benjamin T., W. Vincent Wilding, John L. Oscarson, and
        Richard L. Rowley. "A Note on the Relationship between Organic Solid
        Density and Liquid Density at the Triple Point." Journal of Chemical &
        Engineering Data 49, no. 6 (2004): 1512-14. doi:10.1021/je034220e.

"""
import numpy as np
from scipy.interpolate import interp1d
from math import log, exp
from .. import functional as fn
from .._constants import R
from .virial import BVirial_Pitzer_Curl, BVirial_Abbott, BVirial_Tsonopoulos, BVirial_Tsonopoulos_extended
from .dippr import DIPPR_EQ105
# from .electrochem import _Laliberte_Density_ParametersDict, Laliberte_Density
from ..base import (functor, InterpolatedTDependentModel, 
                    TPDependentModel, TPDependentHandleBuilder,
                    PhaseTPHandleBuilder, ThermoModelHandle)
from .data import (VDI_saturation_dict,
                   VDI_tabular_data,
                   V_data_COSTALD,
                   V_data_SNM0,
                   V_data_Perry_l,
                   V_data_VDI_PPDS_2,
                   V_data_CRC_inorg_l,
                   V_data_CRC_inorg_l_const,
                   V_data_CRC_inorg_s_const,
                   V_data_CRC_virial)

__all__ = ('volume_handle',
           'Yen_Woods',
           'Rackett',
           'Yamada_Gunn', 
           'Townsend_Hales', 
           'Bhirud_Normal', 
           'Costald',
           'Campbell_Thodos', 
           'SNM0', 
           'CRC_Inorganic',
           'VDI_PPDS',
           'Costald_Compressed', 
           'ideal_gas',
           'Tsonopoulos_extended',
           'Tsonopoulos', 
           'Abbott', 
           'Pitzer_Curl', 
           'CRCVirial',
           'Goodman')

# %% Liquids

@functor(var='V.l')
def Yen_Woods(T, Tc, Vc, Zc):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar 
    volume (V.l; in m^3/mol) of a chemical using the Yen Woods method, as 
    described in [1]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    Vc : float
        Critical point volume [m^3/mol].
    Zc : float
        Critical compressibility [-].
    
    Notes
    -----
    The molar volume of a liquid is given by:

    .. math::
        Vc/Vs = 1 + A(1-T_r)^{1/3} + B(1-T_r)^{2/3} + D(1-T_r)^{4/3}

        D = 0.93-B

        A = 17.4425 - 214.578Z_c + 989.625Z_c^2 - 1522.06Z_c^3

        B = -3.28257 + 13.6377Z_c + 107.4844Z_c^2-384.211Z_c^3
        \text{ if } Zc \le 0.26

        B = 60.2091 - 402.063Z_c + 501.0 Z_c^2 + 641.0 Z_c^3
        \text{ if } Zc \ge 0.26

    
    Original equation was in terms of density, but it is converted here.

    No example has been found, nor are there points in the article. However,
    it is believed correct. For compressed liquids with the Yen-Woods method,
    see the `Yen_Woods_compressed` function.

    Examples
    --------
    >>> f = Yen_Woods(Tc=647.14, Vc=5.6e-05, Zc=0.2294728175007233)
    >>> f(300)
    1.7715316221999628e-05

    """
    Tr = T/Tc
    A, B, D = calculate_Yen_Woods_terms(Tc, Vc, Zc)
    return Vc/(1 + A*(1-Tr)**(1/3.) + B*(1-Tr)**(2/3.) + D*(1-Tr)**(4./3.))

def calculate_Yen_Woods_terms(Tc, Vc, Zc):
    Zc2 = Zc*Zc
    Zc3 = Zc2*Zc
    A = 17.4425 - 214.578*Zc + 989.625*Zc2 - 1522.06*Zc3
    if Zc <= 0.26:
        B = -3.28257 + 13.6377*Zc + 107.4844*Zc2 - 384.211*Zc3
    else:
        B = 60.2091 - 402.063*Zc + 501.0*Zc2 + 641.0*Zc3
    D = 0.93 - B
    return (A, B, D)

@functor(var='V.l')
def Rackett(T, Tc, Pc, Zc):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar 
    volume (V.l; in m^3/mol) of a chemical using the Rackett method, as 
    described in [2]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    Pc : float
        Critical point pressure [Pa].
    Zc : float
        Critical compressibility [-].
    
    Notes
    -----
    The molar volume of a liquid is given by:

    .. math::
        V_s = \frac{RT_c}{P_c}{Z_c}^{[1+(1-{T/T_c})^{2/7} ]}

    According to Reid et. al, underpredicts volume for compounds with Zc < 0.22

    Examples
    --------
    Propane, example from the API Handbook

    >>> f = Rackett(Tc=369.83, Pc=4248000.0, Zc=0.2763)
    >>> f(T=272.03889)
    8.299222192473635e-05

    """
    return R*Tc/Pc*Zc**(1. + (1. - T/Tc)**(2./7.))

@functor(var='V.l')
def Yamada_Gunn(T, P, Tc, Pc, omega):
    r"""
    Create a functor of temperature (T; in K) and pressure (P; in Pa) that 
    estimates the liquid molar volume (V.l; in m^3/mol) of a chemical using 
    the Yamada Gunn method, as described in [3]_ [4]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    Pc : float
        Critical point pressure [Pa].
    omega : float
        Acentric factor [-].
        
    Notes
    -----
    The molar volume of a liquid is given by:

    .. math::
        V_s = \frac{RT_c}{P_c}{(0.29056-0.08775\omega)}^{[1+(1-{T/T_c})^{2/7}]}

    This equation is an improvement on the Rackett equation.
    This is often presented as the Rackett equation.
    The acentric factor is used here, instead of the critical compressibility.
    A variant using a reference fluid also exists.

    Examples
    --------
    >>> f = Yamada_Gunn(Tc=647.14, Pc=22048320.0, omega=0.344)
    >>> f(T=300, P=101325)
    1.9511311612842117e-08

    """
    k1, k2 = calculate_Yamada_Gunn_terms(Tc, Pc, omega)
    return k1 * k2**(1 + (1 - T/Tc)**(2/7.))

def calculate_Yamada_Gunn_terms(Tc, Pc, omega):
    k1 = R*Tc/Pc
    k2 = (0.29056 - 0.08775*omega)
    return k1, k2

@functor(var='V.l')
def Townsend_Hales(T, Tc, Vc, omega):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar 
    volume (V.l; in m^3/mol) of a chemical using the Townsend Hales method,
    as described in [5]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    Vc : float
        Critical point volume [m^3/mol].
    omega : float
        Acentric factor [-].
    
    Notes
    -----
    The density of a saturated liquid is given by:

    .. math::
        Vs = V_c/\left(1+0.85(1-T_r)+(1.692+0.986\omega)(1-T_r)^{1/3}\right)

    Calculates saturation liquid density, using the Townsend and Hales
    CSP method as modified from the original Riedel equation.

    Examples
    --------
    Calculate the molar volume of water at 300 K:
    
    >>> f = Townsend_Hales(Tc=647.14, Vc=5.6e-05, omega=0.344)
    >>> f(T=300)
    1.8027637900666407e-05

    """
    Tr = T/Tc
    return Vc/(1 + 0.85*(1-Tr) + (1.692 + 0.986*omega)*(1-Tr)**(1/3.))

Bhirud_normal_Trs = [0.98, 0.982, 0.984, 0.986,
                     0.988, 0.99, 0.992, 0.994,
                     0.996, 0.998, 0.999, 1]
Bhirud_normal_lnU0s = [-1.6198, -1.604, -1.59, -1.578,
                       -1.564, -1.548, -1.533, -1.515,
                       -1.489, -1.454, -1.425, -1.243]
Bhirud_normal_lnU1 = [-0.4626, -0.459, -0.451, -0.441,
                      -0.428, -0.412, -0.392, -0.367,
                      -0.337, -0.302, -0.283, -0.2629]
Bhirud_normal_lnU0_interp = interp1d(Bhirud_normal_Trs,
                                     Bhirud_normal_lnU0s, kind='cubic')
Bhirud_normal_lnU1_interp = interp1d(Bhirud_normal_Trs,
                                     Bhirud_normal_lnU1, kind='cubic')

@functor(var='V.l')
def Bhirud_Normal(T, Tc, Pc, omega):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar 
    volume (V.l; in m^3/mol) of a chemical using the Bhirud Normal method, as 
    described in [6]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    Pc : float
        Critical point pressure [Pa].
    omega : float
        Acentric factor [-].
    
    Notes
    -----
    The density of a liquid is given by:

    .. math::
        &\ln \frac{P_c}{\rho RT} = \ln U^{(0)} + \omega\ln U^{(1)}

        &\ln U^{(0)} = 1.396 44 - 24.076T_r+ 102.615T_r^2
        -255.719T_r^3+355.805T_r^4-256.671T_r^5 + 75.1088T_r^6

        &\ln U^{(1)} = 13.4412 - 135.7437 T_r + 533.380T_r^2-
        1091.453T_r^3+1231.43T_r^4 - 728.227T_r^5 + 176.737T_r^6

    Claimed inadequate by others.

    An interpolation table for ln U values are used from Tr = 0.98 - 1.000.
    Has terrible behavior at low reduced temperatures.

    Examples
    --------
    Calculate the molar volume of water at 300 K:

    >>> f = Bhirud_Normal(Tc=647.14, Pc=22048320.0, omega=0.344)
    >>> f(T=300)
    2.069232443882547e-05

    """
    Tr = T/Tc
    if Tr <= 0.98:
        lnU0 = 1.39644 - 24.076*Tr + 102.615*Tr**2 - 255.719*Tr**3 \
            + 355.805*Tr**4 - 256.671*Tr**5 + 75.1088*Tr**6
        lnU1 = 13.4412 - 135.7437*Tr + 533.380*Tr**2-1091.453*Tr**3 \
            + 1231.43*Tr**4 - 728.227*Tr**5 + 176.737*Tr**6
    elif Tr > 1:
        raise Exception('Critical phase, correlation does not apply')
    else:
        lnU0 = Bhirud_normal_lnU0_interp(Tr)
        lnU1 = Bhirud_normal_lnU1_interp(Tr)

    Unonpolar = exp(lnU0 + omega*lnU1)
    return (Unonpolar*R*T)/Pc

@functor(var='V.l')
def Costald(T, Tc, Vc, omega):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar 
    volume (V.l; in m^3/mol) of a chemical using the Costald method, as 
    described in [7]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    Vc : float
        Critical point volume [m^3/mol].
    omega : float
        Acentric factor [-].
    
    Notes
    -----
    A popular and accurate estimation method. If possible, fit parameters are
    used; alternatively critical properties work well.

    The density of a liquid is given by:

    .. math::
        V_s=V^*V^{(0)}[1-\omega_{SRK}V^{(\delta)}]

        V^{(0)}=1-1.52816(1-T_r)^{1/3}+1.43907(1-T_r)^{2/3}
        - 0.81446(1-T_r)+0.190454(1-T_r)^{4/3}

        V^{(\delta)}=\frac{-0.296123+0.386914T_r-0.0427258T_r^2-0.0480645T_r^3}
        {T_r-1.00001}

    Units are that of critical or fit constant volume.

    196 constants are fit to this function in [1]_.
    Range: 0.25 < Tr < 0.95, often said to be to 1.0

    This function has been checked with the API handbook example problem.

    Examples
    --------
    Calculate the volume of water at 300 K and 1 atm:
    
    >>> f = Costald(Tc=647.14, Vc=5.6e-05, omega=0.344)
    >>> f(T=300, P=101325)
    1.8188550933914777e-05
    
    """
    Tr = T/Tc
    V_delta = (-0.296123 + 0.386914*Tr - 0.0427258*Tr**2
        - 0.0480645*Tr**3)/(Tr - 1.00001)
    V_0 = 1 - 1.52816*(1-Tr)**(1/3.) + 1.43907*(1-Tr)**(2/3.) \
        - 0.81446*(1-Tr) + 0.190454*(1-Tr)**(4/3.)
    return Vc*V_0*(1-omega*V_delta)

@functor(var='V.l')
def Campbell_Thodos(T, Tb, Tc, Pc, MW, dipole=None, has_hydroxyl=False):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar
    volume (V.l; in m^3/mol) of a chemical using the Campbell-Thodos CSP 
    method, as described in [8]_.
    
    Parameters
    ----------
    Tb : float
        Boiling point temperature [K].
    Tc : float
        Critical point temperature [K].
    Pc : float
        Critical point pressure [Pa].
    MW : float
        Molecular weight [g/mol].
    dipole : float
        Dipole momment [Debye].
    has_hydroxyl : float
        Whether a polar chemical has hydroxyl groups [-].
    
    Notes
    -----
    An old and uncommon estimation method.

    .. math::
        V_s = \frac{RT_c}{P_c}{Z_{RA}}^{[1+(1-T_r)^{2/7}]}

        Z_{RA} = \alpha + \beta(1-T_r)

        \alpha = 0.3883-0.0179s

        s = T_{br} \frac{\ln P_c}{(1-T_{br})}

        \beta = 0.00318s-0.0211+0.625\Lambda^{1.35}

        \Lambda = \frac{P_c^{1/3}} { M^{1/2} T_c^{5/6}}

    For polar compounds:

    .. math::
        \theta = P_c \mu^2/T_c^2

        \alpha = 0.3883 - 0.0179s - 130540\theta^{2.41}

        \beta = 0.00318s - 0.0211 + 0.625\Lambda^{1.35} + 9.74\times
        10^6 \theta^{3.38}

    Polar Combounds with hydroxyl groups (water, alcohols)

    .. math::
        \alpha = \left[0.690T_{br} -0.3342 + \frac{5.79\times 10^{-10}}
        {T_{br}^{32.75}}\right] P_c^{0.145}

        \beta = 0.00318s - 0.0211 + 0.625 \Lambda^{1.35} + 5.90\Theta^{0.835}


    If a dipole is provided, the polar chemical method is used.
    The paper is an excellent read. Pc is internally converted to atm.

    Examples
    --------
    Calculate the volume of water at 300 K:   
    
    >>> f = Campbell_Thodos(Tb=373.124, Tc=647.14, Pc=22048320.0, MW=18.02, dipole=1.85, has_hydroxyl=True)
    >>> f(T=300, P=101325)
    1.8048013082120765e-05
    
    """
    Pc = Pc/101325.
    Tr = T/Tc
    Tbr = Tb/Tc
    s = Tbr * log(Pc)/(1-Tbr)
    Lambda = Pc**(1./3.)/(MW**0.5*Tc**(5./6.))
    if not (dipole and has_hydroxyl):
        alpha = 0.3883 - 0.0179*s
    beta = 0.00318*s - 0.0211 + 0.625*Lambda**(1.35)
    if dipole:
        theta = Pc*dipole**2/Tc**2
        if has_hydroxyl:
            beta += 5.90*theta**0.835
            alpha = (0.69*Tbr - 0.3342 + 5.79E-10/Tbr**32.75)*Pc**0.145
        else:
            alpha -= 130540 * theta**2.41
            beta += 9.74E6 * theta**3.38
    Zra = alpha + beta*(1-Tr)
    Vs = R*Tc/(Pc*101325)*Zra**(1+(1-Tr)**(2./7.))
    return Vs

@functor(var='V.l')
def SNM0(T, Tc, Vc, omega, delta_SRK):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar 
    volume (V.l; in m^3/mol) of a chemical using the Mchaweh-Moshfeghian 
    method, as described in [9]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    Vc : float
        Critical point volume [m^3/mol].
    omega : float
        Acentric factor [-].
    delta_SRK : float
        Regressed coefficient.
    
    Notes
    -----
    .. math::
        V = V_c/(1+1.169\tau^{1/3}+1.818\tau^{2/3}-2.658\tau+2.161\tau^{4/3}

        \tau = 1-\frac{(T/T_c)}{\alpha_{SRK}}

        \alpha_{SRK} = [1 + m(1-\sqrt{T/T_C}]^2

        m = 0.480+1.574\omega-0.176\omega^2

    If the fit parameter `delta_SRK` is provided (73 provided in the article), the following is used:

    .. math::
        V = V_C/(1+1.169\tau^{1/3}+1.818\tau^{2/3}-2.658\tau+2.161\tau^{4/3})
        /\left[1+\delta_{SRK}(\alpha_{SRK}-1)^{1/3}\right]

    Examples
    --------
    Argon, without the fit parameter and with it. Tabulated result in Perry's
    is 3.4613e-05. The fit increases the error on this occasion.

    >>> f = SNM0(150.8, 7.49e-05, -0.004)
    >>> f(121)
    3.4402256402733416e-05
    >>> f = SNM0(150.8, 7.49e-05, -0.004, -0.03259620)
    >>> f(121)
    3.493288100008123e-05
    
    """
    m = calculate_SNM0_term(omega)
    Tr = T/Tc
    alpha_SRK = (1. + m*(1. - Tr**0.5))**2
    tau = 1. - Tr/alpha_SRK
    rho0 = 1. + 1.169*tau**(1/3.) + 1.818*tau**(2/3.) - 2.658*tau + 2.161*tau**(4/3.)
    V0 = 1./rho0
    return Vc*V0/(1. + delta_SRK*(alpha_SRK - 1.)**(1/3.)) if delta_SRK else Vc*V0


def calculate_SNM0_term(omega):
    return 0.480 + 1.574*omega - 0.176*omega*omega

@functor(var='V.l')
def CRC_Inorganic(T, rho0, k, Tm, MW):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar 
    volume (V.l; in m^3/mol) of a chemical using the CRC Inorganic method.
    
    Parameters
    ----------
    T : float
        Temperature of the liquid, [K]
    rho0 : float
        Mass density of the liquid at Tm, [kg/m^3]
    k : float
        Linear temperature dependence of the mass density, [kg/m^3/K]
    Tm : float
        The normal melting point, used in the correlation [K]
    MW : float
        The molecular weight [g/mol]
    
    Notes
    -----
    Calculates liquid density of a molten element or salt at temperature
    above the melting point. Some coefficients are given nearly up to the
    boiling point.

    The mass density of the inorganic liquid is given by:

    .. math::
        \rho = \rho_{0} - k(T-T_m)

    [10]_ has units of g/mL. While the individual densities could have been
    converted to molar units, the temperature coefficient could only be
    converted by refitting to calculated data. To maintain compatibility with
    the form of the equations, this was not performed.

    This linear form is useful only in small temperature ranges.
    Coefficients for one compound could be used to predict the temperature
    dependence of density of a similar compound.

    Examples
    --------
    >>> CRC_inorganic(300, 2370.0, 2.687, 239.08)
    2206.30796

    
    """
    f = MW/1000
    return (rho0 - k*(T-Tm))*f

@functor(var='V.l')
def VDI_PPDS(T, Tc, rhoc, MW, a, b, c, d):
    tau = 1. - T/Tc if T < Tc else 0.
    rho = rhoc + a*tau**0.35 + b*tau**(2/3.) + c*tau + d*tau**(4/3.)
    return fn.rho_to_V(rho, MW)
   
@functor(var='V.l')
def Costald_Compressed(T, P, Psat, Tc, Pc, omega, V):
    r"""
    Create a functor of temperature (T; in K) and pressure (P; in Pa) that 
    estimates the liquid molar volume (V.l; in m^3/mol) of a chemical using
    the Costald Compressed method, as described in [11]_.
    
    Parameters
    ----------
    Psat : float
        Saturated vapor pressure [Pa].
    Tc : float
        Critical point temperature [K].
    Pc : float
        Critical point pressure [Pa].
    omega : float
        Acentric factor [-].
    V : float
        Molar volume [m^3/mol].
    
    Notes
    -----
    The molar volume of a liquid is given by:

    .. math::
        V = V_s\left( 1 - C \ln \frac{B + P}{B + P^{sat}}\right)

        \frac{B}{P_c} = -1 + a\tau^{1/3} + b\tau^{2/3} + d\tau + e\tau^{4/3}

        e = \exp(f + g\omega_{SRK} + h \omega_{SRK}^2)

        C = j + k \omega_{SRK}

    Original equation was in terms of density, but it is converted here.

    The example is from DIPPR, and exactly correct.
    This is DIPPR Procedure 4C: Method for Estimating the Density of Pure
    Organic Liquids under Pressure.

    Examples
    --------
    >>> f = COSTALD_compressed(9.8E7, 85857.9, 466.7, 3640000.0, 0.281, 0.000105047)
    >>> f(303.)
    9.287482879788506e-05
    
    """
    a = -9.070217
    b = 62.45326
    d = -135.1102
    f = 4.79594
    g = 0.250047
    h = 1.14188
    j = 0.0861488
    k = 0.0344483
    e = exp(f + g*omega + h*omega**2)
    C = j + k*omega
    tau = 1. - T/Tc if T < Tc else 0.
    B = Pc*(-1 + a*tau**(1/3.) + b*tau**(2/3.) + d*tau + e*tau**(4/3.))
    if isinstance(Psat, ThermoModelHandle): Psat = Psat.at_T(T)
    if isinstance(V, ThermoModelHandle): V = V.at_T(T)
    return V*(1 - C*log((B + P)/(B + Psat)))

@TPDependentHandleBuilder('V.l')
def volume_liquid_handle(handle, CAS, MW, Tb, Tc, Pc, Vc, Zc,
                         omega, Psat, eos, dipole, has_hydroxyl):
    Tmin = 50
    Tmax = 1000
    all_ = all
    add_model = handle.add_model
    if CAS in V_data_VDI_PPDS_2:
        _, MW, Tc_, rhoc, A, B, C, D = V_data_VDI_PPDS_2[CAS]
        data = (Tc, rhoc, MW, A, B, C, D)
        add_model(VDI_PPDS.from_args(data), 0., Tc_)
    if CAS in V_data_Perry_l:
        _, C1, C2, C3, C4, Tmin, Tmax = V_data_Perry_l[CAS]
        data = (C1, C2, C3, C4, True)
        add_model(DIPPR_EQ105.from_args(data), Tmin, Tmax)
    if CAS in VDI_saturation_dict:
        Ts, Vls = VDI_tabular_data(CAS, 'Volume (l)')
        model = InterpolatedTDependentModel(Ts, Vls,
                                            Tmin=Ts[0], Tmax=Ts[-1])
        add_model(model)
    data = (Tb, Tc, Pc, MW, dipole, has_hydroxyl)
    if all_([i is not None for i in data]):
        add_model(Campbell_Thodos.from_args(data), 0, Tc)
    if CAS in V_data_CRC_inorg_l:
        _, MW, rho, k, Tm, Tmax = V_data_CRC_inorg_l[CAS]
        data = (MW, rho, k, Tm)
        add_model(CRC_Inorganic.from_args(data), Tm, Tmax)
    data = (Tc, Vc, Zc)
    if all_(data):
        add_model(Yen_Woods.from_args(data))
    data = (Tc, Pc, Zc)
    if all_(data):
        add_model(Rackett.from_args(data), 0, Tc)
    data = (Tc, Pc, omega)
    if all_(data):
        add_model(Yamada_Gunn.from_args(data), 0, Tc)
        add_model(Bhirud_Normal.from_args(data), 0, Tc)
    data = (Tc, Vc, omega)
    if all_(data):
        add_model(Townsend_Hales.from_args(data), 0, Tc)
        if CAS in V_data_SNM0:
            SNM0_delta_SRK = float(V_data_SNM0.at[CAS, 'delta_SRK'])
            data = (Tc, Vc, omega, SNM0_delta_SRK)
            add_model(SNM0.from_args(data))
    if CAS in V_data_CRC_inorg_l_const:
        Vl = float(V_data_CRC_inorg_l_const.at[CAS, 'Vm'])
        add_model(Vl, Tmin, Tmax, name="CRC inorganic liquid constant")
    if Tc and Pc and CAS in V_data_COSTALD:
        Zc_ = V_data_COSTALD.at[CAS, 'Z_RA']
        if not np.isnan(Zc_): Zc_ = float(Zc_)
        data = (Tc, Pc, Zc_)
        add_model(Rackett.from_args(data), Tmin, Tmax)
        # Roughly data at STP; not guaranteed however; not used for Trange
    data = (Tc, Vc, omega)
    if all_(data) and CAS in V_data_COSTALD:
        add_model(Costald.from_args(data), 0, Tc)
    data = (Tc, Pc, omega)
    if all_(data):
        data = (Psat, Tc, Pc, omega, handle)
        add_model(Costald_Compressed.from_args(data), 50, 500)
        

# %% Gases

def ideal_gas(T, P): return R*T/P

ideal_gas_model = TPDependentModel(ideal_gas,
                                   0, 10e6,
                                   0, 10e12,
                                   var='V.g')

@functor(var='V.g')
def Tsonopoulos_extended(T, P, Tc, Pc, omega, a=0, b=0,
                         species_type='', dipole=0, order=0):
    return ideal_gas(T, P) + BVirial_Tsonopoulos_extended(T, Tc, Pc, omega, a, b,
                                                          species_type, dipole, order)
@functor(var='V.g') 
def Tsonopoulos(T, P, Tc, Pc, omega):
    return ideal_gas(T, P) + BVirial_Tsonopoulos(T, Tc, Pc, omega)

@functor(var='V.g')
def Abbott(T, P, Tc, Pc, omega):
    return ideal_gas(T, P) + BVirial_Abbott(T, Tc, Pc, omega)

@functor(var='V.g')
def Pitzer_Curl(T, P, Tc, Pc, omega):
    return ideal_gas(T, P) + BVirial_Pitzer_Curl(T, Tc, Pc, omega)
    
@functor(var='V.g')
def CRCVirial(T, P, a1, a2, a3, a4, a5):
    t = 298.15/T - 1.
    return ideal_gas(T, P) + (a1 + a2*t + a3*t**2 + a4*t**3 + a5*t**4)/1e6

@TPDependentHandleBuilder('V.g')
def volume_gas_handle(handle, CAS, Tc, Pc, omega, eos):
    add_model = handle.add_model
    # no point in getting Tmin, Tmax
    if all((Tc, Pc, omega)):
        data = (Tc, Pc, omega)
        add_model(Tsonopoulos_extended.from_args(data))
        add_model(Tsonopoulos.from_args(data))
        add_model(Abbott.from_args(data))
        add_model(Pitzer_Curl.from_args(data))
    if CAS in V_data_CRC_virial:
        _, *data = V_data_CRC_virial[CAS]
        add_model(CRCVirial.from_args(data))
    add_model(ideal_gas_model)


# %% Solids

@functor(var='V.s')
def Goodman(T, Tt, V_l):
    r"""
    Create a functor of temperature (T; in K) that estimates the solid molar
    volume (V.s; in m^3/mol) of a chemical using the Goodman method, as 
    described in [12]_.
    
    Parameters
    ----------
    Tt : float
        Triple point temperature [K].
    V_l : float
        Liquid molar volume [-].
    
    Notes
    -----
    Calculates solid density at T using the simple relationship
    by a member of the DIPPR.

    The molar volume of a solid is given by:

    .. math::
        \frac{1}{V_m} = \left( 1.28 - 0.16 \frac{T}{T_t}\right)
        \frac{1}{{Vm}_L(T_t)}

    Works to the next solid transition temperature or to approximately 0.3Tt.

    Examples
    --------
    >>> f = Goodman(353.43, 7.6326)
    >>> f(281.46)
    8.797191839062899

    """
    return (1.28 - 0.16*(T/Tt))*V_l

@TPDependentHandleBuilder('V.s')
def volume_solid_handle(handle, CAS):
    if CAS in V_data_CRC_inorg_s_const:
        CRC_INORG_S_Vm = float(V_data_CRC_inorg_s_const.at[CAS, 'Vm'])
        handle.add_model(CRC_INORG_S_Vm, 0, 1e6, 0, 1e12)


volume_handle = PhaseTPHandleBuilder('V',
                                       volume_solid_handle, 
                                       volume_liquid_handle,
                                       volume_gas_handle)

